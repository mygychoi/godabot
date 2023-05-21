from pydantic import HttpUrl

from .clients import BotClient


class BotClientService:
    def __init__(self, client: BotClient):
        self.client = client

    async def post_message(self, *, token: str, channel_id: str, message: str):
        await self.client.post_message(token=token, channel_id=channel_id, message=message)

    async def acknowledge(self, *, url: HttpUrl):
        await self.client.acknowledge(url)
