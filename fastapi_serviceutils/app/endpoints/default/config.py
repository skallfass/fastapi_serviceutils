"""Endpoint to return currently used configuration of the service."""
from fastapi import APIRouter
from starlette.requests import Request

from fastapi_serviceutils.app import Config
from fastapi_serviceutils.app import create_id_logger
from fastapi_serviceutils.app import Endpoint

ENDPOINT = Endpoint(router=APIRouter(), route='/api/config')
SUMMARY = 'Get currently used config.'


@ENDPOINT.router.post('/', response_model=Config, summary=SUMMARY)
async def get_config(request: Request) -> Config:
    """Get currently used config of the service.

    Returns:
        the content of the currently used config.

    """
    _, log = create_id_logger(request=request, endpoint=ENDPOINT)
    log.debug(f'received request for endpoint {request.url}.')
    return Config.parse_raw(ENDPOINT.router.config.json())
