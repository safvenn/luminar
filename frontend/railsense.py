from calendar import month_name
import json
import math
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


st.set_page_config(page_title="RailSense | Arrival forecast", page_icon="🚆", layout="wide")

MODEL_PATH = Path(__file__).resolve().parent.parent / "src" / "ml" / "model.pkl"
TRAIN_CODES = {"12625": 0, "16306": 1, "16325": 2, "16346": 3}
PREPROCESSING = json.loads(MODEL_PATH.with_name("preprocessing.json").read_text(encoding="utf-8"))
TIME_CODES = {value: index for index, value in enumerate(PREPROCESSING["time_classes"])}


@st.cache_resource
def load_model(path):
    return joblib.load(path)


st.caption("RAILSENSE   /   JOURNEY INTELLIGENCE")
st.title(":material/train: Every journey, a clearer arrival.")
st.write("Turn your latest journey details into an estimated arrival delay.")
st.divider()

form_column, result_column = st.columns([2.2, 1], gap="large")

with form_column:
    # Outside the form so changing trains refreshes its station choices immediately.
    train_no = st.selectbox("Train number", list(TRAIN_CODES))
    station_sequences = PREPROCESSING["station_sequences"][train_no]
    with st.form("prediction_form"):
        st.subheader("Journey details", icon=":material/route:")
        st.caption("01 / Identify your train and the station you're predicting for.")
        c1, c2 = st.columns(2)
        with c1:
            station_code = st.selectbox(
                "Station code", sorted(station_sequences, key=station_sequences.get),
                key=f"station_{train_no}",
            )
            seq = station_sequences[station_code]
        with c2:
            train_type = st.selectbox("Train type", ["SUF", "MEX"])
            platform = st.number_input("Platform number", min_value=1, step=1)
            halts_here = st.selectbox("Scheduled halt", ["Yes", "No"])

        st.divider()
        st.subheader("Recent running history", icon=":material/history:")
        st.caption("02 / Enter recorded delays in minutes.")
        c1, c2 = st.columns(2)
        with c1:
            previous_delay = st.number_input("Previous arrival delay", min_value=0, step=1)
            previous_delay2 = st.number_input("Arrival delay · 2 stops ago", min_value=0, step=1)
        with c2:
            previous_departure_delay = st.number_input("Previous departure delay", min_value=0, step=1)
            previous_delay3 = st.number_input("Arrival delay · 3 stops ago", min_value=0, step=1)

        st.divider()
        st.subheader("Schedule & distance", icon=":material/calendar_month:")
        st.caption("03 / Add the remaining context for your forecast.")
        c1, c2 = st.columns(2)
        with c1:
            distance_km = st.number_input("Distance (km)", min_value=0.0, step=1.0)
            previous_distance_diff = st.number_input("Previous distance (km)", min_value=0.0, step=1.0)
            station_time_difference = st.number_input(
                "Minutes since previous scheduled departure", min_value=0, value=30, step=1,
                help="Scheduled travel time from the previous station to this station, in minutes.",
            )
        with c2:
            sch_arrival_hour = st.selectbox("Scheduled arrival hour", range(24), format_func=lambda h: f"{h:02d}:00")
            month = st.selectbox("Month", range(1, 13), format_func=lambda m: month_name[m])
            is_weekend = st.selectbox("Weekend journey", ["No", "Yes"])

        st.divider()
        submitted = st.form_submit_button("Predict arrival delay", icon=":material/arrow_forward:", type="primary", width="stretch")

if submitted:
    st.session_state.pop("forecast", None)
    if not station_code:
        with result_column:
            st.warning("Enter a station code to generate your forecast.")
    else:
        try:
            with st.spinner("Calculating your arrival forecast…"):
                time_category = str(float(station_time_difference))
                if time_category not in TIME_CODES:
                    raise ValueError("This scheduled travel time was not seen during training; a forecast is unavailable.")
                model = load_model(MODEL_PATH)
                model_features = model.feature_names_in_
                average = (previous_delay + previous_delay2 + previous_delay3) / 3
                row = {
                    "train_no": TRAIN_CODES[train_no],
                    "station_code": station_code,
                    "train_type": int(train_type == "SUF"),
                    "seq": seq,
                    "halts_here": int(halts_here == "Yes"),
                    "platform": platform,
                    "distance_km": distance_km,
                    "previous_delay": previous_delay,
                    "previous_departure_delay": previous_departure_delay,
                    "previous_delay2": previous_delay2,
                    "previous_delay3": previous_delay3,
                    "previous_distance_diff": previous_distance_diff,
                    "last_three_delay_avg": average,
                    "station_time_difference": TIME_CODES[time_category],
                    "is_weekend": int(is_weekend == "Yes"),
                    "month": month,
                    "sch_arrival_hour": sch_arrival_hour,
                }
                frame = pd.get_dummies(pd.DataFrame([row]), columns=["station_code"], dtype=int)
                # AAM is the training drop_first baseline and correctly has no dummy column.
                missing = [name for name in model_features if name not in frame and not name.startswith("station_code_")]
                if missing:
                    raise ValueError(f"Required model inputs are missing: {missing}")
                frame = frame.reindex(columns=model_features, fill_value=0)
                if not all(math.isfinite(float(value)) for value in frame.iloc[0]):
                    raise ValueError("All forecast inputs must be finite numbers.")
                delay = float(model.predict(frame)[0])
                if not math.isfinite(delay):
                    raise ValueError("The model returned an invalid forecast.")
                st.session_state.forecast = {
                    "delay": delay, "train": train_no, "station": station_code,
                    "average": average, "previous": previous_delay,
                }
        except FileNotFoundError:
            with result_column:
                st.error("Model file not found. Check MODEL_PATH in railsense.py.")
        except Exception as exc:
            with result_column:
                st.error("The forecast could not be calculated.")
                with st.expander("Error details"):
                    st.code(str(exc))

with result_column:
    with st.container(border=True):
        st.caption("ARRIVAL FORECAST")
        result = st.session_state.get("forecast")
        if result:
            st.subheader(f"Train {result['train']}")
            st.caption(f"Arrival at {result['station']}")
            st.metric("Predicted arrival delay", f"{result['delay']:.1f} min")
            st.divider()
            st.metric("Previous arrival delay", f"{result['previous']} min")
            st.metric("Last 3 stops · average delay", f"{result['average']:.1f} min")
            st.success("Forecast ready", icon=":material/check_circle:")
            st.caption("Based on your last submitted journey details. Estimates may differ from actual arrivals.")
        else:
            st.subheader("Your next arrival, estimated.")
            st.metric("Predicted arrival delay", "— min")
            st.info("Complete the journey details and select Predict arrival delay.", icon=":material/info:")
    with st.expander("A better forecast starts with good inputs", expanded=True):
        st.write("Use the station code from your journey record and the latest recorded arrival and departure delays.")
        st.caption("Update your details and submit again whenever your journey changes.")

st.divider()
st.caption("RAILSENSE  ·  Arrival estimates powered by your trained prediction model")
