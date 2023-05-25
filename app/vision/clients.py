import base64

import aiohttp

from app.configs import settings
from app.core.clients import Client

from .schemas import StabilityRequest, TextPrompt

HEADERS = {"Authorization": f"Bearer {settings.STABILITY_API_KEY}"}


class StabilityClient(Client):
    @staticmethod
    async def request(*, prompt: str) -> bytes:
        generation_request = StabilityRequest(text_prompts=[TextPrompt(text=prompt, weight=1.0)])
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=generation_request.url,
                headers=HEADERS,
                json=generation_request.dict(exclude={"engine"}),
            ) as response:
                data = await response.json()
                # TODO: key error
                return base64.b64decode(data["artifacts"][0]["base64"])
