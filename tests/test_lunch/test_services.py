import random

import pytest

from app.lunch.models import Attendance, Roulette
from app.lunch.services import (
    AttendanceCommandService,
    RouletteCommandService,
    RouletteQueryService,
)
from tests.test_core.test_database import with_pool

channel_id = f"test_{random.randint(0, 1000_000_000)}"


@pytest.fixture(scope="module")
def roulettes() -> list[Roulette]:
    return []


@pytest.fixture(scope="module")
def attendances() -> list[Attendance]:
    return []


@pytest.mark.asyncio
@with_pool
async def test_roulette_create(roulettes: list[Roulette]):
    commander = RouletteCommandService()
    querier = RouletteQueryService()
    title = f"test_tile_{channel_id}"
    first = await commander.open(channel_id=channel_id, title=title)
    second = await querier.get_scheduled_by_channel_id(channel_id=channel_id)
    third = await commander.open(channel_id=channel_id, title=title)
    fourth = await querier.get_scheduled_by_channel_id(channel_id=channel_id)
    assert first == second == third == fourth
    roulettes.append(first)


@pytest.mark.parametrize("preference", ["pizza", "pizza", "pizza", "italian food", "anything"])
@pytest.mark.asyncio
@with_pool
async def test_roulette_join(
    preference: str, attendances: list[Attendance], roulettes: list[Roulette]
):
    commander = AttendanceCommandService()
    for roulette in roulettes:
        uuid = f"test_user_id_{random.randint(1, 1_000_000_000_000)}"
        attendance = await commander.join_roulette(
            roulette=roulette,
            user_id=uuid,
            user_name=uuid,
            preference=preference,
        )
        attendances.append(attendance)


@pytest.mark.asyncio
@with_pool
async def test_roulette_spin(roulettes: list[Roulette]):
    roulette: Roulette = roulettes[-1]
    commander = RouletteCommandService()
    await commander.spin_until_success(roulette=roulette)
    querier = RouletteQueryService()
    assert await querier.exists_scheduled_by_channel_id(channel_id=roulette.channel_id) is False
