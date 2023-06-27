from __future__ import annotations

from datetime import datetime, timedelta
from enum import Enum
from typing import Iterator

from pydantic import Field

from app.core.database import TimestampModel
from app.core.timezone import utcnow


class Roulette(TimestampModel):
    class Status(str, Enum):
        scheduled = "scheduled"
        spun = "spun"
        canceled = "canceled"

    id: int = Field(default=None)
    channel_id: str = Field(max_length=255)
    title: str = Field(default="")
    status: Status = Field(default=Status.scheduled)
    spin_at: datetime = Field(default_factory=lambda: utcnow() + timedelta(hours=1))

    # Related
    lunches: list[Lunch] = []
    attendances: list[Attendance] = []

    def __iter__(self) -> Iterator[Lunch]:
        return iter(self.lunches)

    def __len__(self) -> int:
        return len(self.lunches)

    def __contains__(self, attendance: Attendance):
        """TODO: Optimize by set datastructure"""
        return any(attendance.user_id == _attendance.user_id for _attendance in self.attendances)

    @property
    def countdown(self) -> int:
        return (self.spin_at - utcnow()).seconds


class Attendance(TimestampModel):
    id: int | None = Field(default=None)
    user_id: str = Field(max_length=255)
    user_name: str = Field(max_length=255)
    preference: str = Field(default="")

    # Foreign Keys
    roulette_id: int = Field()
    lunch_id: int | None = Field(default=None)

    # Related
    roulette: Roulette | None = None

    def __str__(self) -> str:
        return f"user_id:{self.user_id}, user_name:{self.user_name}, preference:{self.preference}"

    @property
    def mention(self) -> str:
        return f"<@{self.user_id}>"


class Lunch(TimestampModel):
    id: int | None = Field(default=None)
    title: str = Field(max_length=255)
    preference: str = Field()
    recommendation: str = Field()

    # Foreign Keys
    roulette_id: int = Field()

    # Related
    attendances: list[Attendance] = []
