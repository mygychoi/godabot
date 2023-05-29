"""Depend on slackbot authorization api specifications
Please refer to https://api.slack.com/methods/oauth.v2.access
"""

from app.core.client import Form


class AccessFormResult(Form):
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

    class TeamForm(Form):
        name: str
        id: str

    class EnterpriseForm(Form):
        name: str
        id: str

    class AuthedUserForm(Form):
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
    team: TeamForm
    enterprise: EnterpriseForm | None = None
    authed_user: AuthedUserForm | None = None

    class Config:
        orm_mode = True
