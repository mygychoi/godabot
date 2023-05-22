from pydantic import BaseModel

from .registry import Registry


class Schema(BaseModel, Registry):
    class Config:
        frozen = True
