import asyncio
import random

import pytest

from app.core.autils import atimer
from tests.pool import with_pool

from .repositories import TempCommandRepository, TempQueryRepository
from .services import TempAggregateService, TempCommandService, TempQueryService


@atimer
async def async_perf(count: int):
    tasks = []
    for i in range(count):
        querier = TempQueryService(repository=TempQueryRepository())
        commander = TempCommandService(repository=TempCommandRepository())
        aggregator = TempAggregateService(
            querier=TempQueryService(repository=TempQueryRepository()),
            commander=TempCommandService(repository=TempCommandRepository()),
        )
        tasks.extend(
            (
                commander.create(name=f"test_{i}"),
                querier.get_by_id(id=random.randint(50, 100)),
                aggregator.read_and_write(id=random.randint(50, 100), name=f"test_{i}"),
            )
        )
    await asyncio.gather(*tasks)


@atimer
async def sync_perform(count: int):
    for i in range(count):
        commander = TempCommandService(repository=TempCommandRepository())
        querier = TempQueryService(repository=TempQueryRepository())
        aggregator = TempAggregateService(
            querier=TempQueryService(repository=TempQueryRepository()),
            commander=TempCommandService(repository=TempCommandRepository()),
        )
        await commander.create(name=f"test_{i}")
        await querier.get_by_id(id=random.randint(50, 100))
        await aggregator.read_and_write(id=random.randint(50, 100), name=f"test_{i}")


@pytest.mark.parametrize("count", list(range(50, 60)))
@pytest.mark.asyncio
@with_pool
async def test_aioperf(count: int):
    sync_elapsed, _ = await sync_perform(count=count)
    async_elapsed, _ = await async_perf(count=count)
    assert async_elapsed < sync_elapsed, (async_elapsed, sync_elapsed)
