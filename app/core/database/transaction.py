from __future__ import annotations

from typing import TYPE_CHECKING
from weakref import WeakKeyDictionary

from asyncpg import Connection, InterfaceError
from asyncpg.transaction import Transaction

from app.core.datastructures import Stack

from .exceptions import DatabaseError
from .pool import PoolManager

if TYPE_CHECKING:
    from .repositories import CommandRepository


class TransactionManager:
    _managers: WeakKeyDictionary[CommandRepository, TransactionManager] = WeakKeyDictionary()

    def __init__(self):
        self._connection: Connection | None = None
        self._transactions: Stack[Transaction] = Stack[Transaction]()

    @classmethod
    def create(cls, *, repository: CommandRepository) -> TransactionManager:
        manager = cls()
        cls._managers[repository] = manager
        return manager

    @classmethod
    def get(cls, *, repository: CommandRepository) -> TransactionManager:
        return cls._managers[repository]

    @classmethod
    def get_or_create(cls, *, repository: CommandRepository) -> TransactionManager:
        if repository in cls._managers:
            return cls.get(repository=repository)
        else:
            return cls.create(repository=repository)

    def add(self, *, repository: CommandRepository):
        self._managers[repository] = self

    async def __aenter__(self):
        if self._connection is None:
            self._connection = await PoolManager.acquire()
        transaction = self._connection.transaction()
        try:
            await transaction.start()
        except InterfaceError as error:
            await PoolManager.release(connection=self._connection)
            raise DatabaseError("Transaction starting failed") from error
        else:
            self._transactions.push(transaction)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        transaction = self._transactions.pop()
        try:
            if exc_type is None:
                await transaction.commit()
            else:
                await transaction.rollback()
        except InterfaceError as error:
            raise DatabaseError("Transaction was aborted") from error
        finally:
            if self._connection is not None and self._transactions.is_empty():
                await PoolManager.release(connection=self._connection)
                self._connection = None

    def connection(self) -> Connection:
        if self._connection is None:
            raise DatabaseError("There is no connection")
        return self._connection
