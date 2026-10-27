from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


st.set_page_config(page_title="Titanic | Survival Lab", page_icon="T", layout="wide")


@st.cache_data
def load_builtin_data() -> pd.DataFrame | None:
    try:
        import seaborn as sns

        return sns.load_dataset("titanic").rename(columns={"survived": "Survived"})
    except Exception:
        return None


def normalize_data(data: pd.DataFrame) -> pd.DataFrame:
    normalized = data.copy()
    aliases = {
        "survived": "Survived",
        "Survival": "Survived",
        "pclass": "Pclass",
        "passenger_class": "Pclass",
        "sex": "Sex",
        "age": "Age",
        "sibsp": "SibSp",
        "parch": "Parch",
        "fare": "Fare",
        "embarked": "Embarked",
    }
    normalized.rename(columns={column: aliases.get(column, column) for column in normalized.columns}, inplace=True)
    return normalized


def make_model(features: pd.DataFrame, neighbors: int) -> Pipeline:
    numeric_columns = features.select_dtypes(include=np.number).columns.tolist()
    categorical_columns = features.select_dtypes(exclude=np.number).columns.tolist()
    numeric_pipeline = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[
            ("numbers", numeric_pipeline, numeric_columns),
            ("categories", categorical_pipeline, categorical_columns),
        ],
        remainder="drop",
    )
    return Pipeline(steps=[("preprocessor", preprocessor), ("classifier", KNeighborsClassifier(n_neighbors=neighbors))])


def train_model(data: pd.DataFrame, target: str, neighbors: int, test_size: float):
    features = data.drop(columns=[target])
    labels = data[target].astype(int)
    x_train, x_test, y_train, y_test = train_test_split(
        features, labels, test_size=test_size, random_state=42, stratify=labels
    )
    model = make_model(features, neighbors)
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    return model, accuracy_score(y_test, predictions), confusion_matrix(y_test, predictions)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Newsreader:opsz,wght@6..72,400;6..72,600;6..72,700&display=swap');
        :root { --ink: #18252b; --sea: #126e77; --coral: #e47455; --paper: #f5f1e8; }
        .stApp { background: radial-gradient(circle at 85% 8%, #dce9e5 0, transparent 28%), var(--paper); color: var(--ink); }
        [data-testid="stSidebar"] { background: #18383b; }
        [data-testid="stSidebar"] * { color: #f5f1e8; }
        h1, h2, h3 { font-family: Newsreader, Georgia, serif !important; letter-spacing: 0 !important; }
        h1 { font-size: clamp(2.8rem, 6vw, 5.5rem) !important; line-height: .92 !important; color: var(--ink); }
        .eyebrow { color: var(--coral); font: 500 .72rem 'DM Mono', monospace; letter-spacing: .12em; text-transform: uppercase; }
        .lede { max-width: 660px; color: #4e5e62; font-size: 1.1rem; line-height: 1.55; }
        div[data-testid="stMetric"] { background: #fffdf7; border: 1px solid #d8d4c9; padding: 1rem; border-radius: 2px; }
        .stButton > button { border-radius: 2px; background: var(--coral); color: white; border: 0; font-weight: 600; }
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_styles()
st.markdown('<div class="eyebrow">A small machine learning observatory</div>', unsafe_allow_html=True)
st.title("Who made it ashore?")
st.markdown(
    '<p class="lede">Explore the passengers of the Titanic, train a K-nearest-neighbors classifier, and test a new passenger profile against the model.</p>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## Data desk")
    uploaded_file = st.file_uploader("Bring a Titanic CSV", type=["csv", "xls", "xlsx"])
    builtin_data = load_builtin_data()
    if uploaded_file is not None:
        try:
            if Path(uploaded_file.name).suffix.lower() == ".csv":
                raw_data = pd.read_csv(uploaded_file)
            else:
                raw_data = pd.read_excel(uploaded_file)
            source_label = uploaded_file.name
        except Exception as error:
            st.error(f"Could not read this file: {error}")
            st.stop()
    elif builtin_data is not None:
        raw_data = builtin_data
        source_label = "seaborn built-in dataset"
        st.caption("Using the built-in Titanic dataset. Upload your own CSV to replace it.")
    else:
        st.warning("Upload a Titanic CSV to begin.")
        st.stop()

    data = normalize_data(raw_data)
    if "Survived" not in data.columns:
        st.error("Your file needs a `Survived` target column.")
        st.stop()
    candidate_features = [
        column for column in ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"] if column in data.columns
    ]
    if not candidate_features:
        st.error("No supported passenger features were found.")
        st.stop()
    selected_features = st.multiselect("Features", candidate_features, default=candidate_features)
    neighbors = st.slider("Neighbors", min_value=1, max_value=15, value=5)
    test_size = st.slider("Test split", min_value=0.1, max_value=0.4, value=0.2, step=0.05)

if not selected_features:
    st.info("Select at least one feature in the sidebar.")
    st.stop()

model_data = data[selected_features + ["Survived"]].dropna(subset=["Survived"])
try:
    model, accuracy, matrix = train_model(model_data, "Survived", neighbors, test_size)
except ValueError as error:
    st.error(f"The model could not be trained: {error}")
    st.stop()

metric_columns = st.columns(4)
metric_columns[0].metric("Passengers", f"{len(data):,}")
metric_columns[1].metric("Survival rate", f"{data['Survived'].mean():.0%}")
metric_columns[2].metric("Model accuracy", f"{accuracy:.1%}")
metric_columns[3].metric("Features", len(selected_features))

st.divider()
explore_tab, predict_tab = st.tabs(["Explore the manifest", "Test a passenger"])

with explore_tab:
    left, right = st.columns([1.15, 0.85])
    with left:
        st.subheader("Passenger manifest")
        st.dataframe(data.head(100), use_container_width=True, hide_index=True)
    with right:
        st.subheader("Observed outcomes")
        outcome_counts = data["Survived"].value_counts().rename(index={0: "Did not survive", 1: "Survived"})
        st.bar_chart(outcome_counts, color="#126e77")
        st.subheader("Confusion matrix")
        st.dataframe(
            pd.DataFrame(matrix, index=["Actual 0", "Actual 1"], columns=["Predicted 0", "Predicted 1"]),
            use_container_width=True,
        )
        st.caption(f"Source: {source_label} | {1 - test_size:.0%}/{test_size:.0%} train/test split")

with predict_tab:
    st.subheader("A new passenger profile")
    st.caption("Fields not used by the current model are omitted automatically.")
    input_values: dict[str, object] = {}
    form_columns = st.columns(2)
    for index, feature in enumerate(selected_features):
        with form_columns[index % 2]:
            if pd.api.types.is_numeric_dtype(data[feature]):
                default_value = float(data[feature].median()) if data[feature].notna().any() else 0.0
                input_values[feature] = st.number_input(feature, value=default_value)
            else:
                options = sorted(data[feature].dropna().astype(str).unique().tolist())
                input_values[feature] = st.selectbox(feature, options or ["Unknown"])

    if st.button("Estimate outcome", type="primary"):
        profile = pd.DataFrame([input_values], columns=selected_features)
        prediction = int(model.predict(profile)[0])
        probability = float(model.predict_proba(profile)[0][prediction])
        if prediction == 1:
            st.success(f"Estimated outcome: survived ({probability:.0%} model confidence)")
        else:
            st.warning(f"Estimated outcome: did not survive ({probability:.0%} model confidence)")