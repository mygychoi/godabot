import asyncio

from app.core.database import CommandService, QueryService
from tests.test_core.test_database.repositories import (
    TempCommandRepository,
    TempQueryRepository,
)


class TempQueryService(QueryService):
    repository: TempQueryRepository = TempQueryRepository()

    async def get_by_id(self, *, id: int):
        return await self.repository.get_by_id(id=id)

    async def get_or_none(self, *, id: int):
        return await self.repository.get_or_none(id=id)


class TempCommandService(CommandService):
    repository: TempCommandRepository = TempCommandRepository()

    async def create(self, *, name: str):
        async with self.transaction():
            return await self.repository.create(name=name)

    async def nested_create(self, *, name: str):
        temps = []
        async with self.transaction():
            temps.append(await self.repository.create(name=name))
            temps.append(await self.repository.create(name=name))
            async with self.transaction():
                temps.append(await self.repository.create(name=name))
                temps.append(await self.repository.create(name=name))
                async with self.transaction():
                    temps.append(await self.repository.create(name=name))
                    temps.append(await self.repository.create(name=name))
                    return temps

    async def delete(self, *, id: int):
        async with self.transaction():
            await self.repository.delete(id=id)


class TempAggregateService:
    def __init__(self, querier: TempQueryService, commander: TempCommandService):
        self.querier = querier
        self.commander = commander

    async def read_and_write(self, *, id: int, name: str):
        reading = [self.querier.get_by_id(id=id) for _ in range(10)]
        temps = [await self.commander.create(name=name) for _ in range(10)]
        temps.extend(await asyncio.gather(*reading))
        return temps
