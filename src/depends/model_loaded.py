from fastapi import Request


def get_ml_components(request: Request):
    return request.app.state.model
