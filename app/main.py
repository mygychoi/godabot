import openai
import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from sentry_sdk.integrations.fastapi import FastApiIntegration

from app import access, slashcommand
from app.configs import settings
from app.core.database.pool import PoolManager
from app.core.middleware import TrustedRequestMiddleware

openai.api_key = settings.OPENAI_API_KEY
openai.organization = settings.OPENAI_ORGANIZATION

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    traces_sample_rate=0.2,
    integrations=[FastApiIntegration(transaction_style="url")],
    environment=settings.ENV.value,
)

godabot = FastAPI(
    title=settings.NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    contact=settings.AUTHORS[0],
    license_info={"name": settings.LICENSE},
    terms_of_service="",  # TODO: Add url later
    debug=settings.DEBUG,
    openapi_url="/openapi.json" if settings.ENV == settings.DEV else None,
    lifespan=PoolManager.initiate,
)

# Middlewares
if settings.ENV == settings.PROD:
    godabot.add_middleware(HTTPSRedirectMiddleware)
    godabot.add_middleware(TrustedRequestMiddleware)

# Domains
godabot.include_router(router=access.router)
godabot.include_router(router=slashcommand.router)

# Tests
if settings.ENV == settings.DEV:
    from tests import test_database

    godabot.include_router(router=test_database.routers.router)
