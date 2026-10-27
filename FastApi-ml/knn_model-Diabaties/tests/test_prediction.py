from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)



def test_prediction():
    response = client.post(
        '/predict',
        json={
            "Pregnancies": 2,
            "Glucose": 140,
            "BloodPressure": 80,
            "SkinThickness": 25,
            "Insulin": 100,
            "BMI": 30,
            "DiabetesPedigreeFunction": 0.5,
            "Age": 35
        }
    )
    assert response.status_code == 200