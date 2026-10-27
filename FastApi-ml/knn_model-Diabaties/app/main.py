from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import os
import joblib
from app.routers.predict import router as predict_router

#lifespan
from contextlib import asynccontextmanager

from app.routers.verify import router as protected_route

@asynccontextmanager
async def lifespan(app:FastAPI):
    app.state.model = joblib.load("models/model.pkl")
    app.state.scaler = joblib.load(
        "models/scaler.pkl"
    )
    
    print("Model Loaded - main.py:20")
    
    yield
    
    print("Application shutdown - main.py:24")


app = FastAPI(title="Diabetes Prediction API",lifespan=lifespan)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_router)

app.include_router(protected_route)


@app.get("/", response_class=HTMLResponse,tags=["HTML Frontend"])
def home():
    index_path = os.path.join(os.path.dirname(__file__), "..", "index.html")
    index_path = os.path.abspath(index_path)

    if not os.path.exists(index_path):
        return HTMLResponse(content="<h1>index.html not found</h1>")

    with open(index_path, "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())