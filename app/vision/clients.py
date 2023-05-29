from typing import ClassVar

import aiohttp

from app.configs import settings
from app.core.client import Client

from .forms import StabilityForm, StabilityFormResult


class StabilityClient(Client):
    HEADERS: ClassVar[dict] = {"Authorization": f"Bearer {settings.STABILITY_API_KEY}"}

    @classmethod
    async def generate_image(cls, *, form: StabilityForm) -> bytes:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=form.url,
                headers=cls.HEADERS,
                json=form.dict(exclude={"engine"}),
            ) as response:
                data = await response.json()
                return StabilityFormResult.parse_obj(data).file()
