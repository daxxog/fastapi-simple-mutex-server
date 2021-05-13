from fastapi import FastAPI

from .config import (
    service_config,
    APP_VERSION
)
from .routes import router


app = FastAPI(
    title=service_config.service_name,
    version=APP_VERSION
)


app.include_router(router)
