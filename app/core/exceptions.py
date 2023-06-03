import logging

from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError

from app.main import godabot


@godabot.exception_handler(RequestValidationError)
async def log_request_validation_error(request, exc):
    logging.error(exc)
    return await request_validation_exception_handler(request, exc)
