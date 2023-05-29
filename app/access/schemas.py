"""Depend on slackbot authorization api specifications
Please refer to https://api.slack.com/methods/oauth.v2.access
"""

from pydantic import validator

from app.configs import settings
from app.core.service import Schema


class AccessInput(Schema):
    """Request spec
    client_id: string(Optional)
    client_secret: string(Optional)
    code: string(Optional)
    grant_type: string(Optional)
    redirect_uri: string(Optional)
    refresh_token: string(Optional)
    """

    client_id: str
    client_secret: str
    code: str
    grant_type: str | None = None
    redirect_uri: str | None = None
    refresh_token: str | None = None

    @validator("client_id", pre=True)
    def validate_client_id(cls, v):
        if v != settings.SLACK_CLIENT_ID:
            raise ValueError("Invalid client_id")
        return v

    @validator("client_secret", pre=True)
    def validate_client_secret(cls, v):
        if v != settings.SLACK_CLIENT_SECRET:
            raise ValueError("Invalid client_secret")
        return v
