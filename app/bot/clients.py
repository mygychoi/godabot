from pydantic import HttpUrl
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.webhook.async_client import AsyncWebhookClient

from app.core.client import Client

from .forms import FileForm


class BotClient(Client):
    @staticmethod
    async def post_message(*, token: str, channel_id: str, text: str, blocks: list):
        client = AsyncWebClient(token=token)
        await client.chat_postMessage(channel=channel_id, text=text, blocks=blocks)

    @staticmethod
    async def post_file(*, token: str, form: FileForm):
        slack_web_client = AsyncWebClient(token=token)
        await slack_web_client.files_upload_v2(**form.dict())

    @staticmethod
    async def acknowledge(*, url: HttpUrl):
        client = AsyncWebhookClient(url=url)
        await client.send()
