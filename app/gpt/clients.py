import openai

from app.core.clients import Client

from .schemas import ChatCompletionRequest, ChatCompletionResponse, Message, Role


class GptClient(Client):
    @staticmethod
    async def chat(*, prompt: str) -> str:
        completion_request = ChatCompletionRequest(
            messages=[
                Message(role=Role.system, content="You are a helpful chatbot named godabot."),
                Message(role=Role.user, content=prompt),
            ]
        )
        response = await openai.ChatCompletion.acreate(**completion_request.dict())
        return ChatCompletionResponse.from_orm(response).answer()
