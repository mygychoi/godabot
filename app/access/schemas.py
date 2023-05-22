"""Depend on slackbot authorization api specifications
Please refer to https://api.slack.com/methods/oauth.v2.access
"""

from pydantic import validator

from app.configs import settings
from app.core.schemas import Schema


class AccessRequest(Schema):
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


class AccessResponse(Schema):
    """Response spec
    {
        "ok": true,
        "access_token": "xoxb-17653672481-19874698323-pdFZKVeTuE8sk7oOcBrzbqgy",
        "token_type": "bot",
        "scope": "commands,incoming-webhook",
        "bot_user_id": "U0KRQLJ9H",
        "app_id": "A0KRD7HC3",
        "team": {
            "name": "Slack Softball Team",
            "id": "T9TK3CUKW"
        },
        "enterprise": {
            "name": "slack-sports",
            "id": "E12345678"
        },
        "authed_user": {
            "id": "U1234",
            "scope": "chat:write",
            "access_token": "xoxp-1234",
            "token_type": "user"
        }
    }
    """

    class Team(Schema):
        name: str
        id: str

    class Enterprise(Schema):
        name: str
        id: str

    class AuthedUser(Schema):
        id: str
        scope: str
        access_token: str
        token_type: str

    ok: bool
    access_token: str
    token_type: str
    scope: str
    bot_user_id: str
    app_id: str
    team: Team
    enterprise: Enterprise | None = None
    authed_user: AuthedUser | None = None
