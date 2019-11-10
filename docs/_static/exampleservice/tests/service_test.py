import pytest
from app.main import app

from fastapi_serviceutils.app.service_config import Config
from fastapi_serviceutils.utils.tests.endpoints import json_endpoint


def test_endpoint_example():
    json_endpoint(
        application=app,
        endpoint='/api/v1/example/',
        payload={'msg': 'test'},
        expected={'msg': 'test'}
    )


@pytest.mark.parametrize(
    'endpoint, status_code',
    [
        ('/api/v1/example',
         307),
        ('/api/',
         404),
        ('/api/v1/',
         404),
        ('/api/v1/example/',
         200),
    ]
)
def test_endpoint_invalid(endpoint, status_code):
    json_endpoint(
        application=app,
        endpoint=endpoint,
        status_code=status_code,
        payload={'msg': 'test'}
    )
