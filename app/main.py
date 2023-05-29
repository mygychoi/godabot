import logging

from fastapi import FastAPI
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from app import access, home, slashcommand
from app.configs import settings
from app.core.database.pool import PoolManager
from app.core.middleware import TrustedRequestMiddleware

godabot = FastAPI(
    title=settings.NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    contact=settings.AUTHORS[0],
    license_info={"name": settings.LICENSE},
    terms_of_service=settings.TERMS,
    debug=settings.DEBUG,
    docs_url="/docs" if settings.ENV == settings.DEV else None,
    lifespan=PoolManager.initiate,
)

# Middlewares
godabot.add_middleware(HTTPSRedirectMiddleware)
godabot.add_middleware(TrustedRequestMiddleware)


# Logging
@godabot.exception_handler(RequestValidationError)
async def log_request_validation_error(request, exc):
    logging.error(exc)
    return await request_validation_exception_handler(request, exc)


# Domains
godabot.include_router(router=access.router)
godabot.include_router(router=slashcommand.router)
godabot.mount(path="/", app=home.app)

# Tests
if settings.ENV == settings.DEV:
    from tests import test_database

    godabot.include_router(router=test_database.routers.router)
