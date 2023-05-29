"""Depends on slack authentication
refer to https://api.slack.com/authentication/verifying-requests-from-slack
"""

import hashlib
import hmac

from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.configs import settings


def calculate_signature(*, timestamp: str, body: bytes) -> str:
    signature = f"v0:{timestamp}:{body.decode('utf-8')}".encode()
    secret = settings.SLACK_SIGNING_SECRET.encode()
    return f"v0={hmac.new(secret, signature, hashlib.sha256).hexdigest()}"


class ValidSignatureMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.method == "POST":
            timestamp = request.headers["X-Slack-Request-Timestamp"]
            signature = request.headers["X-Slack-Signature"]
            import logging

            calculated = calculate_signature(timestamp=timestamp, body=await request.body())
            logging.error(f"{signature}, {calculated}")
            if signature != calculated:
                raise HTTPException(status_code=404, detail="Invalid slack signature")
            response = await call_next(request)
            return response
        return await call_next(request)
