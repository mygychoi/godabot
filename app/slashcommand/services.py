import asyncio

from app.access import AccessQueryService
from app.bot import BotClientService
from app.core.database import CommandService
from app.gpt import GptClientService

from .models import Slashcommand
from .repositories import SlashcommandCommandRepository
from .schemas import SlashcommandRequest


class SlashcommandCommandService(CommandService[SlashcommandCommandRepository]):
    async def create(self, *, slashcommand: Slashcommand):
        async with self.transaction():
            return await self.repository.insert(slashcommand=slashcommand)


class SlashcommandService:
    """TODO: Remove code duplication"""

    def __init__(
        self,
        *,
        commander: SlashcommandCommandService,
        access_querier: AccessQueryService,
        bot_clienteer: BotClientService,
        gpt_clienteer: GptClientService,
    ):
        self.commander = commander
        self.access_querier = access_querier
        self.bot_clienteer = bot_clienteer
        self.gpt_clienteer = gpt_clienteer

    async def echo(self, *, request: SlashcommandRequest):
        acknowledging_task = asyncio.create_task(
            self.bot_clienteer.acknowledge(url=request.response_url)
        )
        access = await self.access_querier.get_by_team_id(team_id=request.team_id)
        posting_task = asyncio.create_task(
            self.bot_clienteer.post_message(
                token=access.token,
                channel_id=request.channel_id,
                message=request.text,
            )
        )
        creating_task = asyncio.create_task(
            self.commander.create(slashcommand=Slashcommand.parse_obj(obj=request))
        )
        await asyncio.gather(acknowledging_task, posting_task, creating_task)

    async def chat(self, *, request: SlashcommandRequest):
        acknowledging_task = asyncio.create_task(
            self.bot_clienteer.acknowledge(url=request.response_url)
        )
        answer, access = await asyncio.gather(
            self.gpt_clienteer.answer_for(prompt=request.text),
            self.access_querier.get_by_team_id(team_id=request.team_id),
        )
        posting_task = asyncio.create_task(
            self.bot_clienteer.post_message(
                token=access.token,
                channel_id=request.channel_id,
                message=f"Here is my answer for **{request.text}** \n {answer}",
            )
        )
        creating_task = asyncio.create_task(
            self.commander.create(slashcommand=Slashcommand.parse_obj(obj=request))
        )
        await asyncio.gather(acknowledging_task, posting_task, creating_task)
