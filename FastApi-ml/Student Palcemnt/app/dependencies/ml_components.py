from fastapi import Request


def get_ml_components(request: Request):
    return {
        "knn_model": request.app.state.knn_model,
        "nb_model": request.app.state.nb_model,
        "scaler": request.app.state.scaler
    }