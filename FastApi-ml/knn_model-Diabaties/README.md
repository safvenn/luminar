# Diabetes Prediction API

A simple FastAPI project that predicts whether a patient is likely to have diabetes based on medical input values.

This project uses a K-Nearest Neighbors (KNN) classifier trained on the diabetes dataset.

---

## Project Overview

This application provides:

- a FastAPI backend
- a prediction endpoint for diabetes risk
- a request schema using Pydantic validation
- a repository-style dataset loader
- an ML pipeline for preprocessing and prediction
- a simple HTML landing page at the root route

---

## Tech Stack

- Python
- FastAPI
- Pydantic
- scikit-learn
- pandas
- numpy
- Uvicorn

---

## Project Structure

```text
knn_model-Diabaties/
├── app.py
├── index.html
├── README.md
├── requirements.txt
├── uploads/
│   └── diabetes.csv
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── ml_model/
│   │   ├── diabeties_model.py
│   │   ├── inference.py
│   │   └── scaller.py
│   ├── repository/
│   │   └── data_repository.py
│   ├── routers/
│   │   └── predict.py
│   ├── schemas/
│   │   ├── details.py
│   │   └── predict_response.py
│   └── services/
│       └── predict_service.py
```

---

## How the App Works

### 1. Dataset loading
The repository layer reads the diabetes CSV file from the `uploads` folder.

### 2. Preprocessing
The scaler is fitted on the dataset features and used to transform input values before prediction.

### 3. Model training
A KNN model is trained using the processed dataset.

### 4. Prediction API
The API receives patient details, transforms them into the same feature format, and returns:

- `prediction` as an integer
- `accuracy` as a float

---

## API Endpoint

### Predict Diabetes

```http
POST /predict/
```

### Request Body

```json
{
  "Pregnancies": 2,
  "Glucose": 120,
  "BloodPressure": 70,
  "SkinThickness": 20,
  "Insulin": 80,
  "BMI": 25.0,
  "DiabetesPedigreeFunction": 0.5,
  "Age": 30
}
```

### Example Response

```json
{
  "prediction": 0,
  "accuracy": 0.77
}
```

> `prediction = 0` means no diabetes predicted.
>
> `prediction = 1` means diabetes predicted.

---

## Request Schema

The input schema is defined in `app/schemas/details.py`.

Each field is validated and must be non-negative.

---

## Root Route

The application also serves a simple HTML page from the project root.

```http
GET /
```

---

## Setup Instructions

### 1. Create a virtual environment

```bash
python -m venv venv
```

### 2. Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the FastAPI app

```bash
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

---

## Notes

This project is a good learning example for:

- FastAPI routes
- Pydantic validation
- service layer architecture
- ML model integration
- API response modeling

It is still a beginner-to-intermediate level ML API and can be improved further with:

- better model persistence
- environment-based configuration
- custom error handling
- tests
- cleaner deployment setup

---

## Summary

This project demonstrates how to combine FastAPI with a simple machine learning model to create a diabetes prediction API.

It is a practical learning project for understanding how to expose an ML model through an HTTP API in Python.
