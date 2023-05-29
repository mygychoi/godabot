from app.core.service import Service

from .clients import GptClient
from .forms import ChatCompletionForm


class GptClientService(Service):
    client: GptClient = GptClient()

    async def answer_for(self, *, prompt: str) -> str:
        form = ChatCompletionForm.from_prompt(prompt=prompt)
        return await self.client.chat(form=form)
