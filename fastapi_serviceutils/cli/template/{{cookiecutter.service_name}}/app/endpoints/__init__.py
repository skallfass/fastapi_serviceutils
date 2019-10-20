"""Define routers to be available as endpoints in the service."""
from app.endpoints.v1 import {{cookiecutter.endpoint}}


ENDPOINTS = [
    {'router': epoint.ROUTER, 'prefix': epoint.PREFIX} for epoint in [{{cookiecutter.endpoint}}]
]

__all__ = ['ENDPOINTS']
