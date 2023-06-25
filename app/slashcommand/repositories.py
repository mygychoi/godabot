from app.core.database import CommandRepository

from .models import Slashcommand


class SlashcommandCommandRepository(CommandRepository):
    async def insert(self, *, slashcommand: Slashcommand):
        record = await self.connection().fetchrow(
            """
            INSERT INTO
                slashcommand_slashcommand (
                    team_id,
                    team_name,
                    command
                )
            VALUES ($1, $2, $3)
            RETURNING *;
           """,
            *slashcommand.dict(exclude={"id", "created_at"}).values(),
        )
        return Slashcommand.construct_from(record=record)
