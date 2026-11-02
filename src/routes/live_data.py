from fastapi import APIRouter, HTTPException
import requests
from src.depends.db import reports
from src.services.live_prediction import add_prediction_features
from src.services.timetable_services import load_timetable
from dotenv import dotenv_values
from pathlib import Path
import os
import re
from uuid import uuid4
from time import time
from typing import Literal





router = APIRouter(tags=['live data'])



ENV_PATH = Path(__file__).resolve().parents[1] / ".env"


def get_api_key():
    # Read the local configuration on each request so edits do not leave a
    # stale module-level credential in the running server.
    key = (dotenv_values(ENV_PATH).get("API_KEY")
           or dotenv_values(ENV_PATH.parent.parent / ".env").get("API_KEY")
           or os.getenv("API_KEY"))
    key = (key or "").strip()
    if not key:
        raise HTTPException(status_code=503, detail="IRCTC API key is missing. Set API_KEY in the project-root .env or src/.env.")
    return key


TRAIN_OPTIONS = Literal['12625', '16306', '16346', '16325']


def fetch_train_data(train_no, endpoint, date=None):
    api_key = get_api_key()
    url = f"https://api.irctc.dev/api/v1/{endpoint}/{train_no}"
    params = {}
    if date and str(date).strip() and str(date).strip().lower() != "none":
        if hasattr(date, "strftime"):
            params["date"] = date.strftime("%Y-%m-%d")
        else:
            params["date"] = str(date).strip()

    try:
        response = requests.get(
            url,
            headers={
                "Authorization": f"Bearer {api_key}"
            },
            params=params if params else None,
            timeout=20
        )
        response.raise_for_status()
    except requests.Timeout:
        raise HTTPException(status_code=504, detail="IRCTC API timed out. Please try again.") from None
    except requests.HTTPError as error:
        status = error.response.status_code if error.response is not None else 502
        details = {
            401: "IRCTC API rejected the API key. Update API_KEY in src/.env with a valid key.",
            403: "IRCTC API denied access. Check your API key permissions and plan.",
            404: "IRCTC API could not find this train's data.",
            429: "IRCTC API request quota reached. Please try again later or check your plan.",
        }
        raise HTTPException(status_code=status if status in details else 502,
                            detail=details.get(status, "IRCTC API is temporarily unavailable. Please try again.")) from None
    except requests.RequestException:
        raise HTTPException(status_code=502, detail="Unable to connect to IRCTC API. Please try again.") from None

    try:
        payload = response.json()
        data = payload["data"]
        if payload.get("success") is False or not isinstance(data, dict):
            raise ValueError("Invalid response")
        return data
    except (ValueError, KeyError, TypeError):
        raise HTTPException(status_code=502, detail=f"IRCTC API returned invalid {endpoint} data.") from None


def match_station_stop(row, live_stops, used_indices):
    """Match unique station identities; distances alone cannot establish identity."""
    def clean(value):
        value = re.sub(r"\b(junction|jn|jnction)\b", "", str(value or "").lower())
        return re.sub(r"[^a-z0-9]", "", value)

    code = str(row.get("station_code") or "").strip().upper()
    aliases = {
        "TVC": ["trivandrum cntl", "trivandrum central", "thiruvananthapuram central"],
        "ALLP": ["alleppey", "alappuzha"],
        "CNO": ["cancona", "canacona"],
        "SGR": ["sangmeshwar", "sangameshwar", "sangameshwar road"],
        "VARD": ["vaikom", "vaikom road", "vaikam road"],
        "RDM": ["ramagundam", "ramgundam"],
        "VGLJ": ["v lakshmibai jhansi jhs", "virangana lakshmibai", "virangana lakshmibai jhansi", "jhansi"],
        "NZM": ["hazrat nizamuddin", "h nizamuddin"],
        "IPL": ["idapalli", "idaplli", "edappally"],
        "TRTR": ["tripunittura", "triupunittura", "tripunithura"],
        "VAK": ["varkalasivagiri"],
        "CGY": ["changanaseri"],
        "SKZR": ["sirpur kagazngr"],
        "MGK": ["mulagunnathukvu"],
        "KPY": ["karunagapalli"],
        "HAD": ["harippad"],
        "MAJN": ["mangaluru jn"],
        "BYNR": ["mookambika road"],
        "LTT": ["lokmanyatilak t"],
        "VPZ": ["vallapuzha", "vailapuzha"],
        "VTK": ["vallathol nagar", "vallattolnagar"],
    }
    names = {clean(row.get("station_name")), *(clean(n) for n in aliases.get(code, []))} - {""}
    explicit, named = [], []
    for i, stop in enumerate(live_stops):
        if i in used_indices:
            continue
        live_code = str(stop.get("stationCode") or stop.get("code") or "").strip().upper()
        if live_code:
            if live_code == code:
                explicit.append((i, stop))
            continue
        if clean(stop.get("stationName")) in names:
            named.append((i, stop))
    matches = explicit or named
    return matches[0] if len(matches) == 1 else (None, None)


@router.get("/live")
def live_data(train_no: TRAIN_OPTIONS = '16346', date: str | None = None):
    live = fetch_train_data(train_no, "live", date=date)
    if str(live.get("trainNumber")) != train_no or not isinstance(live.get("stops"), list):
        raise HTTPException(status_code=502, detail="IRCTC API returned invalid live-status data.")
    if any(not isinstance(stop, dict) for stop in live["stops"]):
        raise HTTPException(status_code=502, detail="IRCTC API returned invalid live stops.")

    timetable = load_timetable(train_no)
    rows = timetable["data"]

    # Match unique station identities, including verified spelling aliases.
    used_indices = set()
    for row in rows:
        if not row["current_route"]:
            continue
        idx, stop = match_station_stop(row, live["stops"], used_indices)
        if stop is not None:
            used_indices.add(idx)
            row["live_arrival"] = stop.get("arrives")
            row["live_departure"] = stop.get("departs")
            row["live_delay_min"] = stop.get("delayMin")
            row["live_status"] = stop.get("status")
            row["live_date"] = stop.get("date")

    prediction_message = "Missing previous delays use 0 minutes. Future API estimates are not used as observations."
    try:
        active_rows = [row for row in rows if row["current_route"] and row["schedule_available"]]
        add_prediction_features(active_rows, live, timetable["train_type"], journey_date=date)
        for row in rows:
            if not row["current_route"]:
                row["prediction_available"] = False
                row["prediction_reason"] = "Historical station entry; not on the current scraped route."
            elif not row["schedule_available"]:
                row["prediction_available"] = False
                row["prediction_reason"] = "Fixed schedule is unavailable for this station."
    except (ValueError, TypeError, KeyError, IndexError) as error:
        for row in rows:
            row.pop("model_features", None)
            row["prediction_available"] = False
            row["prediction_reason"] = "Live inputs are incomplete or invalid. Refresh your train."
        prediction_message = f"Prediction unavailable: {error}"
    prediction_available = any("model_features" in row for row in rows)
    if not prediction_available:
        prediction_message = "No upcoming station has supported schedule inputs."

    current_location = live.get("currentLocation")
    current = next((row for row in rows if row.get("live_status") == "current"), None)
    if current:
        current_location = {"stationCode": current["station_code"],
                            "sequence": current["seq"],
                            "name": live.get("currentLocation"),
                            "status": live.get("locationStatus")}

    journey_date = (date.strip() if date and str(date).strip() and str(date).strip().lower() != "none"
                    else (live["stops"][0].get("date") if live.get("stops") else None))

    report = {
        "report_id": uuid4().hex,
        "created_at": time(),
        "train_no": train_no,
        "train_name": timetable["train_name"],
        "timetable_updated_at": timetable["timetable_updated_at"],
        "timetable_source": timetable["timetable_source"],
        "journey_date": journey_date,
        "current_delay": live.get("currentDelayMin"),
        "current_location": current_location,
        "last_updated": live.get("lastUpdated"),
        "live_stops": live["stops"],
        "total_stations": len(rows),
        "data": rows,
        "prediction_available": prediction_available,
        "prediction_message": prediction_message,
    }
    reports.append(report)
    del reports[:-100]
    # Keep model inputs on the server; the frontend only needs display fields.
    return {**report, "data": [
        {key: value for key, value in row.items() if key != "model_features"}
        for row in rows
    ]}


@router.get("/timetable")
def timetable(train_no: TRAIN_OPTIONS = "16346"):
    return load_timetable(train_no)
