import asyncio

from app.core.database import CommandRepository, QueryRepository

from .models import Attendance, Lunch, Roulette


class RouletteQueryRepository(QueryRepository):
    async def get(self, *, channel_id, status: Roulette.Status) -> Roulette:
        record = await self.connection().fetchrow(
            """
            SELECT *
            FROM lunch_roulette
            WHERE channel_id = $1 AND status = $2;
            """,
            channel_id,
            status,
        )
        roulette = Roulette.construct_from(record=record)
        attendances_fetching = self.connection().fetch(
            """
            SELECT *
            FROM lunch_attendance
            WHERE lunch_attendance.roulette_id = $1;
            """,
            roulette.id,
        )
        lunches_fetching = self.connection().fetch(
            """
            SELECT *
            FROM lunch_lunch
            WHERE lunch_lunch.roulette_id = $1;
            """,
            roulette.id,
        )
        attendance_records, lunches_records = await asyncio.gather(
            attendances_fetching, lunches_fetching
        )
        roulette.attendances = [
            Attendance.construct_from(record=record) for record in attendance_records
        ]
        roulette.lunches = [Lunch.construct_from(record=record) for record in lunches_records]
        return roulette

    async def exists(self, *, channel_id, status) -> bool:
        record = await self.connection().fetchrow(
            """
            SELECT 1
            FROM lunch_roulette
            WHERE channel_id = $1 AND status = $2;
            """,
            channel_id,
            status,
        )
        return record is not None


class RouletteCommandRepository(CommandRepository):
    async def save(self, *, roulette: Roulette):
        record = await self.connection().fetchrow(
            """
            INSERT INTO
                lunch_roulette (
                    channel_id,
                    title,
                    status,
                    spin_at
                )
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (channel_id, status) WHERE status='scheduled'
            DO UPDATE
                SET
                    title = $2,
                    status = $3,
                    spin_at = $4
            RETURNING *;
           """,
            *roulette.dict(include={"channel_id", "title", "status", "spin_at"}).values(),
        )
        roulette.update_from(record=record)

    async def delete(self, *, channel_id: str, status: Roulette.Status):
        await self.connection().execute(
            """
            DELETE
            FROM lunch_roulette
            WHERE channel_id = $1 AND status = $2;
            """,
            channel_id,
            status,
        )

    async def add_lunches(self, *, roulette: Roulette, lunches: list[Lunch]):
        await self.connection().executemany(
            """
            INSERT INTO lunch_lunch (title, preference, recommendation, roulette_id)
            VALUES ($1, $2, $3, $4);
            """,
            [
                [lunch.title, lunch.preference, lunch.recommendation, roulette.id]
                for lunch in lunches
            ],
        )
        records = await self.connection().fetch(
            """
            SELECT *
            FROM lunch_lunch
            WHERE roulette_id = $1
            ORDER BY created_at;
            """,
            roulette.id,
        )
        Lunch.update_many_from(models=lunches, records=records)
        roulette.lunches = lunches

    async def remove_lunches(self, *, roulette: Roulette):
        await self.connection().execute(
            """
            DELETE FROM lunch_lunch
            WHERE roulette_id = $1;
            """,
            roulette.id,
        )
        roulette.lunches = []

    async def set_lunches(self, *, roulette: Roulette, lunches: list[Lunch]):
        await self.remove_lunches(roulette=roulette)
        await self.add_lunches(roulette=roulette, lunches=lunches)


class AttendanceQueryRepository(QueryRepository):
    async def filter_by(self, *, roulette_id: int) -> list[Attendance]:
        records = await self.connection().fetch(
            """
            SELECT *
            FROM lunch_attendance
            WHERE roulette_id = $1;
            """,
            roulette_id,
        )
        return [Attendance.construct_from(record=record) for record in records]


class AttendanceCommandRepository(CommandRepository):
    async def save(self, *, attendance: Attendance):
        include = {"user_id", "user_name", "preference", "roulette_id", "lunch_id"}
        record = await self.connection().fetchrow(
            """
            INSERT INTO
                lunch_attendance (
                    user_id,
                    user_name,
                    preference,
                    roulette_id,
                    lunch_id
                )
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT on constraint lunch_attendance_user_id_roulette_id_u
            DO UPDATE SET preference = $3
            RETURNING *;
           """,
            *attendance.dict(include=include).values(),
        )
        attendance.update_from(record=record)


class LunchCommandRepository(CommandRepository):
    async def remove_attendances(self, *, lunch: Lunch):
        await self.connection().execute(
            """
            UPDATE lunch_attendance
            SET lunch_id = null
            WHERE lunch_id = $1;
            """,
            lunch.id,
        )
        for attendance in lunch.attendances:
            attendance.lunch_id = None
        lunch.attendances = []

    async def add_attendances(self, *, lunch: Lunch, attendances: list[Attendance]):
        records = await self.connection().fetch(
            """
            UPDATE lunch_attendance
            SET lunch_id = $1
            WHERE roulette_id = $2 AND user_id = ANY($3)
            RETURNING *;
            """,
            lunch.id,
            lunch.roulette_id,
            [attendance.user_id for attendance in attendances],
        )
        Attendance.update_many_from(models=attendances, records=records)
        lunch.attendances = attendances

    async def set_attendances(self, *, lunch: Lunch, attendances: list[Attendance]):
        await self.remove_attendances(lunch=lunch)
        await self.add_attendances(lunch=lunch, attendances=attendances)
