from contextlib import asynccontextmanager
from pathlib import Path

import joblib
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.routes.live_data import router as live_router
from src.services.predict_services import predict_services

PROJECT_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = PROJECT_DIR / "frontend"


@asynccontextmanager
async def lifespan(app: FastAPI):
    model_path = Path(__file__).resolve().parent / "ml" / "model.pkl"
    if not model_path.exists():
        model_path = PROJECT_DIR / "model.pkl"
    app.state.model = joblib.load(model_path)
    print(f"Model loaded from {model_path}")
    yield
    print("App shutdown")


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(live_router)


@app.api_route("/predict", methods=["GET", "POST"], tags=["Predict"])
def predict(
    station_code: str,
    request: Request,
    train_no: str | None = None,
    report_id: str | None = None,
):
    # The existing service expects the model itself and returns the result.
    return predict_services(
        station_code=station_code,
        model=request.app.state.model,
        train_no=train_no,
        report_id=report_id,
    )


@app.get("/", response_class=FileResponse, tags=["HTML Frontend"])
def home():
    return FileResponse(FRONTEND_DIR / "index.html", media_type="text/html")


app.mount("/assets", StaticFiles(directory=FRONTEND_DIR), name="frontend-assets")
