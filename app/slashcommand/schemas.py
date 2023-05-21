"""Depends on slack slash command api
refer to https://api.slack.com/interactivity/slash-commands
"""

from enum import Enum
from typing import Annotated

from pydantic import HttpUrl, validator

from app.configs import settings
from app.core.schemas import Schema


class Command(str, Enum):
    CHAT = "godabot/"
    ECHO = "godabot-echo/"


class SlashcommandRequest(Schema):
    """
    token=gIkuvaNzQIHg97ATvDxqgjtO
    &team_id=T0001
    &team_domain=example
    &enterprise_id=E0001
    &enterprise_name=Globular%20Construct%20Inc
    &channel_id=C2147483705
    &channel_name=test
    &user_id=U2147483697
    &user_name=Steve
    &command=/weather
    &text=94070
    &response_url=https://hooks.slack.com/commands/1234/5678
    &trigger_id=13345224609.738474920.8088930838d88f008e0
    &api_app_id=A123456

    """

    command: Command
    text: str

    team_id: str
    team_name: str
    team_domain: str
    enterprise_id: str | None = None
    enterprise_name: str | None = None
    user_id: str
    user_name: str

    channel_id: str
    channel_name: str

    response_url: HttpUrl
    api_app_id: str

    trigger_id: str
    token: Annotated[str | None, "deprecated"] = None

    @validator("text")
    def trim_text(cls, v):
        return v.stip("/ ")

    @validator("api_app_id", pre=True)
    def validate_api_app_id(cls, v):
        if v != settings.SLACK_API_APP_ID:
            raise ValueError("Invalid api_app_id")
        return v
