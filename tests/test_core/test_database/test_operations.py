import pytest

from tests.test_core.test_database import with_pool

from .models import Temp
from .repositories import TempCommandRepository, TempQueryRepository
from .services import TempCommandService, TempQueryService


@pytest.fixture
def querier() -> TempQueryService:
    return TempQueryService(repository=TempQueryRepository())


@pytest.fixture()
def commander() -> TempCommandService:
    return TempCommandService(repository=TempCommandRepository())


@pytest.fixture(scope="module")
def temps() -> list[Temp]:
    return []


@with_pool
@pytest.mark.asyncio
async def test_create(temps: list[Temp], commander: TempCommandService):
    for i in range(50):
        name = f"test_{i}"
        temp = await commander.create(name=name)
        assert temp.name == name
        temps.append(temp)


@with_pool
@pytest.mark.asyncio
async def test_read(temps: list[Temp], querier: TempQueryService):
    for temp in temps:
        t = await querier.get_by_id(id=temp.id)
        assert t == temp
    assert (await querier.get_or_none(id=-1)) is None


@with_pool
@pytest.mark.asyncio
async def test_delete(temps: list[Temp], querier: TempQueryService, commander: TempCommandService):
    for temp in temps:
        await commander.delete(id=temp.id)
        assert (await querier.get_or_none(id=temp.id)) is None
