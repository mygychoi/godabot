from .clients import GptClient


class GptClientService:
    def __init__(self, client: GptClient):
        self.client = client

    async def answer_for(self, *, prompt: str) -> str:
        return await self.client.chat(prompt=prompt)
