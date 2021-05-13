from typing import Optional

from pydantic import BaseModel


class ObtainMutexResponse(BaseModel):
    obtained: bool
    uuid: Optional[str]
