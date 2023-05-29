import pytest

from app.access.schemas import AccessInput
from app.access.services import AccessCommandService
from app.configs import settings
from tests.pool import with_pool

from .clients import AccessTestClient


@pytest.fixture
def input():
    return AccessInput(
        client_secret=settings.SLACK_CLIENT_SECRET,
        client_id=settings.SLACK_CLIENT_ID,
        code="test",
    )


@pytest.fixture
def commander():
    return AccessCommandService(client=AccessTestClient())


@with_pool
@pytest.mark.asyncio
async def test_activation(input: AccessInput, commander: AccessCommandService):
    active_access = await commander.activate(input=input)
    assert active_access.is_active is True
    assert active_access.created_at is not None
    assert active_access.updated_at is None

    inactive_access = await commander.deactivate(team_id=active_access.team_id)
    assert inactive_access.team_id == active_access.team_id
    assert inactive_access.token == active_access.token
    assert inactive_access.is_active is False
    assert inactive_access.created_at is not None
    assert inactive_access.updated_at is not None

    await commander.delete(team_id=inactive_access.team_id)
