import openai

from app.core.client import Client

from .forms import ChatCompletionForm, ChatCompletionFormResult


class GptClient(Client):
    @staticmethod
    async def chat(*, form: ChatCompletionForm) -> str:
        response = await openai.ChatCompletion.acreate(**form.dict())
        result = ChatCompletionFormResult.from_orm(response)
        return result.answer
