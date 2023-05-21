import uuid

from app.access.clients import AccessClient
from app.access.schemas import AccessRequest, AccessResponse


class AccessTestClient(AccessClient):
    async def request(self, *, request: AccessRequest) -> AccessResponse:
        return AccessResponse(
            ok=True,
            access_token=str(uuid.uuid4()),
            token_type="test_token_type",
            scope="test_scope",
            bot_user_id="test_bot_user_id",
            app_id="test_app_id",
            team=AccessResponse.Team(id=str(uuid.uuid4()), name="test_team_name"),
        )
