from app.schemas.details import Details
import numpy as np



def predict(features: np.ndarray,model,scaler):
    scaled_features=scaler.transform(features)
    prediction = model.predict(features)
    
    return prediction