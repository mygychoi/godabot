from pydantic import BaseModel, Extra

from .registry import Registry


class Client(BaseModel, Registry):
    class Config:
        frozen = True
        extra = Extra.forbid
        arbitrary_types_allowed = True
