from slack_sdk.web.async_client import AsyncWebClient

from app.configs import settings

from .schemas import AccessRequest, AccessResponse


class AccessClient:
    def __init__(self):
        self.client: AsyncWebClient = AsyncWebClient()

    async def request(self, *, request: AccessRequest) -> AccessResponse:
        access_resp = await self.client.oauth_access(
            client_id=settings.SLACK_CLIENT_ID,
            client_secret=settings.SLACK_CLIENT_SECRET,
            code=request.code,
        )
        return AccessResponse.parse_obj(access_resp)
