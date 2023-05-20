from typing import Generic

from app.core.registry import Registry

from .repositories import CommandRepositoryT, QueryRepositoryT
from .transaction import TransactionManager


class QueryService(Generic[QueryRepositoryT], Registry):
    def __init__(self, *, repository: QueryRepositoryT):
        self.repository = repository


class CommandService(Generic[CommandRepositoryT], Registry):
    def __init__(self, *, repository: CommandRepositoryT):
        self.repository = repository

    def transaction(self) -> TransactionManager:
        return TransactionManager.get_or_create(repository=self.repository)
