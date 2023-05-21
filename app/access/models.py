from datetime import datetime

from pydantic import Field

from app.core.database import Model

from .schemas import AccessResponse


class Access(Model):
    team_id: str = Field(description="varchar(255), not null, pk")
    team_name: str = Field(description="varchar(255), not null")
    token: str = Field(description="varchar(255), not null, unique")
    is_active: bool = Field(description="boolean, default true, not null", default=True)

    # for later
    organization_id: str | None = Field(description="varchar(255)", default=None)
    organization_name: str | None = Field(description="varchar(255)", default=None)

    # timestamp
    created_at: datetime = Field(
        description="timestamp with time zone, not null",
        default_factory=datetime.utcnow,
    )
    updated_at: datetime | None = Field(
        description="timestamp with time zone, not null",
        default=None,
    )

    @classmethod
    def parse_response(cls, *, response: AccessResponse) -> "Access":
        team = response.team
        access = cls(team_id=team.id, team_name=team.name, token=response.access_token)
        if response.enterprise is not None:
            access.organization_id = response.enterprise.id
            access.organization_name = response.enterprise.name
        return access
