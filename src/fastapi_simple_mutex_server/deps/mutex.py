from typing import Optional
from uuid import uuid4
from functools import cached_property
from fastapi import Depends

from fastapi_simple_mutex_server.models import (
    ObtainMutexRequest,
    ObtainMutexResponse,
    ReleaseMutexResponse,
    ReleaseMutexRequest
)
from fastapi_simple_mutex_server.config import service_config
from .redis import Redis
from .security import APIKeySecurity


class Mutex:
    _uuid: Optional[str] = None

    def __init__(self,
        redis = Depends(Redis),
        security = Depends(APIKeySecurity)
    ):
        self.redis = redis

    @cached_property
    def uuid(self):
        return self._uuid if self._uuid else str(uuid4())

    async def obtain(self, request: ObtainMutexRequest) -> ObtainMutexResponse:
        if await self.redis.setnx(request.resource_name, self.uuid) == 1:
            if request.ttl and request.ttl > 0:
                await self.redis.expire(request.resource_name, request.ttl)
            else:
                await self.redis.expire(request.resource_name, service_config.default_mutex_expire)

            return ObtainMutexResponse(obtained=True, uuid=self.uuid)
        else:
            return ObtainMutexResponse(obtained=False)

    async def release(self, request: ReleaseMutexRequest) -> ReleaseMutexResponse:
        self._uuid = request.uuid

        if not await self.redis.exists(request.resource_name):
            return ReleaseMutexResponse(released=True)
        else:
            if (await self.redis.get(request.resource_name)).decode("utf-8") == self.uuid:
                await self.redis.delete(request.resource_name)
                return ReleaseMutexResponse(released=True)
            else:
                return ReleaseMutexResponse(released=False)
