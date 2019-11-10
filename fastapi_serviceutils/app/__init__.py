"""Helpers for fastapi-app especially the endpoint-functions.

Inside endpoints defined using fastapi-serviceutils the variable ``ENDPOINTS``
should be defined as an instance of :class:`Endpoint`.

For better traceback inside the logs :func:`create_id_logger` is used inside
the endpoint-function.
"""
from dataclasses import dataclass
from typing import List

from fastapi import APIRouter
from loguru._logger import Logger
from starlette.requests import Request

from .logger import customize_logging
from .service_config import collect_config_definition
from .service_config import Config
from .service_config import update_config


@dataclass
class Endpoint:
    """Endpoint as required inside each endpoint module.

    Attributes:
        router: the router for this endpoint.
        route: the route to this endpoint (is modified for the app using
            function
            :func:`fastapi_serviceutils.app.endpoints.set_version_endpoints`).
        tags: the tags for the endpoint (used for swagger-documentation).
        version: the version of the endpoint.

    """
    router: APIRouter
    route: str
    tags: List[str] = None
    version: str = None


def create_request_id(request: Request):
    """Create a request-id baed on the attributes of the passed request.

    Parameters:
        request: the request to create the id for.

    Returns:
        the request-id.

    """
    return abs(hash(f'{request.client}{request.headers}{request.body}'))


def create_id_logger(
        request: Request,
        endpoint: Endpoint,
) -> [int,
      Logger]:
    """Create the request-id and the request-specific logger.

    This function is meant to be used inside an endpoint-function to be able
    to use a unique request-id in each request for better traceback in the
    logs.

    Parameters:
        request: the request to create id and logger.
        endpoint: the endpoint to extract the logger-function.

    Returns:
        the request-id and the customized logger.

    """
    request_id = create_request_id(request)
    log = endpoint.router.logger.bind(request_id=request_id)
    return request_id, log


__all__ = [
    'collect_config_definition',
    'Config',
    'create_id_logger',
    'create_request_id',
    'customize_logging',
    'update_config',
]
