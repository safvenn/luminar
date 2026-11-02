from datetime import timedelta
from time import time
import math

import pandas as pd
from fastapi import HTTPException
from src.depends.db import reports
from src.services.live_prediction import metadata

train_codes = {"12625": 0, "16306": 1, "16325": 2, "16346": 3}

def predict_services(station_code: str, model, report_id: str):
    # Use the same column names and order as training.
    cols = model.feature_names_in_

    report = next((item for item in reports if item.get("report_id") == report_id), None)
    if report is None or time() - report.get("created_at", 0) > 1800:
        raise HTTPException(status_code=409, detail="Journey report expired or unavailable. Refresh your train.")
    stations = report.get("data", [])
    data = next(
        (item for item in stations if str(item.get("station_code", "")).strip().upper() == station_code.strip().upper()),
        None
    )
    if not data:
        raise HTTPException(status_code=404, detail=f"Station code '{station_code}' not found in this journey report. Try refreshing live data.")

    if not data.get("prediction_available") or "model_features" not in data:
        raise HTTPException(status_code=422, detail=data.get("prediction_reason") or "Prediction unavailable for this station.")
    features = data.get("model_features", data)
    scheduled_arrival = features.get("scheduled_arrival_iso")
    df = pd.DataFrame([features]).drop(columns=["scheduled_arrival_iso"], errors="ignore")
    df["train_no"] = df["train_no"].astype(str).map(train_codes)
    if df[["train_no", "station_time_difference"]].isna().any().any():
        raise HTTPException(status_code=422, detail="Train or station time difference was not seen during training.")
    if station_code.strip().upper() not in metadata["station_sequences"].get(str(features["train_no"]), {}):
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

    # Safely compute predicted arrival time
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
        "report_id": report_id,
        "train_no": data.get("train_no"),
        "station_code": data.get("station_code"),
        "predicted_delay_arrival_min": delay_minutes,
        "predict_time": predict_time_str,
        "prediction_note": report.get("prediction_message")
    }
