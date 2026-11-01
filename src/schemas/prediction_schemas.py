from typing import Optional, List, Union
from pydantic import BaseModel, Field


class Prediction_schema(BaseModel):
    train_no: str = Field(..., description="Train number", examples=[16346])
    train_type: str = Field(default="MEX", description="Train type code", examples=["MEX"])
    seq: str = Field(..., description="Sequence number of the station stop", examples=[1])
    station_code: str = Field(..., description="Station IR code", examples=["TVC"])
    scheduled_arrival: Optional[str] = Field(default=None, description="Scheduled arrival time (HH:MM:SS)", examples=["09:15:00"])
    platform: float = Field(default=1.0, description="Platform number", examples=[4.0])
    distance_km: float = Field(default=0.0, description="Distance from origin in km", examples=[0.0])
    previous_delay: float = Field(default=0.0, description="Previous station arrival delay in minutes", examples=[0.0])
    previous_distance_diff: float = Field(default=0.0, description="Distance diff from previous station", examples=[0.0])
    previous_arrival_delay: float = Field(default=0.0, description="Departure delay at previous station", examples=[0.0])
    last_three_delay_avg: float = Field(default=0.0, description="Average departure delay over last 3 stations", examples=[0.0])
    previous_arrival_delay2: float = Field(default=0.0, description="Departure delay 2 stations ago", examples=[0.0])
    previous_arrival_delay3: float = Field(default=0.0, description="Departure delay 3 stations ago", examples=[0.0])
    weekend: str = Field(default="Mon", description="Day of week (Mon, Tue, Wed, Thu, Fri, Sat, Sun)", examples=["Thu"])
    month: int = Field(default=10, ge=1, le=12, description="Month of arrival (1-12)", examples=[10])
    sch_arrival_hour: int = Field(default=9, ge=0, le=23, description="Scheduled arrival hour (0-23)", examples=[9])
    Time: str = Field(default="morning", description="Time category (morning, noon, evening, night)", examples=["morning"])


# Alias for PEP8 PascalCase naming convention
PredictionSchema = Prediction_schema


class BatchPredictionSchema(BaseModel):
    stations: List[Prediction_schema]


class PredictionResponse(BaseModel):
    train_no: Optional[Union[int, str]] = None
    station_code: Optional[str] = None
    
    predicted_delay_arrival_min: float
