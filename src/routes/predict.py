"""Compatibility router sharing the main API's model and report contract."""
from fastapi import APIRouter, Depends
from src.depends.model_loaded import get_ml_components
from src.services.predict_services import predict_services

router = APIRouter(tags=["Predict"])

@router.post("/predict")
def predict(station_code: str, report_id: str, model=Depends(get_ml_components)):
    return predict_services(station_code=station_code, model=model, report_id=report_id)
