"""Depends on slack authentication
refer to https://api.slack.com/authentication/verifying-requests-from-slack
"""

import hashlib
import hmac

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.configs import settings

FORBIDDEN = Response(status_code=403)


def calculate_signature(*, timestamp: str, body: bytes) -> str:
    signature = f"v0:{timestamp}:{body.decode('utf-8')}".encode()
    secret = settings.SLACK_SIGNING_SECRET.encode()
    return f"v0={hmac.new(secret, signature, hashlib.sha256).hexdigest()}"


class TrustedRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        import logging

        logger = logging.getLogger(__name__)
        body = await request.body()
        logger.error(body.decode("utf-8"))
        """TODO: research about"""
        timestamp = request.headers.get("X-Slack-Request-Timestamp")
        signature = request.headers.get("X-Slack-Signature")
        if timestamp is None or signature is None:
            return FORBIDDEN
        else:
            if signature != calculate_signature(timestamp=timestamp, body=await request.body()):
                return FORBIDDEN
            return await call_next(request)
