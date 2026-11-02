import streamlit as st
import joblib
import pandas as pd

model = joblib.load("C:\\Desktop\\luminar\\Machine Learning\\Trian Time Delay Prediction\\src\\ml\\model.pkl")


model_features = model.feature_names_in_


st.title("Train Delay Prediction")

st.write("Please enter the following information to predict train delay:")

train_no = st.text_input("Train Number (e.g., 16346, 12345):")
station_code = st.text_input("Station Code (e.g., NDLS, BCT, MAS):")
train_type = st.selectbox("Train Type:", ["SUF","MEX" ])
seq = st.number_input("Sequence Number (seq):", min_value=1, step=1)
station_code = station_code.upper()
halts_here = st.selectbox("Halts Here:", [0, 1])
platform = st.number_input("Platform Number:", min_value=1, step=1)
distance_km = st.number_input("Distance (in km):", min_value=0.0, step=1.0)
previous_delay = st.number_input("Previous Delay (in minutes):", min_value=0, step=1)
previous_departure_delay = st.number_input("Previous Departure Delay (in minutes):", min_value=0, step=1)
previous_delay2 = st.number_input("Previous Delay 2 (in minutes):", min_value=0, step=1)
previous_delay3 = st.number_input("Previous Delay 3 (in minutes):", min_value=0, step=1)
previous_distance_diff = st.number_input("Previous Distance (in km):", min_value=0.0, step=1.0)
last_three_delays_avg = st.number_input("Last Three Delays (in minutes):", min_value=0, step=1)
station_time_difference	= st.number_input("Enter last time difference")
is_weekend = st.selectbox("Weekend:",[1,0])
month = st.number_input("Month:", min_value=1, max_value=12, step=1)
sch_arrival = st.number_input("Scheduled Arrival Time (in minutes):", min_value=0, step=1,max_value=23)


df = pd.DataFrame({
    "station_code": [station_code],
    "train_type": [train_type],
    "seq": [seq],
    "halts_here": [halts_here],
    "platform": [platform],
    "distance_km": [distance_km],
    "previous_delay": [previous_delay],
    "previous_departure_delay": [previous_departure_delay],
    "previous_delay2": [previous_delay2],
    "previous_delay3": [previous_delay3],
    "previous_distance_diff": [previous_distance_diff],
    "last_three_delays_avg": [last_three_delays_avg],
    "station_time_difference": [station_time_difference],
    "is_weekend": [is_weekend],
    "month": [month],
    "sch_arrival": [sch_arrival]
}
)
df["train_type"] = df["train_type"].apply(lambda x: 1 if x == "MEX" else 0)

df = pd.get_dummies(df, columns=["station_code"], drop_first=True)

df = df.reindex(columns=model_features, fill_value=0)


prediction = model.predict(df)


if st.button("Predict Delay"):
    st.write(f"Predicted Delay: {prediction[0]} minutes")
