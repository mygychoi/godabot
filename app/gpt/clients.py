import openai

from .schemas import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatModel,
    Message,
    Role,
)


class GptClient:
    @staticmethod
    async def chat(
        *,
        prompt: str,
        model: ChatModel = ChatModel.gpt3dot5,
        max_token: int = 512,
        temperature: float = 1.0,
        top_p: float = 1.0,
        n: int = 1,
    ) -> str:
        completion_request = ChatCompletionRequest(
            model=model,
            messages=[
                Message(role=Role.system, content="You are a helpful chatbot named godabot."),
                Message(role=Role.user, content=prompt),
            ],
            max_token=max_token,
            temperature=temperature,
            top_p=top_p,
            n=n,
        )
        response = await openai.ChatCompletion.acreate(**completion_request.dict())
        return ChatCompletionResponse.parse_obj(response).answer()
