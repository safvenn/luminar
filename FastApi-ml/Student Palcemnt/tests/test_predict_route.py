from app.routers.predict_router import predict
from app.schemas.prediction_input import Prediction_input


def test_predict_returns_binary_label_for_valid_sample():
    payload = {
        "Age": 22,
        "Gender": "Male",
        "University_Year": "Sophomore",
        "Major": "Computer Science",
        "Attendance_Percentage": 86,
        "Study_Hours_Per_Week": 21,
        "CGPA": 3.28,
        "Academic_Performance": "Good",
        "Programming_Skill": 9,
        "Projects_Completed": 10,
        "Certifications": 1,
        "Hackathons": 6,
        "GitHub_Profile": "Yes",
        "Internships": 5,
        "Leadership_Experience": "No",
        "LinkedIn_Profile": "No",
        "Resume_Score": 100,
        "Communication_Skills": 9,
        "Teamwork": 7,
        "Problem_Solving": 8,
        "English_Proficiency": "Advanced",
        "Interview_Score": 72,
        "Employability_Score": 231.7,
    }

    result = predict(Prediction_input(**payload))

    assert set(result.keys()) == {"result"}
    assert result["result"] in {0, 1}
