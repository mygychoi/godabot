from app.core.services import Service

from .repositories import CommandRepository
from .transaction import TransactionManager


class QueryService(Service):
    pass


class CommandService(Service):
    repository: CommandRepository

    def transaction(self) -> TransactionManager:
        return TransactionManager.get_or_create(repository=self.repository)
