"""Depends on slack slash command api
refer to https://api.slack.com/interactivity/slash-commands
"""

from enum import Enum
from typing import Annotated

from fastapi import Form as RouterForm
from pydantic import HttpUrl, validator

from app.configs import settings
from app.core.service import Schema


class Command(str, Enum):
    CHAT = "/godabot"
    ECHO = "/godabot-echo"
    DRAW = "/godabot-draw"


class SlashcommandInput(Schema):
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

    command: Annotated[Command, RouterForm()]
    text: Annotated[str, RouterForm()]

    team_id: Annotated[str, RouterForm()]
    team_domain: Annotated[str, RouterForm()]

    enterprise_id: Annotated[str | None, RouterForm()] = None
    enterprise_name: Annotated[str | None, RouterForm()] = None

    user_id: Annotated[str, RouterForm()]
    user_name: Annotated[str, RouterForm()]

    channel_id: Annotated[str | None, RouterForm()] = None
    channel_name: Annotated[str | None, RouterForm()] = None

    response_url: Annotated[HttpUrl, RouterForm()]
    api_app_id: Annotated[str, RouterForm()]

    trigger_id: Annotated[str | None, RouterForm()]
    token: Annotated[str | None, RouterForm()] = None  # deprecated

    @validator("api_app_id", pre=True)
    def validate_api_app_id(cls, v):
        if v != settings.SLACK_API_APP_ID:
            raise ValueError("Invalid api_app_id")
        return v

    @property
    def destination(self) -> str:
        return self.channel_id or self.user_id
