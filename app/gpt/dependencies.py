from typing import Annotated

from fastapi import Depends

from .clients import GptClient
from .services import GptClientService

GptClienteer = Annotated[GptClientService, Depends(GptClient)]
