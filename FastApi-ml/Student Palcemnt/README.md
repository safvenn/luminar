# Student Placement Prediction System

A lightweight full-stack application for predicting whether a student is likely to be placed based on academic, technical, and professional profile attributes. The project combines a FastAPI backend, an ML prediction pipeline, and a light-themed frontend served directly from the API application.

## Overview

The system accepts a structured student profile, validates the input, transforms categorical fields into model-compatible encodings, and runs one of two trained classifiers:

- K-Nearest Neighbors (`knn_model`)
- Naive Bayes (`nb_model`)

The prediction result is binary:

- `1` = student will be placed
- `0` = student will not be placed

## Core Architecture

### Backend

The backend is built with FastAPI and organized inside the `app/` directory:

- `app/main.py` initializes the API, loads the model artifacts, and serves the frontend
- `app/routers/predict_router.py` exposes the prediction endpoint
- `app/schemas/prediction_input.py` defines the request and response models
- `app/dependencies/auth.py` validates the required `X-API-Key` header
- `app/services/model_loader.py` encodes categorical values and prepares the model features
- `app/dependencies/ml_components.py` provides the current model and scaler objects
- `app/ml/model_selector.py` performs the actual model inference
- `app/repository/predict_repository.py` contains the label encoders used for categorical input

### Frontend

The frontend is a clean, light-styled interface served directly by the FastAPI app:

- `frontend/index.html` contains the student form and result section
- `frontend/app.js` handles validation, sample data loading, API requests, and result rendering
- `frontend/styles.css` defines the visual design and layout

### Data and Model Assets

- `models/` contains the trained prediction artifacts and encoders
- `datas/` contains the dataset used during the placement prediction workflow

## Project Structure

```text
Student Palcemnt/
├── app/
│   ├── dependencies/
│   │   ├── auth.py
│   │   └── ml_components.py
│   ├── ml/
│   │   └── model_selector.py
│   ├── repository/
│   │   └── predict_repository.py
│   ├── routers/
│   │   └── predict_router.py
│   ├── schemas/
│   │   └── prediction_input.py
│   ├── services/
│   │   └── model_loader.py
│   └── main.py
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── styles.css
├── models/
│   ├── encoder.pkt
│   ├── knn_model.pkt
│   ├── nb_model.pkt
│   └── scaler.pkt
├── datas/
│   └── student_career_success_dataset.csv
├── requirements.txt
├── README.md
└── .env (or environment variable configuration for API_KEY)
```

## Setup

### Prerequisites

- Python 3.10+
- pip

### Install Dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Configure the API Key

The API requires a valid `X-API-Key` header for requests. Set the expected key in the environment or in a `.env` file:

```env
API_KEY=your_secret_key_here
```

The value is read in `app/dependencies/auth.py`.

### Run the Application

```powershell
uvicorn app.main:app --reload
```

The app runs at:

- Frontend: `http://127.0.0.1:8000/`
- API docs: `http://127.0.0.1:8000/docs`

## API Contract

### Prediction Endpoint

```http
POST /predict?model=knn_model
```

Required headers:

```http
X-API-Key: <your_api_key>
Content-Type: application/json
```

Example response:

```json
{
  "result": 1
}
```

The request body includes the student’s demographic, academic, skill, and profile details. These fields are validated by the schema in `app/schemas/prediction_input.py`.

## Prediction Flow

1. The API receives a validated student profile.
2. Categorical fields are transformed with the stored label encoders.
3. Numeric fields are combined with the encoded values into a model-ready feature vector.
4. The selected model predicts the placement outcome.
5. The backend returns the binary prediction result.

This flow is handled by the service and model-selection layers in `app/services/model_loader.py` and `app/ml/model_selector.py`.

## Notes

- The frontend is served directly by FastAPI, so no separate frontend server is required.
- Model artifacts are currently loaded from local file paths defined in `app/main.py`; if the project is moved to a different system or directory, those paths should be updated.
- The model is designed for binary classification and returns a simple `0` or `1` output.
