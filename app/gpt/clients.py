import openai

from app.core.clients import Client

from .schemas import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatModel,
    Message,
    Role,
)


class GptClient(Client):
    model: ChatModel = ChatModel.gpt3dot5
    max_tokens: int = 512
    temperature: float = 1.0
    top_p: float = 1.0
    n: int = 1

    async def chat(self, *, prompt: str) -> str:
        completion_request = ChatCompletionRequest(
            model=self.model,
            messages=[
                Message(role=Role.system, content="You are a helpful chatbot named godabot."),
                Message(role=Role.user, content=prompt),
            ],
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            top_p=self.top_p,
            n=self.n,
        )
        response = await openai.ChatCompletion.acreate(**completion_request.dict())
        return ChatCompletionResponse.from_orm(response).answer()
