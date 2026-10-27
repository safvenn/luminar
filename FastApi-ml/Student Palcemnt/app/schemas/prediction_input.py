from pydantic import BaseModel
from typing import Literal
from enum import Enum

class Prediction_input(BaseModel):
    Age : int
    Gender: Literal["Female", "Male", "Other"]
    University_Year : Literal["Freshman", "Junior", "Senior", "Sophomore"]
    Major: Literal[
        "Artificial Intelligence",
        "Business Analytics",
        "Computer Science",
        "Cybersecurity",
        "Data Science",
        "Electrical Engineering",
        "Information Technology",
        "Software Engineering",
    ]
    Attendance_Percentage : int
    Study_Hours_Per_Week : int
    CGPA: float
    Academic_Performance: Literal["Average", "Excellent", "Good", "Poor"]
    Programming_Skill: int
    Projects_Completed: int
    Certifications: int
    Hackathons: int
    GitHub_Profile: Literal["No", "Yes"]
    Internships: int
    Leadership_Experience: Literal["No", "Yes"]
    LinkedIn_Profile: Literal["No", "Yes"]
    Resume_Score: int
    Communication_Skills: int
    Teamwork: int
    Problem_Solving: int
    English_Proficiency: Literal["Advanced", "Basic", "Intermediate"]
    Interview_Score: int
    Employability_Score: float


class Predict_response(BaseModel):
    result: int
    
class Model_input(str,Enum):
    knn_model = 'knn_model'
    nb_model = 'nb_model'
