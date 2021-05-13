from pydantic import (
    BaseModel,
    create_model
)
from fastapi import HTTPException


_model_cache = {}


class HTTPExceptionModel(BaseModel):
    detail: str


def exception_responses(*http_exceptions) -> dict:
    """
    wrapper for "reponses=" in FastAPI decorator methods
    allows automatic generation of Swagger documentation for HTTPException instances
    """

    global _model_cache
    _reponses = {}

    for _http_exception in http_exceptions:
        if callable(_http_exception):
            http_exception: HTTPException = _http_exception()
        else:
            http_exception: HTTPException = _http_exception

        if hasattr(_http_exception, '__name__') and type(_http_exception.__name__) == str:
            http_exception_name = _http_exception.__name__\
            .replace("HTTP", "")\
            .replace("Exception", "Error")\
            .replace("<lambda>", "Error")
        else:
            http_exception_name = "Error"

        _reponses[http_exception.status_code] = {}
        model_name = f"HTTP{http_exception.status_code}{http_exception_name}" # magic dynamic model name
        if model_name not in _model_cache:
            _model_cache[model_name] = create_model(
                model_name,
                __base__=HTTPExceptionModel,
                Config=type('Config', (), { # dynamic "Config" class for FastAPI / Swagger example detail
                    "schema_extra": {
                        "example": {
                            "detail": http_exception.detail
                        }
                    }
                })
            )
        _reponses[http_exception.status_code]["model"] = _model_cache[model_name]
        _reponses[http_exception.status_code]["description"] = http_exception.detail

    return _reponses
