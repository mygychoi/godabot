from pydantic import HttpUrl
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.webhook.async_client import AsyncWebhookClient


class BotClient:
    @staticmethod
    async def post_message(token: str, channel_id: str, message: str):
        client = AsyncWebClient(token=token)
        await client.chat_postMessage(
            channel=channel_id,
            text=message,
        )

    @staticmethod
    async def acknowledge(url: HttpUrl):
        client = AsyncWebhookClient(url=url)
        await client.send()
