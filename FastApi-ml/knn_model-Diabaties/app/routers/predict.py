from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.schemas.details import Details
from app.schemas.predict_response import PredictResponseModel
from app.services.predict_service import prediction_data
from app.dependencies.ml import get_ml_components


router = APIRouter(prefix="/predict", tags=["Predict"])


@router.post("/", response_model=PredictResponseModel, status_code=200)
def predict(
    details: Details,
    username: str = Depends(get_current_user),
    ml=Depends(get_ml_components),
):
    return prediction_data(details,ml['model'],ml['scaler'])
