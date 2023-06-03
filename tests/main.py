from app.configs import settings
from app.main import godabot
from tests.test_core import test_database

if settings.ENV == settings.DEV:
    godabot.include_router(router=test_database.router)
