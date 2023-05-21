from typing import Annotated

from fastapi import Depends

from .clients import BotClient
from .services import BotClientService

BotClienteer = Annotated[BotClientService, Depends(BotClient)]
