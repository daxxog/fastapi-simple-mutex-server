from fastapi import APIRouter, Depends
from fastapi_simple_mutex_server.models import (
    ObtainMutexRequest,
    ObtainMutexResponse,
    ReleaseMutexResponse,
    ReleaseMutexRequest
)

from fastapi_simple_mutex_server.deps import Mutex
from fastapi_simple_mutex_server.deps.security import NotAuthenticated403
from fastapi_simple_mutex_server.utils.fastapi import exception_responses


router = APIRouter()


@router.get('',
    response_model=ObtainMutexResponse,
    responses=exception_responses(NotAuthenticated403)
)
async def obtain_a_mutex(
    request: ObtainMutexRequest = Depends(ObtainMutexRequest),
    mutex: Mutex = Depends(Mutex)
):
    """
    Obtains a mutex lock on a named resource.
    Requires authentication.
    """

    return await mutex.obtain(request)


@router.delete('',
    response_model=ReleaseMutexResponse,
    responses=exception_responses(NotAuthenticated403)
)
async def release_a_held_mutex(
    request: ReleaseMutexRequest = Depends(ReleaseMutexRequest),
    mutex: Mutex = Depends(Mutex)
):
    """
    Releases a mutex lock on a named resource.
    Requires authentication.
    """

    return await mutex.release(request)
