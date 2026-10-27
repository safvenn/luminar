from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import joblib
from app.routers.predict_router import router as predict_router

from contextlib import asynccontextmanager
from pathlib import Path


FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


@asynccontextmanager
async def lifespan(app:FastAPI):
    knn_model = joblib.load(r'C:\Desktop\luminar\FastApi-ml\Student Palcemnt\models\knn_model.pkt')
    nb_model = joblib.load(r'C:\Desktop\luminar\FastApi-ml\Student Palcemnt\models\nb_model.pkt')
    scaler = joblib.load(r'C:\Desktop\luminar\FastApi-ml\Student Palcemnt\models\scaler.pkt')
    app.state.knn_model = knn_model
    app.state.nb_model = nb_model
    app.state.scaler = scaler
    print("Model loaded - main.py:22")
    yield
    print("app Shutdown - main.py:24")
    
app = FastAPI(lifespan=lifespan)


#
@app.get("/", include_in_schema=False)
def home():
    return FileResponse(FRONTEND_DIR / "index.html")
    

app.include_router(predict_router)

app.mount("/assets", StaticFiles(directory=FRONTEND_DIR), name="assets")


