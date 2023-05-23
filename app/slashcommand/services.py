import asyncio

from app.access import AccessQueryService
from app.bot import BotClientService, File, Message
from app.core.database import CommandService, QueryService
from app.core.services import Service
from app.gpt import GptClientService
from app.vision import StabilityClientService

from .models import Slashcommand
from .repositories import SlashcommandCommandRepository
from .schemas import SlashcommandForm


class SlashcommandQueryService(QueryService):
    access_querier: AccessQueryService = AccessQueryService()
    bot_clienteer: BotClientService = BotClientService()

    async def echo(self, *, form: SlashcommandForm):
        acknowledging = asyncio.create_task(self.bot_clienteer.acknowledge(url=form.response_url))
        access = await self.access_querier.get_by_team_id(team_id=form.team_id)
        message = Message(token=access.token, channel_id=form.channel_id, text=form.text)
        posting = asyncio.create_task(self.bot_clienteer.post_message(message=message))
        await asyncio.gather(acknowledging, posting)


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

    async def chat(self, *, form: SlashcommandForm):
        acknowledging = asyncio.create_task(self.bot_clienteer.acknowledge(url=form.response_url))
        answer, access = await asyncio.gather(
            self.gpt_clienteer.answer_for(prompt=form.text),
            self.access_querier.get_by_team_id(team_id=form.team_id),
        )
        answer = f"Here is my answer for *{form.text}*\n\n{answer}"
        message = Message(token=access.token, channel_id=form.channel_id, text=answer)
        posting = self.bot_clienteer.post_message(message=message)
        logging = self.commander.create(slashcommand=Slashcommand.parse_obj(obj=form))
        await asyncio.gather(acknowledging, posting, logging)

    async def draw(self, *, form: SlashcommandForm):
        await asyncio.gather(
            self.bot_clienteer.acknowledge(url=form.response_url),
            self.commander.create(slashcommand=Slashcommand.parse_obj(obj=form)),
        )
        image, access = await asyncio.gather(
            self.stability_clienteer.generate_image(prompt=form.text),
            self.access_querier.get_by_team_id(team_id=form.team_id),
        )
        file = File(
            token=access.token,
            channel_id=form.channel_id,
            file_name=form.text,
            file=image,
            initial_comment=f"I just drew for *{form.text}*!",
        )
        await self.bot_clienteer.post_file(file=file)
