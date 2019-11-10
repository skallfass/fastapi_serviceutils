from app.endpoints.v1 import example

from fastapi_serviceutils.app.endpoints import set_version_endpoints

ENDPOINTS = set_version_endpoints(
    endpoints=[example],
    version='v1',
    prefix_template='/api/{version}{route}'
)

__all__ = ['ENDPOINTS']
