from typing import Any
from fastapi import HTTPException
from app.ml.model_selector import model_predict
from app.schemas.prediction_input import Prediction_input
from app.repository.predict_repository import (
    academic_performance_encoder,
    english_proficiency_encoder,
    gender_encoder,
    github_profile_encoder,
    leadership_experience_encoder,
    linkedin_profile_encoder,
    major_encoder,
    university_year_encoder,
)
def _encode(encoder: Any, value: Any) -> int:
    return int(encoder.transform([value])[0])


def predict_services(data:Prediction_input,model,scaler):
        features = [[
        data.Age, 
        _encode(gender_encoder, data.Gender),
        _encode(university_year_encoder, data.University_Year),
        _encode(major_encoder, data.Major),
        data.Attendance_Percentage, 
        data.Study_Hours_Per_Week, 
        data.CGPA, 
        _encode(academic_performance_encoder, data.Academic_Performance),
        data.Programming_Skill, 
        data.Projects_Completed, 
        data.Certifications, 
        data.Hackathons, 
        _encode(github_profile_encoder, data.GitHub_Profile),
        data.Internships, 
        _encode(leadership_experience_encoder, data.Leadership_Experience),
        _encode(linkedin_profile_encoder, data.LinkedIn_Profile),
        data.Resume_Score, 
        data.Communication_Skills, 
        data.Teamwork, 
        data.Problem_Solving, 
        _encode(english_proficiency_encoder, data.English_Proficiency),
        data.Interview_Score, 
        data.Employability_Score]]
        
        
        
        return model_predict(features,scaler,model) # pyright: ignore[reportArgumentType]