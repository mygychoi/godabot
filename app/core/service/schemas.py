from pydantic import BaseModel

from app.core.registry import Registry


class Schema(BaseModel, Registry):
    class Config:
        frozen = True
