"""Available handlers for services based on fastapi_serviceutils."""
import traceback
from typing import Union

from fastapi.exception_handlers import http_exception_handler
from loguru import logger
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette.responses import Response

from fastapi_serviceutils.app import create_request_id


async def log_exception_handler(
        request: Request,
        exc: Union[StarletteHTTPException,
                   Exception]
) -> Response:
    """Add log of exception if an exception occur."""
    # add the request_id to the logger to be able to understand what request
    # caused the exception
    log = logger.bind(request_id=create_request_id(request))

    if isinstance(exc, StarletteHTTPException):
        # do not log exception for wrong endpoints
        if exc.status_code != 404:
            log.error(
                'following error occurred: {detail}. {error}'.format(
                    detail=exc.detail,
                    error=repr(exc)
                )
            )
        return await http_exception_handler(request, exc)

    # if not already a StarletteHTTPException, convert the exception to it
    _exception = StarletteHTTPException(
        status_code=500,
        detail=traceback.format_exc().split('\n')
    )
    log.error(
        f'{_exception.detail}\n '
        f'request from {request.client} to url {request.url}'
    )
    return await http_exception_handler(request, _exception)


__all__ = [
    'log_exception_handler',
]
