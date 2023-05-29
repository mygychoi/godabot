from app.core.cache import rlu
from app.core.database import CommandRepository, QueryRepository

from .models import Access

access_rlu = rlu[Access]


class AccessQueryRepository(QueryRepository):
    @access_rlu(key="team_id")
    async def get_by_team_id(self, *, team_id: str) -> Access:
        record = await self.connection().fetchrow(
            """
            SELECT *
            FROM access_access
            WHERE team_id = $1;
            """,
            team_id,
        )
        return Access.construct_from(obj=record)


class AccessCommandRepository(CommandRepository):
    async def save(self, *, access: Access):
        record = await self.connection().fetchrow(
            """
            INSERT INTO
                access_access (
                    team_id,
                    team_name,
                    token,
                    is_active,
                    organization_id,
                    organization_name
                )
            VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (team_id)
            DO UPDATE
                SET
                    team_name = $2,
                    token = $3,
                    is_active = $4,
                    organization_id = $5,
                    organization_name = $6
            RETURNING *;
           """,
            *access.dict(exclude={"created_at", "updated_at"}).values(),
        )
        return Access.construct_from(obj=record)

    async def delete(self, *, team_id: str):
        await self.connection().execute(
            """
            DELETE
            FROM access_access
            WHERE team_id=$1;
            """,
            team_id,
        )
