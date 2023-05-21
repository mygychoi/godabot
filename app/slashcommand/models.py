from datetime import datetime

from pydantic import Field

from app.core.database import Model


class Slashcommand(Model):
    id: int | None = Field(default=None, description="")
    team_id: str = Field(description="")
    team_name: str = Field(description="")
    command: str = Field(description="")
    # timestamp
    created_at: datetime = Field(default_factory=datetime.utcnow, description="")
