from pydantic import validator

from app.core.client import Form

from .models import Lunch


class RouletteSpinValidator(Form):
    lunches: list[Lunch]

    @validator("lunches")
    def unique_lunch_per_attendance(cls, lunches: list[Lunch]):
        attendances = set()
        for lunch in lunches:
            for attendance in lunch.attendances:
                if attendance.user_id in attendances:
                    raise ValueError("Attendance is duplicated through lunches")
                else:
                    attendances.add(attendance.user_id)
        return lunches

    @validator("lunches", each_item=True)
    def min_attendances_per_lunch(cls, lunch: Lunch):
        if len(lunch.attendances) < 2:
            print(lunch.attendances)
            raise ValueError(f"There should be at least 2 attendances at lunch, {lunch}")
        return lunch
