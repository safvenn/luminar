from datetime import timedelta
import math

import pandas as pd
from fastapi import HTTPException
from src.depends.db import reports
from src.services.live_prediction import metadata


train_codes = {"12625": 0, "16306": 1, "16325": 2, "16346": 3}


def _predict_one(features: dict, model) -> float:
    cols = model.feature_names_in_
    df = pd.DataFrame([features]).drop(columns=["scheduled_arrival_iso"], errors="ignore")
    df["train_no"] = df["train_no"].astype(str).map(train_codes)
    if df[["train_no", "station_time_difference"]].isna().any().any():
        raise HTTPException(status_code=422, detail="Train or station time difference was not seen during training.")

    station_seqs = metadata.get("station_sequences", {}).get(str(features.get("train_no")), {})
    if station_seqs and str(features.get("station_code")).strip().upper() not in station_seqs:
        raise HTTPException(status_code=422, detail="Station was not seen for this train during training.")

    required = [col for col in cols if not col.startswith("station_code_")]
    if any(col not in df or not math.isfinite(float(df.iloc[0][col])) for col in required):
        raise HTTPException(status_code=422, detail="Required model inputs are missing or invalid.")

    df = pd.get_dummies(df, columns=["station_code"], dtype=int)
    df = df.reindex(columns=cols, fill_value=0)

    prediction = model.predict(df)
    delay_minutes = float(prediction[0])

    if not math.isfinite(delay_minutes):
        raise HTTPException(status_code=422, detail="Model returned an invalid prediction.")

    return delay_minutes


def predict_services(
    station_code: str,
    model,
    train_no: str | None = None,
    report_id: str | None = None,
):
    report = None
    if report_id:
        report = next(
            (r for r in reversed(reports) if str(r.get("report_id", "")).strip() == str(report_id).strip()),
            None,
        )
    if report is None and train_no:
        report = next(
            (r for r in reversed(reports) if str(r.get("train_no", "")).strip() == str(train_no).strip()),
            None,
        )
    if report is None:
        report = reports[-1] if reports else None

    if report is None:
        raise HTTPException(status_code=400, detail="No live data found. Please fetch live data first via /live.")

    stations = report.get("data", [])
    data = next(
        (item for item in stations if str(item.get("station_code", "")).strip().upper() == station_code.strip().upper()),
        None,
    )
    if not data:
        raise HTTPException(status_code=404, detail=f"Station code '{station_code}' not found in the latest report. Try refreshing live data.")

    if not data.get("prediction_available", True) or "model_features" not in data:
        raise HTTPException(status_code=422, detail=data.get("prediction_reason") or "Prediction unavailable for this station.")

    route = sorted(
        (row for row in stations if row.get("current_route", True) and "seq" in row),
        key=lambda row: row["seq"],
    )
    observed = [row for row in route if row.get("live_status") in ("passed", "current")]
    if not observed:
        raise HTTPException(status_code=422, detail="No observed station delay is available. Refresh your train.")

    history = []
    for row in observed:
        value = row.get("live_delay_min")
        if value is not None:
            try:
                value = float(value)
            except (TypeError, ValueError):
                continue
            if math.isfinite(value):
                history.append(value)

    latest = observed[-1].get("live_delay_min")
    try:
        latest_valid = latest is not None and math.isfinite(float(latest))
    except (TypeError, ValueError):
        latest_valid = False

    if not history or not latest_valid:
        if not history and report.get("current_delay") is not None:
            try:
                cd = float(report["current_delay"])
                if math.isfinite(cd):
                    history.append(cd)
                    latest_valid = True
            except (TypeError, ValueError):
                pass

    if not history or not latest_valid:
        raise HTTPException(status_code=422, detail="The latest observed station delay is missing. Refresh your train.")

    last_seq = observed[-1]["seq"]
    if data["seq"] <= last_seq:
        raise HTTPException(status_code=422, detail="Prediction is only available for an upcoming arrival.")

    steps = []
    delay_minutes = history[-1]
    for row in route:
        if not last_seq < row["seq"] <= data["seq"]:
            continue
        if not row.get("prediction_available", True) or "model_features" not in row:
            raise HTTPException(
                status_code=422,
                detail=f"Cannot predict through {row['station_code']}: supported schedule inputs are missing.",
            )
        features = dict(row["model_features"])
        recent = history[-3:]
        features.update(
            previous_delay=recent[-1],
            previous_departure_delay=recent[-1],
            previous_delay2=recent[-2] if len(recent) >= 2 else 0.0,
            previous_delay3=recent[-3] if len(recent) >= 3 else 0.0,
            last_three_delay_avg=sum(recent) / len(recent),
        )
        delay_minutes = _predict_one(features, model)
        history.append(delay_minutes)
        steps.append({
            "station_code": row["station_code"],
            "station_name": row.get("station_name"),
            "predicted_delay_arrival_min": delay_minutes,
        })

    if not steps:
        raise HTTPException(status_code=422, detail="Target is not on the upcoming route.")

    scheduled_arrival = data["model_features"].get("scheduled_arrival_iso")
    predict_time_str = None
    if scheduled_arrival:
        try:
            scheduled_dt = pd.Timestamp(scheduled_arrival)
            if scheduled_dt.tzinfo is not None:
                scheduled_dt = scheduled_dt.tz_convert("Asia/Kolkata")
            predicted_dt = scheduled_dt + timedelta(minutes=delay_minutes)
            predict_time_str = predicted_dt.time().strftime("%H:%M:%S")
        except (ValueError, TypeError):
            predict_time_str = None

    return {
        "report_id": report.get("report_id"),
        "train_no": data.get("train_no") or report.get("train_no"),
        "station_code": data.get("station_code"),
        "station_name": data.get("station_name"),
        "predicted_delay_arrival_min": delay_minutes,
        "predict_time": predict_time_str,
        "prediction_method": "recursive",
        "prediction_steps": steps,
        "prediction_note": (
            "Predicted each upcoming station in order. Earlier estimates feed later predictions; "
            "errors can grow with distance. Departure delay is assumed equal to arrival delay."
        ),
    }
