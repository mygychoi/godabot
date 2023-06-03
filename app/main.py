from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.staticfiles import StaticFiles

from app import access, home, slashcommand
from app.configs import settings
from app.core.database.pool import PoolManager
from app.core.middleware import ValidSignatureMiddleware

godabot = FastAPI(
    title=settings.NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    contact=settings.AUTHORS[0],
    license_info={"name": settings.LICENSE},
    terms_of_service=settings.TERMS,
    debug=settings.DEBUG,
    docs_url=settings.DOCS_URL,
    openapi_url=settings.OPENAPI_URL,
    lifespan=PoolManager.initiate,
)

# Middlewares
if settings.ENV == settings.PROD:
    godabot.add_middleware(HTTPSRedirectMiddleware)
    godabot.add_middleware(ValidSignatureMiddleware)

# Static
godabot.mount("/static", StaticFiles(directory="static"), name="static")

# Domains
godabot.include_router(router=home.router)
godabot.include_router(router=access.router)
godabot.include_router(router=slashcommand.router)
