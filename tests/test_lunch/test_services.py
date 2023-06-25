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


@with_pool
@pytest.mark.asyncio
async def test_roulette_create(roulettes: list[Roulette]):
    commander = RouletteCommandService()
    querier = RouletteQueryService()
    title = f"test_tile_{channel_id}"
    first = await commander.open(channel_id=channel_id, title=title)
    print("first here", first)
    second = await querier.get_scheduled_by_channel_id(channel_id=channel_id)
    print("second here", second)
    third = await commander.open(channel_id=channel_id, title=title)
    print("third here", third)
    fourth = await querier.get_scheduled_by_channel_id(channel_id=channel_id)
    print("fourth here", fourth)
    assert first == second == third == fourth
    roulettes.append(first)


@with_pool
@pytest.mark.asyncio
@pytest.mark.parametrize("preference", ["pizza", "pizza", "pizza", "italian food", "anything"])
async def test_attendance_create(
    preference: str, attendances: list[Attendance], roulettes: list[Roulette]
):
    commander = AttendanceCommandService()
    for roulette in roulettes:
        uuid = f"test_user_id_{random.randint(1, 1_000_000)}"
        attendance = await commander.join_roulette(
            channel_id=roulette.channel_id,
            user_id=uuid,
            user_name=uuid,
            preference=preference,
        )
        attendances.append(attendance)


@with_pool
@pytest.mark.asyncio
async def test_roulette_spin(roulettes: list[Roulette]):
    roulette: Roulette = roulettes[-1]
    commander = RouletteCommandService()
    await commander.spin(roulette=roulette)
    assert len(roulette) > 0
    for lunch in roulette:
        assert len(lunch.attendances) > 0
