from pydantic import BaseModel


class MutexResource(BaseModel):
    resource_name: str
