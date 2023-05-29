"""Depends on stability.ai api specification
refer to https://platform.stability.ai/rest-api#tag/v1generation/operation/textToImage"""

import base64
from typing import Literal

from app.core.client import Form


class StabilityForm(Form):
    class TextPromptForm(Form):
        text: str
        weight: float = 1.0

    engine: Literal["stable-diffusion-512-v2-1"] = "stable-diffusion-512-v2-1"
    text_prompts: list[TextPromptForm]
    cfg_scale: Literal[7] = 7
    clip_guidance_preset: Literal["FAST_BLUE", "FAST_GREEN"] = "FAST_GREEN"
    height: int = 512
    width: int = 512
    samples: int = 1
    steps: int = 15

    @property
    def url(self) -> str:
        return f"https://api.stability.ai/v1/generation/{self.engine}/text-to-image"

    @classmethod
    def from_prompt(cls, *, prompt: str) -> "StabilityForm":
        return cls(text_prompts=[cls.TextPromptForm(text=prompt)])


class StabilityFormResult(Form):
    class ArtifactForm(Form):
        base64: str
        finishReason: str
        seed: int

    artifacts: list[ArtifactForm]
    """
    [
      [
        {
          "base64": "...very long string...",
          "finishReason": "SUCCESS",
          "seed": 1050625087
        },
        {
          "base64": "...very long string...",
          "finishReason": "CONTENT_FILTERED",
          "seed": 1229191277
        }
      ]
    ]
    """

    def file(self) -> bytes:
        return base64.b64decode(self.artifacts[0].base64)
