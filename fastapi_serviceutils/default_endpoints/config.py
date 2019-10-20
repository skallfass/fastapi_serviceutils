"""Endpoint to return currently used configuration of the service."""
from fastapi import APIRouter

from fastapi_serviceutils.base import Config

ROUTER = APIRouter()
PREFIX = '/api/config'
TAGS = ['status']


@ROUTER.post(
    '/',
    response_model=Config,
    summary='Get currently used config.',
    tags=TAGS,
)
async def get_config() -> Config:
    """Get currently used config of the service.

    Returns:
        the content of the currently used config.

    """
    return Config.parse_raw(ROUTER.config.json())
