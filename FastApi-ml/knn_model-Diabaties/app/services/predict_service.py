
import numpy as np
from app.ml.predictor import predict
from app.schemas.details import Details






def prediction_data(details: Details,model,scaler):
        features = np.array(
            [[
                details.Pregnancies,
                details.Glucose,
                details.BloodPressure,
                details.SkinThickness,
                details.Insulin,
                details.BMI,
                details.DiabetesPedigreeFunction,
                details.Age,
            ]],
            dtype=float,
        )
        
        prediction = predict(features,model,scaler)

        

        return {
            "prediction": int(prediction[0])
        }



