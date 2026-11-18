"""Prepare model inputs from completed live stops and the timetable."""
import json
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
    updated = pd.Timestamp(live["updatedAt"]).tz_convert("Asia/Kolkata")
    first = live["stops"][0]
    journey_date = date_near(first["date"], updated) - pd.Timedelta(days=int(first["day"]) - 1)
    route = []
    observed_count = 0

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
            if row.get("live_delay_min") is not None:
                arr_delay = float(row["live_delay_min"])
                dep_delay = float(row["live_delay_min"])
                observed_count += 1
            elif row.get("live_date"):
                actual_date = date_near(row["live_date"], arrival or departure)
                actual_arrival = actual_date + pd.Timedelta(row["live_arrival"] + ":00") if row.get("live_arrival") else None
                actual_departure = actual_date + pd.Timedelta(row["live_departure"] + ":00") if row.get("live_departure") else None
                if actual_arrival is not None and actual_departure is not None and actual_departure < actual_arrival:
                    actual_departure += pd.Timedelta(days=1)
                if arrival is not None and actual_arrival is not None:
                    arr_delay = (actual_arrival - arrival).total_seconds() / 60
                    observed_count += 1
                if departure is not None and actual_departure is not None:
                    dep_delay = (actual_departure - departure).total_seconds() / 60

        # Do not repeat delays across missing or upcoming stops.
        route.append({
            "stationCode": row["station_code"], "sequence": row["seq"],
            "distance": row["distance_km"], "haltsHere": 1, "platform": 1,
            "scheduledArrival": arrival.isoformat() if arrival is not None else None,
            "scheduledDeparture": departure.isoformat() if departure is not None else None,
            "delayArrival": arr_delay, "delayDeparture": dep_delay,
        })
    if not observed_count:
        raise ValueError("No completed stops with observed arrival times are available yet")
    features = extract_features({"trainNumber": live["trainNumber"], "train": {"type": train_type}, "route": route})
    by_code = {row["station_code"]: row for row in rows}
    sequences = metadata["station_sequences"][str(live["trainNumber"])]
    for feature in features.to_dict("records"):
        if pd.isna(feature["scheduled_arrival_iso"]):
            feature["scheduled_arrival_iso"] = None
        code = feature["station_code"]
        if code in sequences and feature["station_time_difference"] in time_codes:
            feature["seq"] = sequences[code]
            feature["station_time_difference"] = time_codes[feature["station_time_difference"]]
            by_code[code]["model_features"] = feature
