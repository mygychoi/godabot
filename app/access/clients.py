from slack_sdk.web.async_client import AsyncWebClient

from app.configs import settings
from app.core.client import Client

from .forms import AccessFormResult


class AccessClient(Client):
    client: AsyncWebClient = AsyncWebClient()

    async def acquire_access(self, *, code: str) -> AccessFormResult:
        response = await self.client.oauth_v2_access(
            client_id=settings.SLACK_CLIENT_ID,
            client_secret=settings.SLACK_CLIENT_SECRET,
            code=code,
        )
        return AccessFormResult.from_orm(response)
