from fastapi import FastAPI

from app import access
from app.configs import settings
from app.core.database.pool import PoolManager
from app.core.middleware import TrustedRequestMiddleware

godabot = FastAPI(
    title=settings.NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    contact=settings.AUTHORS[0],
    license_info={"name": settings.LICENSE},
    terms_of_service="",  # TODO: Add url later
    debug=settings.DEBUG,
    openapi_url="/openapi.json" if settings.DEBUG else None,
    lifespan=PoolManager.initiate,
)

# Middlewares
if not settings.DEBUG:
    godabot.add_middleware(TrustedRequestMiddleware)

# Domains
godabot.include_router(router=access.routers.router)

if settings.DEBUG:
    from tests import test_database

    godabot.include_router(router=test_database.routers.router)
