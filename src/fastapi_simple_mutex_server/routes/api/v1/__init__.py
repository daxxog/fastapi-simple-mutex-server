from fastapi import APIRouter

from .mutex import router as mutex_router


router = APIRouter()

router.include_router(mutex_router, prefix='/mutex', tags=['Mutex Operations'])
