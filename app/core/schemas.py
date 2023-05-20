from pydantic import BaseModel

from .registry import Registry


class Schema(Registry, BaseModel):
    class Config:
        frozen = True
