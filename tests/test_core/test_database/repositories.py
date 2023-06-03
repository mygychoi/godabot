from app.core.cache import rlu
from app.core.database import CommandRepository, QueryRepository
from tests.test_core.test_database.models import Temp


class TempQueryRepository(QueryRepository):
    @rlu[Temp]("id")
    async def get_by_id(self, *, id: int) -> Temp:
        record = await self.connection().fetchrow(
            """
            SELECT id, name
            FROM test_temp
            WHERE id = $1;
            """,
            id,
        )
        return Temp.construct_from(obj=record)

    @rlu[Temp | None]("id")
    async def get_or_none(self, *, id: int) -> Temp | None:
        record = await self.connection().fetchrow(
            """
            SELECT id, name
            FROM test_temp
            WHERE id = $1;
            """,
            id,
        )
        return Temp.construct_from_or_none(obj=record)


class TempCommandRepository(CommandRepository):
    async def create(self, *, name: str):
        record = await self.connection().fetchrow(
            """
            INSERT INTO test_temp (name)
            VALUES ($1)
            RETURNING *;
            """,
            name,
        )
        return Temp.construct_from(obj=record)

    async def delete(self, *, id: int):
        await self.connection().execute(
            """
            DELETE
            FROM test_temp
            WHERE id=$1;
            """,
            id,
        )
