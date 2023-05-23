"""Depends on slack slash command api
refer to https://api.slack.com/interactivity/slash-commands
"""

from enum import Enum
from typing import Annotated

from fastapi import Form
from pydantic import HttpUrl, validator

from app.configs import settings
from app.core.schemas import Schema


class Command(str, Enum):
    CHAT = "/godabot"
    ECHO = "/godabot-echo"
    DRAW = "/godabot-draw"


class SlashcommandForm(Schema):
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

    command: Annotated[Command, Form()]
    text: Annotated[str, Form()]

    team_id: Annotated[str, Form()]
    team_domain: Annotated[str, Form()]

    enterprise_id: Annotated[str | None, Form()] = None
    enterprise_name: Annotated[str | None, Form()] = None

    user_id: Annotated[str, Form()]
    user_name: Annotated[str, Form()]

    channel_id: Annotated[str, Form()]
    channel_name: Annotated[str, Form()]

    response_url: Annotated[HttpUrl, Form()]
    api_app_id: Annotated[str, Form()]

    trigger_id: Annotated[str | None, Form()]
    token: Annotated[str | None, Form()] = None  # deprecated

    @validator("api_app_id", pre=True)
    def validate_api_app_id(cls, v):
        if v != settings.SLACK_API_APP_ID:
            raise ValueError("Invalid api_app_id")
        return v
