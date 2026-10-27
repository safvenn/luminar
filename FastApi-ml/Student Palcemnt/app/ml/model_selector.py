import numpy as np


def model_predict(features: np.ndarray, scaler, model):
    scaled_features = scaler.transform(features)
    prediction = model.predict(scaled_features)

    return {"result": int(prediction[0])}