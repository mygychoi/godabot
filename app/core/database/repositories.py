from typing import TypeVar

from asyncpg import Connection, Pool

from app.core.registry import Registry

from .pool import PoolManager
from .transaction import TransactionManager


class QueryRepository(Registry):
    @staticmethod
    def connection() -> Pool:
        manager = PoolManager
        return manager.pool()


class CommandRepository(Registry):
    def connection(self) -> Connection:
        manager = TransactionManager.get(repository=self)
        return manager.connection()


QueryRepositoryT = TypeVar("QueryRepositoryT", bound=QueryRepository)
CommandRepositoryT = TypeVar("CommandRepositoryT", bound=CommandRepository)
