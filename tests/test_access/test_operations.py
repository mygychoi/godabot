import pytest

from app.access.services import AccessCommandService
from app.configs import settings  # noqa
from tests.pool import with_pool

from .clients import AccessTestClient


@pytest.fixture
def commander():
    return AccessCommandService(client=AccessTestClient())


@with_pool
@pytest.mark.asyncio
async def test_activation(commander: AccessCommandService):
    active_access = await commander.activate(code="test")
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
