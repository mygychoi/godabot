from pydantic import HttpUrl

from app.core.services import Service

from .clients import BotClient
from .schemas import File, Message


class BotClientService(Service):
    client: BotClient = BotClient()

    async def post_message(self, *, message: Message):
        await self.client.post_message(**message.dict(exclude={"blocks"}))

    async def post_file(self, *, file: File):
        await self.client.post_file(**file.dict())

    async def acknowledge(self, *, url: HttpUrl):
        await self.client.acknowledge(url=url)
