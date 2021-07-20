from starlette.status import HTTP_403_FORBIDDEN
from fastapi import HTTPException
from fastapi import Security
from fastapi.security.api_key import APIKeyQuery

from fastapi_simple_mutex_server.config import service_config
from secrets import compare_digest as secure_strings_same

NotAuthenticated403 = lambda: HTTPException(
    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
)


class APIKeySecurity:
    def __init__(self, api_key: str = Security(APIKeyQuery(name='api_key'))):
        if not secure_strings_same(api_key, service_config.api_key):
            raise NotAuthenticated403()
