from app.core.service import Service

from .repositories import CommandRepository, QueryRepository
from .transaction import TransactionManager


class QueryService(Service):
    repository: QueryRepository


class CommandService(Service):
    repository: CommandRepository

    @staticmethod
    def transaction(*repositories: CommandRepository) -> TransactionManager:
        first, *remains = repositories
        transaction_manager = TransactionManager.get_or_create(repository=first)
        for repository in remains:
            transaction_manager.add(repository=repository)
        return transaction_manager
