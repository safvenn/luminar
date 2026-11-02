"""Read the fixed station data saved by scripts/scrape_timetables.py."""
import json
from pathlib import Path

TIMETABLE_FILE = Path(__file__).resolve().parents[1] / "data" / "train_timetables.json"


def load_timetable(train_no):
    data = json.loads(TIMETABLE_FILE.read_text(encoding="utf-8"))
    train = data["trains"][str(train_no)]
    rows = []
    for station in train["stations"]:
        if not station["training_station"]:
            continue
        rows.append({
            "train_no": str(train_no),
            "train_type": "SUF" if str(train_no) == "12625" else "MEX",
            "station_code": station["code"],
            "station_name": station["name"],
            "seq": station["seq"],
            "current_route": station["current_route"],
            "previous_station_code": station.get("previous_station_code"),
            "distance_km": station["distance_km"],
            "previous_distance_diff": station.get("distance_from_previous_km"),
            "station_time_difference": station.get("minutes_from_previous_station"),
            "halts_here": station.get("halts_here", 1),
            "scheduled_arrival": station.get("arrival"),
            "scheduled_departure": station.get("departure"),
            "arrival_day_offset": station.get("arrival_day_offset"),
            "departure_day_offset": station.get("departure_day_offset"),
            "schedule_source": station.get("schedule_source", "public_html"),
            "schedule_available": station.get("available", True),
        })
    return {
        "train_no": str(train_no),
        "train_name": train["train_name"],
        "train_type": "SUF" if str(train_no) == "12625" else "MEX",
        "timetable_updated_at": data["scraped_at"],
        "timetable_source": train["source_url"],
        "total_stations": len(rows),
        "data": rows,
    }
