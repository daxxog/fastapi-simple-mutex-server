from .mutex_resource import MutexResource


class ReleaseMutexRequest(MutexResource):
    uuid: str
