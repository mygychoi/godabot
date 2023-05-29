from pydantic import HttpUrl

from app.core.service import Service

from .clients import BotClient
from .forms import FileForm
from .schemas import FileInput, MessageInput


class BotClientService(Service):
    client: BotClient = BotClient()

    async def post_message(self, *, token: str, message: MessageInput):
        await self.client.post_message(token=token, **message.dict())

    async def post_file(self, *, token: str, file: FileInput):
        form = FileForm.from_input(input=file)
        await self.client.post_file(token=token, form=form)

    async def acknowledge(self, *, url: HttpUrl):
        await self.client.acknowledge(url=url)
