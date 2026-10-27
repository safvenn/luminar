from pathlib import Path

import pandas as pd
import streamlit as st
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


st.set_page_config(
    page_title="Iris Species Predictor",
    page_icon="🌼",
    layout="wide",
)


@st.cache_data
def load_data():
    csv_path = Path(__file__).resolve().parent / "Iris.csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"Could not find Iris.csv at: {csv_path}")

    return pd.read_csv(csv_path)


FEATURE_COLUMNS = [
    "SepalLengthCm",
    "SepalWidthCm",
    "PetalLengthCm",
    "PetalWidthCm",
]


def build_model():
    df = load_data()
    X = df[FEATURE_COLUMNS]
    y = df["Species"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    return model, accuracy


model, accuracy = build_model()


st.title("🌼 Iris Flower Species Prediction")
st.caption("K-Nearest Neighbors model trained from the Iris dataset")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Accuracy", f"{accuracy * 100:.2f}%")
with col2:
    st.metric("Classes", len(model.classes_))
with col3:
    st.metric("Features", len(FEATURE_COLUMNS))
with col4:
    st.metric("Neighbors", model.n_neighbors)

st.divider()

left_col, right_col = st.columns([1.15, 0.85])

with left_col:
    st.subheader("Dataset preview")
    st.dataframe(load_data().head(10), use_container_width=True)

with right_col:
    st.subheader("Flower summary")
    summary = load_data().groupby("Species").agg({
        "SepalLengthCm": "mean",
        "SepalWidthCm": "mean",
        "PetalLengthCm": "mean",
        "PetalWidthCm": "mean",
    }).round(2)
    st.dataframe(summary, use_container_width=True)

st.divider()

st.subheader("Predict species")

inputs = {}
for idx, column in enumerate(FEATURE_COLUMNS):
    min_value = float(load_data()[column].min())
    max_value = float(load_data()[column].max())
    default_value = float(load_data()[column].median())

    if idx % 2 == 0:
        left, right = st.columns(2)
        with left:
            inputs[column] = st.number_input(
                label=column,
                min_value=min_value,
                max_value=max_value,
                value=default_value,
                step=0.1,
            )
    else:
        with right:
            inputs[column] = st.number_input(
                label=column,
                min_value=min_value,
                max_value=max_value,
                value=default_value,
                step=0.1,
            )

if st.button("Predict Species", type="primary"):
    feature_values = [[inputs[column] for column in FEATURE_COLUMNS]]
    prediction = model.predict(feature_values)[0]
    probabilities = model.predict_proba(feature_values)[0]
    class_probabilities = pd.Series(probabilities, index=model.classes_).sort_values(ascending=False)

    st.success(f"Predicted species: {prediction}")
    st.write("Prediction confidence:")
    st.bar_chart(class_probabilities)
