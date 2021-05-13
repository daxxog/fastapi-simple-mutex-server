import uvicorn
from fastapi_simple_mutex_server.config import (
    IS_DEV,
    IS_PROD,
    service_config
)


def main():
    if IS_DEV:
        uvicorn.run('fastapi_simple_mutex_server:app', port=service_config.port_number, reload=True)
    elif IS_PROD:
        # use WEB_CONCURRENCY environment variable to configure concurrency workers
        uvicorn.run('fastapi_simple_mutex_server:app', host='0.0.0.0', port=service_config.port_number)
