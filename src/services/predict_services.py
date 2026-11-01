from datetime import timedelta

import pandas as pd
from fastapi import HTTPException
from src.depends.db import reports


train_codes = {"12625": 0, "16306": 1, "16325": 2, "16346": 3}


def predict_services(station_code: str, model):
    # Use the same column names and order as training.
    cols = model.feature_names_in_

    if not reports:
        raise HTTPException(status_code=400, detail="No live data found. Please fetch live data first via /live.")


    stations = reports[-1].get("data", [])
    data = next(
        (item for item in stations if str(item.get("station_code", "")).strip().upper() == station_code.strip().upper()),
        None
    )
    if not data:
        raise HTTPException(status_code=404, detail=f"Station code '{station_code}' not found in the latest report. Try refreshing live data.")

    if "prediction_available" in reports[-1] and "model_features" not in data:
        raise HTTPException(status_code=422, detail="This station could not be matched to the model's training inputs.")
    features = data.get("model_features", data)
    scheduled_arrival = features.get("scheduled_arrival_iso")
    df = pd.DataFrame([features]).drop(columns=["scheduled_arrival_iso"], errors="ignore")
    df["train_no"] = df["train_no"].astype(str).map(train_codes)
    
    
    
    if df[["train_no", "station_time_difference"]].isna().any().any():
        raise HTTPException(status_code=422, detail="Train or station time difference was not seen during training.")
    
    
    
    
    df = pd.get_dummies(df, columns=["station_code"], dtype=int)
    df = df.reindex(columns=cols, fill_value=0)
    
    
    

    prediction = model.predict(df)
    delay_minutes = float(prediction[0])

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
        "train_no": data.get("train_no"),
        "station_code": data.get("station_code"),
        "predicted_delay_arrival_min": delay_minutes,
        "predict_time": predict_time_str,
        "prediction_note": reports[-1].get("prediction_message")
    }
