from slack_sdk.web.async_client import AsyncWebClient

from app.configs import settings
from app.core.clients import Client

from .schemas import AccessRequest, AccessResponse


class AccessClient(Client):
    client: AsyncWebClient = AsyncWebClient()

    async def request(self, *, request: AccessRequest) -> AccessResponse:
        access_resp = await self.client.oauth_access(
            client_id=settings.SLACK_CLIENT_ID,
            client_secret=settings.SLACK_CLIENT_SECRET,
            code=request.code,
        )
        return AccessResponse.from_orm(access_resp)
