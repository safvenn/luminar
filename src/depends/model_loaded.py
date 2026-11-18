from fastapi import Request


def get_ml_components(request: Request):
    return {
        "model": getattr(request.app.state, "model", None),
        "scaler": getattr(request.app.state, "scaler", None)
    }