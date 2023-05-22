from pydantic import HttpUrl
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.webhook.async_client import AsyncWebhookClient

from app.core.clients import Client


class BotClient(Client):
    @staticmethod
    async def post_message(token: str, channel_id: str, text: str):
        client = AsyncWebClient(token=token)
        await client.chat_postMessage(channel=channel_id, text=text)

    @staticmethod
    async def acknowledge(url: HttpUrl):
        client = AsyncWebhookClient(url=url)
        await client.send()
