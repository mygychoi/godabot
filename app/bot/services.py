from pydantic import HttpUrl

from app.core.services import Service

from .clients import BotClient
from .schemas import Message


class BotClientService(Service):
    client: BotClient = BotClient()

    async def post_message(self, *, message: Message):
        await self.client.post_message(
            token=message.token,
            channel_id=message.channel_id,
            text=message.token,
        )

    async def acknowledge(self, *, url: HttpUrl):
        await self.client.acknowledge(url)
