from pydantic import BaseModel


class ReleaseMutexResponse(BaseModel):
    released: bool
