"""Prepare model inputs from completed live stops and the timetable."""
import json
import math
from pathlib import Path

import pandas as pd
from src.services.live_data_services import extract_features

metadata = json.loads((Path(__file__).resolve().parents[1] / "ml" / "preprocessing.json").read_text())
time_codes = {value: index for index, value in enumerate(metadata["time_classes"])}


def date_near(day_month, reference):
    # Live dates omit the year; handle journeys across New Year too.
    dates = []
    for year in range(reference.year - 1, reference.year + 2):
        try:
            dates.append(pd.to_datetime(f"{day_month}-{year}", format="%d-%b-%Y").tz_localize("Asia/Kolkata"))
        except ValueError:
            continue
    if not dates:
        raise ValueError("Live stop date is missing or invalid")
    return min(dates, key=lambda value: abs(value - reference))


def add_prediction_features(rows, live, train_type):
    for row in rows:
        row.pop("model_features", None)
        row["prediction_available"] = False
        row["prediction_reason"] = "Station or timetable is not supported by the trained model."
    updated = pd.Timestamp(live["updatedAt"]).tz_convert("Asia/Kolkata")
    first = live["stops"][0]
    journey_date = date_near(first["date"], updated) - pd.Timedelta(days=int(first["day"]) - 1)
    route = []

    def scheduled(clock, offset):
        return None if clock is None else journey_date + pd.Timedelta(days=int(offset or 0)) + pd.Timedelta(clock)

    for row in rows:
        arrival = scheduled(row["scheduled_arrival"], row["arrival_day_offset"])
        departure = scheduled(row["scheduled_departure"], row["departure_day_offset"])

        arr_delay = dep_delay = None
        # Observed stops: passed or currently at station
        if row.get("live_status") in ("passed", "current"):
            # Reconcile timetable and live API delay information:
            # The live API directly provides reliable delayMin.
            if row.get("live_delay_min") is not None and math.isfinite(float(row["live_delay_min"])):
                arr_delay = float(row["live_delay_min"])
                dep_delay = float(row["live_delay_min"])

        # Do not repeat delays across missing or upcoming stops.
        route.append({
            "stationCode": row["station_code"], "sequence": row["seq"],
            "distance": row["distance_km"], "haltsHere": 1, "platform": 1,
            "scheduledArrival": arrival.isoformat() if arrival is not None else None,
            "scheduledDeparture": departure.isoformat() if departure is not None else None,
            "delayArrival": arr_delay, "delayDeparture": dep_delay,
        })

    features = extract_features({"trainNumber": live["trainNumber"], "train": {"type": train_type}, "route": route})
    by_code = {row["station_code"]: row for row in rows}
    sequences = metadata["station_sequences"][str(live["trainNumber"])]
    for feature in features.to_dict("records"):
        if pd.isna(feature["scheduled_arrival_iso"]):
            feature["scheduled_arrival_iso"] = None
        code = feature["station_code"]
        row = by_code[code]
        if row.get("live_status") != "upcoming" or not row.get("scheduled_arrival"):
            row["prediction_reason"] = "Prediction is only available for an upcoming arrival."
            continue
        index = rows.index(row)
        predecessors = rows[max(0, index - 3):index]
        if len(predecessors) < 3 or any(p["station_code"] not in sequences or p.get("live_status") not in ("passed", "current") for p in predecessors):
            row["prediction_reason"] = "Waiting for observed delays at the preceding three stops."
            continue
        history = ("previous_delay", "previous_departure_delay", "previous_delay2", "previous_delay3", "last_three_delay_avg")
        if any(not math.isfinite(float(feature[key])) for key in history):
            row["prediction_reason"] = "Waiting for observed delays at the preceding three stops."
            continue
        if code in sequences and feature["station_time_difference"] in time_codes:
            feature["seq"] = sequences[code]
            feature["station_time_difference"] = time_codes[feature["station_time_difference"]]
            by_code[code]["model_features"] = feature
            row["prediction_available"] = True
            row["prediction_reason"] = None
