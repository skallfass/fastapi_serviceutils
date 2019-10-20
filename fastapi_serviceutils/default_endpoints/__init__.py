"""Contain endpoints to be added as routes inside all fastapi-based service."""
from typing import Dict
from typing import List
from typing import Union

from fastapi import APIRouter

from fastapi_serviceutils.base import Config
from fastapi_serviceutils.default_endpoints import alive as alive_endpoint
from fastapi_serviceutils.default_endpoints import config as config_endpoint


def add_default_endpoints(
        endpoints: List[Dict[str,
                             Union[APIRouter,
                                   str]]],
        config: Config
) -> List[Dict[str,
               Union[APIRouter,
                     str]]]:
    """Add default endpoints to existing endpoints."""
    default_endpoints = {
        'alive': {
            'router': alive_endpoint.ROUTER,
            'prefix': alive_endpoint.PREFIX
        },
        'config': {
            'router': config_endpoint.ROUTER,
            'prefix': config_endpoint.PREFIX
        },
    }

    for endpoint in config.service.use_default_endpoints:
        endpoints.append(default_endpoints[endpoint])
    return endpoints


__all__ = [
    'add_default_endpoints',
]
