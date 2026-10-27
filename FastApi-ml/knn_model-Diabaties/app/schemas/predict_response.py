from pydantic import BaseModel

class PredictResponseModel(BaseModel):
    prediction: int