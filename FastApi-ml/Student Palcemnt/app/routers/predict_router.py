from fastapi import APIRouter, Depends,Security
from app.dependencies.auth import verify_auth
from app.schemas.prediction_input import Model_input, Prediction_input,Predict_response
from app.services.model_loader import _encode, predict_services
from app.dependencies.ml_components import get_ml_components

router = APIRouter()





@router.post("/predict",response_model=Predict_response)
def predict(data:Prediction_input,model:Model_input,ml = Depends(get_ml_components),auth =Security(verify_auth)):
    return predict_services(data,ml[model],ml['scaler'])

    

