import pytest

from app.configs import settings  # noqa
from app.nlp.services import GptClientService


@pytest.fixture
def gpt_clienteer():
    return GptClientService()


@pytest.mark.asyncio
async def test_gpt_chat(gpt_clienteer: GptClientService):
    answer = await gpt_clienteer.answer_for(prompt="Who are you?")
    assert "goda".casefold() in answer.casefold()
