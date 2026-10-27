from pathlib import Path

import streamlit as st # pyright: ignore[reportMissingImports]
import pandas as pd

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="Diabetes Prediction",
    page_icon="🩺",
    layout="centered"
)


# -----------------------------
# TITLE
# -----------------------------

st.title("🩺 Diabetes Prediction")
st.write("KNN Machine Learning Model")


# -----------------------------
# LOAD DATASET
# -----------------------------

@st.cache_data
def load_data():
    base_dir = Path(__file__).resolve().parent
    candidates = [
        base_dir / "diabetes.csv",
        base_dir / "uploads" / "diabetes.csv",
        base_dir.parent / "uploads" / "diabetes.csv",
    ]

    for path in candidates:
        if path.exists():
            return pd.read_csv(path)

    raise FileNotFoundError(
        "Could not find diabetes.csv. Checked: " + ", ".join(str(p) for p in candidates)
    )


df = load_data()


# -----------------------------
# SPLIT FEATURES
# -----------------------------

x = df.iloc[:, :-1].values
y = df.iloc[:, -1].values


# -----------------------------
# TRAIN TEST SPLIT
# -----------------------------

x_train, x_test, y_train, y_test = train_test_split(
    x,
    y,
    test_size=0.3
)


# -----------------------------
# CREATE MODEL
# -----------------------------

model = KNeighborsClassifier(
    n_neighbors=5
)

model.fit(x_train, y_train)


# -----------------------------
# MODEL ACCURACY
# -----------------------------

y_pred = model.predict(x_test)

accuracy = accuracy_score(y_test, y_pred)


# -----------------------------
# DISPLAY ACCURACY
# -----------------------------

st.metric(
    "Model Accuracy",
    f"{accuracy * 100:.2f}%"
)


st.divider()


# -----------------------------
# USER INPUT
# -----------------------------

st.subheader("Enter Patient Details")


pregnancies = st.number_input(
    "Pregnancies",
    min_value=0,
    max_value=20,
    value=1
)

glucose = st.number_input(
    "Glucose",
    min_value=0,
    max_value=300,
    value=120
)

blood_pressure = st.number_input(
    "Blood Pressure",
    min_value=0,
    max_value=200,
    value=70
)

skin_thickness = st.number_input(
    "Skin Thickness",
    min_value=0,
    max_value=100,
    value=20
)

insulin = st.number_input(
    "Insulin",
    min_value=0,
    max_value=900,
    value=80
)

bmi = st.number_input(
    "BMI",
    min_value=0.0,
    max_value=70.0,
    value=25.0
)

dpf = st.number_input(
    "Diabetes Pedigree Function",
    min_value=0.0,
    max_value=3.0,
    value=0.5
)

age = st.number_input(
    "Age",
    min_value=1,
    max_value=120,
    value=30
)


# -----------------------------
# PREDICTION
# -----------------------------

if st.button("🔍 Predict Diabetes"):

    input_data = [[
        pregnancies,
        glucose,
        blood_pressure,
        skin_thickness,
        insulin,
        bmi,
        dpf,
        age
    ]]

    prediction = model.predict(input_data) # pyright: ignore[reportArgumentType]

    st.divider()

    if prediction[0] == 0:
        st.success("✅ NO — Diabetes is not predicted.")
    else:
        st.error("⚠️ YES — Diabetes is predicted.")