import asyncio

from app.access import AccessQueryService
from app.bot import BotClientService, FileInput, MessageInput
from app.core.database import CommandService, QueryService
from app.core.service import Service
from app.nlp import GptClientService
from app.vision import StabilityClientService

from .models import Slashcommand
from .repositories import SlashcommandCommandRepository
from .schemas import SlashcommandInput


class SlashcommandQueryService(QueryService):
    access_querier: AccessQueryService = AccessQueryService()
    bot_clienteer: BotClientService = BotClientService()

    async def echo(self, *, input: SlashcommandInput):
        access = await self.access_querier.get_by_team_id(team_id=input.team_id)
        message = MessageInput(channel_id=input.destination, text=input.text)
        await asyncio.gather(
            self.bot_clienteer.post_message(token=access.token, message=message),
            self.bot_clienteer.acknowledge(url=input.response_url),
        )


class SlashcommandCommandService(CommandService):
    repository: SlashcommandCommandRepository = SlashcommandCommandRepository()

    async def create(self, *, slashcommand: Slashcommand):
        async with self.transaction():
            return await self.repository.insert(slashcommand=slashcommand)


class SlashcommandService(Service):
    commander: SlashcommandCommandService = SlashcommandCommandService()
    access_querier: AccessQueryService = AccessQueryService()
    bot_clienteer: BotClientService = BotClientService()
    gpt_clienteer: GptClientService = GptClientService()
    stability_clienteer: StabilityClientService = StabilityClientService()

    async def chat(self, *, input: SlashcommandInput):
        access, answer, *_ = await asyncio.gather(
            self.access_querier.get_by_team_id(team_id=input.team_id),
            self.gpt_clienteer.answer_for(prompt=input.text),
            self.bot_clienteer.acknowledge(url=input.response_url),
            self.commander.create(slashcommand=Slashcommand.parse_obj(obj=input)),
        )
        answer = f"Here is my answer for *{input.text}*\n\n{answer}"
        message = MessageInput(channel_id=input.destination, text=answer)
        await self.bot_clienteer.post_message(token=access.token, message=message)

    async def draw(self, *, input: SlashcommandInput):
        """Access checking should be prioritized considering api cost is expensive"""
        access = await self.access_querier.get_by_team_id(team_id=input.team_id)
        image, *_ = await asyncio.gather(
            self.stability_clienteer.generate_for(prompt=input.text),
            self.bot_clienteer.acknowledge(url=input.response_url),
            self.commander.create(slashcommand=Slashcommand.parse_obj(obj=input)),
        )
        file = FileInput(
            channel_id=input.destination,
            file=image,
            file_name=input.text,
            initial_comment=f"I just drew for *{input.text}*!",
        )
        await self.bot_clienteer.post_file(token=access.token, file=file)
