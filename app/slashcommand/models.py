from datetime import datetime

from pydantic import Field

from app.core.database import Model


class Slashcommand(Model):
    id: int | None = Field(default=None, description="serial, not null, pk")
    team_id: str = Field(description="varchar(255), not null")
    team_name: str = Field(description="varchar(255), not null")
    command: str = Field(description="varchar(255), not null")

    # timestamptz
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="timestamptz, default current_timestamp, index(desc)",
    )
