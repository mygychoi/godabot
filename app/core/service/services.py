from pydantic import BaseModel, Extra

from app.core.registry import Registry


class Service(BaseModel, Registry):
    class Config:
        frozen = True
        extra = Extra.forbid
