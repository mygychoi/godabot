from __future__ import annotations

from datetime import datetime

from app.core.service import Schema


class RouletteSchema(Schema):
    title: str
    lunch_at: datetime
    created_at: datetime
    attendees: list[AttendanceSchema]
    lunches: list[LunchSchema]


class AttendanceSchema(Schema):
    user_id: str
    preference: str
    attend_at: datetime
    roulette: RouletteSchema
    lunch: LunchSchema


class LunchSchema(Schema):
    title: str
    attendees: list[AttendanceSchema]
