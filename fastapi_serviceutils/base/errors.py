"""Exception handlers and other exception related functions, classes."""
import logging
import traceback

from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException


async def log_exception_handler(request, exc):
    """Add log of exception if a :class:`StarletteHTTPException` occur."""
    if isinstance(exc, StarletteHTTPException):
        if exc.status_code != 404:
            logging.error(
                'following error occurred: {detail}. {error}'.format(
                    detail=exc.detail,
                    error=repr(exc)
                )
            )
    else:
        logging.error(
            f'{traceback.format_exc()}\n '
            f'request from {request.client} to url {request.url}'
        )
    return await http_exception_handler(request, exc)


__all__ = [
    'log_exception_handler',
]
