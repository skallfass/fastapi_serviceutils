"""Endpoint to check if service is alive."""
from fastapi import APIRouter
from starlette.requests import Request

from fastapi_serviceutils.app import create_id_logger
from fastapi_serviceutils.app import Endpoint
from fastapi_serviceutils.app.endpoints.default.models import Alive

ENDPOINT = Endpoint(router=APIRouter(), route='/api/alive')
SUMMARY = 'Check if service is alive.'


@ENDPOINT.router.post('/', response_model=Alive, summary=SUMMARY)
async def alive(request: Request) -> Alive:
    """Check if service is alive.

    Returns:
        the information that the service is alive.

    """
    _, log = create_id_logger(request=request, endpoint=ENDPOINT)
    log.debug(f'received request for endpoint {request.url}.')
    return Alive(alive=True)
