"""Endpoint to check if service is alive."""
from fastapi import APIRouter

from fastapi_serviceutils.default_endpoints.models import Alive

ROUTER = APIRouter()
PREFIX = '/api/alive'
TAGS = ['status']


@ROUTER.post(
    '/',
    response_model=Alive,
    summary='Check if service is alive.',
    tags=TAGS,
)
async def alive() -> Alive:
    """Check if service is alive.

    Returns:
        the information that the service is alive.

    """
    return Alive(alive=True)
