from typing import Optional
from .mutex_resource import MutexResource


class ObtainMutexRequest(MutexResource):
    ttl: Optional[int] = None
