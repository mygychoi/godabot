from app.core.services import Service

from .clients import GptClient


class GptClientService(Service):
    client: GptClient = GptClient()

    async def answer_for(self, *, prompt: str) -> str:
        return await self.client.chat(prompt=prompt)
