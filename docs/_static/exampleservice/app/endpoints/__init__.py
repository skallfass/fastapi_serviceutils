from app.endpoints.v1 import ENDPOINTS as v1

from fastapi_serviceutils.app.endpoints import set_version_endpoints

LATEST = set_version_endpoints(
    endpoints=v1,
    version='latest',
    prefix_template='{route}'
)

ENDPOINTS = LATEST + v1

__all__ = ['ENDPOINTS']
