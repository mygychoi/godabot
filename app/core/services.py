from pydantic import BaseModel, Extra

from .registry import Registry


class Service(BaseModel, Registry):
    class Config:
        frozen = True
        extra = Extra.ignore
