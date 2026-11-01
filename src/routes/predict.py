import os
from fastapi import APIRouter, Depends
import joblib 
from src.depends.model_loaded import get_ml_components
from src.services.predict_services import predict_services

router = APIRouter(tags=["Predict"])

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "model.pkl")
model = joblib.load(MODEL_PATH)


@router.post("/predict")
def predict(station_code: str, model = Depends(get_ml_components)):
    return predict_services(station_code=station_code, model=model)
