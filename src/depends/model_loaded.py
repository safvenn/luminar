from fastapi import Request


def get_ml_components(request: Request):
    return {
        "model": request.app.state.model,
        "scaler": request.app.state.scaler
    }