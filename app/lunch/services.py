from __future__ import annotations

import asyncio
import logging
import random

from pydantic import ValidationError

from app.core.database import CommandService, QueryService
from app.nlp import GptClientService

from .constants import PROMPT
from .exceptions import RouletteSpinFailed
from .forms import RouletteSpunForm
from .models import Attendance, Roulette
from .repositories import (
    AttendanceCommandRepository,
    AttendanceQueryRepository,
    LunchCommandRepository,
    RouletteCommandRepository,
    RouletteQueryRepository,
)


class RouletteQueryService(QueryService):
    repository: RouletteQueryRepository = RouletteQueryRepository()

    async def get_scheduled_by_channel_id(self, *, channel_id: str) -> Roulette:
        return await self.repository.get(channel_id=channel_id, status=Roulette.Status.scheduled)

    async def is_scheduled_by_channel_id(self, *, channel_id: str):
        return await self.repository.exists(channel_id=channel_id, status=Roulette.Status.scheduled)


class RouletteCommandService(CommandService):
    repository: RouletteCommandRepository = RouletteCommandRepository()
    querier: RouletteQueryService = RouletteQueryService()
    attendance_query_repository: AttendanceQueryRepository = AttendanceQueryRepository()
    lunch_command_repository: LunchCommandRepository = LunchCommandRepository()
    gpt_clienteer: GptClientService = GptClientService()

    async def open(self, *, channel_id: str, title: str) -> Roulette:
        if await self.querier.is_scheduled_by_channel_id(channel_id=channel_id):
            roulette = await self.querier.get_scheduled_by_channel_id(channel_id=channel_id)
        else:
            async with self.transaction(self.repository):
                roulette = Roulette(channel_id=channel_id, title=title)
                await self.repository.save(roulette=roulette)
        return roulette

    async def cancel(self, *, roulette: Roulette):
        async with self.transaction(self.repository):
            await self.repository.delete(
                channel_id=roulette.channel_id,
                status=roulette.Status.scheduled,
            )

    async def spin(self, *, roulette: Roulette, temperature=1.0):
        attendances = await self.attendance_query_repository.filter_by(roulette_id=roulette.id)
        prompt = self.make_prompt(roulette=roulette, attendances=attendances)
        answer = await self.gpt_clienteer.answer_for(
            prompt=prompt,
            max_tokens=2_048,
            temperature=temperature,
        )
        try:
            lunches = RouletteSpunForm.parse_raw(answer).lunches
        except ValidationError as error:
            raise RouletteSpinFailed(f"Spinning was failed from {roulette.title}") from error
        else:
            async with self.transaction(
                self.repository,
                self.lunch_command_repository,
            ):
                await self.repository.set_lunches(roulette=roulette, lunches=lunches)
                for lunch in lunches:
                    await self.lunch_command_repository.set_attendances(
                        lunch=lunch, attendances=lunch.attendances
                    )
                roulette.status = roulette.Status.spun
                await self.repository.save(roulette=roulette)

    async def spin_until_success(self, *, roulette: Roulette, threshold: int = 5):
        if threshold > 5:
            raise ValueError(f"Too high {threshold} threshold")
        attempt = 0
        temperature = 1.0
        success = False
        while not success and attempt <= threshold:
            try:
                await self.spin(roulette=roulette, temperature=temperature)
            except RouletteSpinFailed as error:
                logging.warning(f"attempts: {attempt}, error: {error}")
                attempt += 1
                temperature = random.randint(0, 20) / 10
                await asyncio.sleep(1)
            else:
                success = True
            finally:
                if attempt > threshold:
                    logging.error(
                        f"Spinning Failed with {attempt} attempts and {threshold} threshold"
                    )

    @staticmethod
    def make_prompt(*, roulette: Roulette, attendances: list[Attendance]) -> str:
        attendance_info = "\n".join(str(attendance) for attendance in attendances)
        return PROMPT + f"roulette_id:{roulette.id}\n\n" + attendance_info


class AttendanceCommandService(CommandService):
    repository: AttendanceCommandRepository = AttendanceCommandRepository()
    roulette_querier: RouletteQueryService = RouletteQueryService()

    async def join_roulette(
        self,
        *,
        channel_id: str,
        user_id: str,
        user_name: str,
        preference: str,
    ) -> Attendance:
        roulette = await self.roulette_querier.get_scheduled_by_channel_id(channel_id=channel_id)
        async with self.transaction(self.repository):
            attendance = Attendance(
                user_id=user_id,
                user_name=user_name,
                roulette_id=roulette.id,
                preference=preference,
                roulette=roulette,
            )
            await self.repository.save(attendance=attendance)
            if attendance not in roulette:
                roulette.attendances.append(attendance)
            return attendance
