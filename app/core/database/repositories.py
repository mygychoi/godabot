from asyncpg import Connection, Pool
from pydantic import BaseModel, Extra

from app.core.registry import Registry

from .pool import PoolManager
from .transaction import TransactionManager


class Repository(BaseModel, Registry):
    class Config:
        frozen = True
        extra = Extra.forbid


class QueryRepository(Repository):
    @staticmethod
    def connection() -> Pool:
        manager = PoolManager
        return manager.pool()


class CommandRepository(Repository):
    def connection(self) -> Connection:
        manager = TransactionManager.get(repository=self)
        return manager.connection()

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return id(self) == id(other)
