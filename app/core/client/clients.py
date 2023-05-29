from pydantic import BaseModel, Extra

from app.core.registry import Registry


class Client(BaseModel, Registry):
    """Persistence layer base as a web client"""

    class Config:
        frozen = True
        extra = Extra.forbid
        arbitrary_types_allowed = True
