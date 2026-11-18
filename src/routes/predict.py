from fastapi import APIRouter, Request
from src.services.predict_services import predict_services

router = APIRouter(tags=["Predict"])


@router.api_route("/predict", methods=["GET", "POST"])
def predict(
    station_code: str,
    request: Request,
    train_no: str | None = None,
    report_id: str | None = None,
):
    return predict_services(
        station_code=station_code,
        model=request.app.state.model,
        train_no=train_no,
        report_id=report_id,
    )
