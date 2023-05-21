import openai
import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from app import access, slashcommand
from app.configs import settings
from app.core.database.pool import PoolManager
from app.core.middleware import TrustedRequestMiddleware

openai.api_key = settings.OPENAI_API_KEY
openai.organization = settings.OPENAI_ORGANIZATION

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    traces_sample_rate=0.05,
    integrations=[
        StarletteIntegration(transaction_style="endpoint"),
        FastApiIntegration(transaction_style="endpoint"),
    ],
    environment=settings.ENVIRONMENT,
)

godabot = FastAPI(
    title=settings.NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    contact=settings.AUTHORS[0],
    license_info={"name": settings.LICENSE},
    terms_of_service="",  # TODO: Add url later
    debug=settings.DEBUG,
    openapi_url="/openapi.json" if settings.ENVIRONMENT == settings.ENVIRONMENT.DEV else None,
    lifespan=PoolManager.initiate,
)

# Middlewares
if settings.ENVIRONMENT != settings.ENVIRONMENT.DEV:
    godabot.add_middleware(HTTPSRedirectMiddleware)
    godabot.add_middleware(TrustedRequestMiddleware)

# Domains
godabot.include_router(router=access.router)
godabot.include_router(router=slashcommand.router)

# Tests
if settings.ENVIRONMENT == settings.ENVIRONMENT.DEV:
    from tests import test_database

    godabot.include_router(router=test_database.routers.router)

    @godabot.get("/test")
    def test():
        return 1 / 0
