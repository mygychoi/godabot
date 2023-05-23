from app.core.services import Service

from .clients import StabilityClient


class StabilityClientService(Service):
    client: StabilityClient = StabilityClient()

    async def generate_image(self, *, prompt: str) -> bytes:
        return await self.client.request(prompt=prompt)
