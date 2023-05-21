from typing import Annotated

from fastapi import Depends

from app.access import AccessQuerier
from app.bot import BotClienteer
from app.gpt import GptClienteer

from .repositories import SlashcommandCommandRepository
from .services import SlashcommandCommandService, SlashcommandService

SlashcommandCommander = Annotated[
    SlashcommandCommandService, Depends(SlashcommandCommandRepository)
]


def slashcommand_servicer(
    commander: SlashcommandCommander,
    access_querier: AccessQuerier,
    bot_clienteer: BotClienteer,
    gpt_clienteer: GptClienteer,
) -> SlashcommandService:
    return SlashcommandService(
        commander=commander,
        access_querier=access_querier,
        bot_clienteer=bot_clienteer,
        gpt_clienteer=gpt_clienteer,
    )


SlashcommandServicer = Annotated[SlashcommandService, Depends(slashcommand_servicer)]
