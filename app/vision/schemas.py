"""Depends on stability.ai api specification
refer to https://platform.stability.ai/rest-api#tag/v1generation/operation/textToImage"""

from typing import Literal

from app.core.schemas import Schema


class TextPrompt(Schema):
    text: str
    weight: float


class StabilityRequest(Schema):
    engine: Literal["stable-diffusion-512-v2-1"] = "stable-diffusion-512-v2-1"
    text_prompts: list[TextPrompt]
    cfg_scale: Literal[7] = 7
    clip_guidance_preset: Literal["FAST_BLUE", "FAST_GREEN"] = "FAST_GREEN"
    height: int = 512
    width: int = 512
    samples: int = 1
    steps: int = 15

    @property
    def url(self) -> str:
        return f"https://api.stability.ai/v1/generation/{self.engine}/text-to-image"
