import pytest

from app.access.repositories import AccessCommandRepository, AccessQueryRepository
from app.access.schemas import AccessRequest
from app.access.services import AccessCommandService, AccessQueryService
from app.configs import settings
from tests.pool import with_pool

from .clients import AccessTestClient


@pytest.fixture
def access_request():
    return AccessRequest(
        client_secret=settings.SLACK_CLIENT_SECRET, client_id=settings.SLACK_CLIENT_ID, code="test"
    )


@pytest.fixture
def commander():
    return AccessCommandService(
        querier=AccessQueryService(repository=AccessQueryRepository()),
        repository=AccessCommandRepository(),
        client=AccessTestClient(),
    )


@with_pool
@pytest.mark.asyncio
async def test_activation(access_request: AccessRequest, commander: AccessCommandService):
    active_access = await commander.activate(request=access_request)
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
