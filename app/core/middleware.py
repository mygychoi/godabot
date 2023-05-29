"""Depends on slack authentication
refer to https://api.slack.com/authentication/verifying-requests-from-slack
"""

import hashlib
import hmac

from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send

from app.configs import settings


class ValidSignatureMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
        else:
            request = Request(scope)
            if request.method == "POST":
                timestamp = request.headers["X-Slack-Request-Timestamp"]
                signature = request.headers["X-Slack-Signature"]
                body = await request.body()
                if signature != self.calculate_signature(timestamp=timestamp, body=body):
                    raise HTTPException(status_code=403, detail="Invalid slack signature")
            await self.app(scope, receive, send)

    @staticmethod
    def calculate_signature(*, timestamp: str, body: bytes) -> str:
        signature = f"v0:{timestamp}:{body.decode('utf-8')}".encode()
        secret = settings.SLACK_SIGNING_SECRET.encode()
        return f"v0={hmac.new(secret, signature, hashlib.sha256).hexdigest()}"
