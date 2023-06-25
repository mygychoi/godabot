import asyncio

from app.access import AccessQueryService
from app.bot import BotClientService, FileInput, MessageInput
from app.core.database import CommandService
from app.core.service import Service
from app.lunch import (
    AttendanceCommandService,
    AttendanceJoinedBlockKit,
    RouletteCommandService,
    RouletteOpenBlockKit,
    RouletteQueryService,
    RouletteSpunBlockKit,
)
from app.nlp import GptClientService
from app.vision import StabilityClientService

from .models import Slashcommand
from .repositories import SlashcommandCommandRepository
from .schemas import SlachcommandChannelInput, SlashcommandInput


class SlashcommandEchoService(Service):
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
        async with self.transaction(self.repository):
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


class SlashcommandLunchRouletteService(Service):
    commander: SlashcommandCommandService = SlashcommandCommandService()
    access_querier: AccessQueryService = AccessQueryService()
    roulette_querier: RouletteQueryService = RouletteQueryService()
    roulette_commander: RouletteCommandService = RouletteCommandService()
    attendance_commander: AttendanceCommandService = AttendanceCommandService()
    bot_clienteer: BotClientService = BotClientService()

    async def open_roulette(self, *, input: SlachcommandChannelInput):
        access = await self.access_querier.get_by_team_id(team_id=input.team_id)
        title = f"{access.team_name} - {input.channel_name} - {input.user_name}"
        roulette = await self.roulette_commander.open(channel_id=input.channel_id, title=title)
        blockkit = RouletteOpenBlockKit(roulette=roulette)
        message = MessageInput(channel_id=input.channel_id, text=title, blocks=blockkit.blocks())
        await self.bot_clienteer.post_message(token=access.token, message=message)

        async def schedule_roulette_spinning():
            await asyncio.sleep(roulette.countdown)
            await self.spin_roulette_until_success(input=input)

        asyncio.create_task(schedule_roulette_spinning())

    async def cancel_roulette(self, *, input: SlachcommandChannelInput):
        roulette = await self.roulette_querier.get_scheduled_by_channel_id(
            channel_id=input.channel_id
        )
        await self.roulette_commander.cancel(roulette=roulette)

    async def spin_roulette_until_success(self, *, input: SlachcommandChannelInput):
        access = await self.access_querier.get_by_team_id(team_id=input.team_id)
        roulette = await self.roulette_querier.get_scheduled_by_channel_id(
            channel_id=input.channel_id
        )
        if len(roulette.attendances) < 2:
            await self.roulette_commander.cancel(roulette=roulette)
            message = MessageInput(
                channel_id=input.channel_id,
                text="Sorry, there are no sufficient attendees. Roulette is canceled",
            )
            await self.bot_clienteer.post_message(token=access.token, message=message)
        else:
            await self.roulette_commander.spin_until_success(roulette=roulette)
            blockkit = RouletteSpunBlockKit(roulette=roulette)
            message = MessageInput(
                channel_id=input.channel_id, text="...", blocks=blockkit.blocks()
            )
            await self.bot_clienteer.post_message(token=access.token, message=message)

    async def join_roulette(self, *, input: SlachcommandChannelInput):
        access = await self.access_querier.get_by_team_id(team_id=input.team_id)
        if not await self.roulette_querier.is_scheduled_by_channel_id(channel_id=input.channel_id):
            await self.bot_clienteer.post_message(
                token=access.token,
                message=MessageInput(
                    channel_id=input.channel_id,
                    text="Sorry, there is no open lunch roulette. "
                    "Please ask @Goda to open a roulette for this channel.",
                ),
            )
        else:
            roulette = await self.roulette_querier.get_scheduled_by_channel_id(
                channel_id=input.channel_id
            )
            attendance = await self.attendance_commander.join_roulette(
                user_id=input.user_id,
                user_name=input.user_name,
                preference=input.text,
                roulette=roulette,
            )
            blockkit = AttendanceJoinedBlockKit(attendance=attendance)
            message = MessageInput(
                channel_id=input.channel_id, text="...", blocks=blockkit.blocks()
            )
            await self.bot_clienteer.post_message(token=access.token, message=message)
