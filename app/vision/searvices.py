from app.core.service import Service

from .clients import StabilityClient
from .forms import StabilityForm


class StabilityClientService(Service):
    client: StabilityClient = StabilityClient()

    async def generate_for(self, *, prompt: str) -> bytes:
        form = StabilityForm.from_prompt(prompt=prompt)
        return await self.client.generate_image(form=form)
