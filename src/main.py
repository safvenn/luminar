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
    app.state.model = joblib.load(PROJECT_DIR / "src" / "ml" / "model.pkl")
    print("Model loaded")
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


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}


@app.post("/predict", tags=["Predict"])
def predict(station_code: str, report_id: str, request: Request):
    # The existing service expects the model itself and returns the result.
    return predict_services(station_code=station_code, model=request.app.state.model, report_id=report_id)


@app.get("/", response_class=FileResponse, tags=["HTML Frontend"])
def home():
    return FileResponse(FRONTEND_DIR / "index.html", media_type="text/html")


app.mount("/assets", StaticFiles(directory=FRONTEND_DIR), name="frontend-assets")
