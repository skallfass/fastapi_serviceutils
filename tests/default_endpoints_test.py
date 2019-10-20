from pathlib import Path

import pytest
from starlette.testclient import TestClient

from fastapi_serviceutils.base import Config
from fastapi_serviceutils.service import make_app


def _app():
    return make_app(
        config_path=Path('tests/config.yml'),
        version='0.1.0',
        endpoints=[],
        enable_middlewares=[],
        additional_middlewares=[],
    )

CLIENT = TestClient(_app())


@pytest.mark.parametrize(
    'expected, endpoint',
    [({
        'alive': True
    },
      '/api/alive/')]
)
def test_endpoint_alive(expected, endpoint):
    """Test if endpoint "/api/alive/" works as expected."""
    response = CLIENT.post(endpoint)
    assert response.status_code == 200
    result = response.json()
    assert result == expected


@pytest.mark.parametrize('endpoint', ['/api/config/'])
def test_endpoint_config(endpoint):
    """Test if endpoint "/api/config/" works as expected."""
    response = CLIENT.post(endpoint)
    assert response.status_code == 200
    result = response.json()
    print(result)
    assert isinstance(Config.parse_obj(result), Config)
