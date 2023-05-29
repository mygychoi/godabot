from pydantic import BaseModel, Extra

from app.core.registry import Registry


class Form(BaseModel, Registry):
    """Interface between ClientService and Client"""

    class Config:
        frozen = True
        extra = Extra.ignore
        arbitrary_types_allowed = True
