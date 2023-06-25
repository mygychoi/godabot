from app.core.service import Service

from .clients import GptClient
from .forms import ChatCompletionForm


class GptClientService(Service):
    client: GptClient = GptClient()

    async def answer_for(
        self, *, prompt: str, temperature: float = 1.0, max_tokens: int = 512
    ) -> str:
        form = ChatCompletionForm.from_prompt(
            prompt=prompt, temperature=temperature, max_tokens=max_tokens
        )
        return await self.client.chat(form=form)
