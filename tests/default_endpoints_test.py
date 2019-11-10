from pathlib import Path

from fastapi_serviceutils import make_app
from fastapi_serviceutils.app import Config
from fastapi_serviceutils.utils.tests.endpoints import json_endpoint

app = make_app(
    config_path=Path('tests/configs/config.yml'),
    version='0.1.0',
    endpoints=[],
    enable_middlewares=[],
    additional_middlewares=[],
)


def test_endpoint_alive():
    """Test if endpoint "/api/alive/" works as expected."""
    json_endpoint(
        application=app,
        endpoint='/api/alive/',
        expected={'alive': True}
    )


def test_endpoint_config():
    """Test if endpoint "/api/config/" works as expected."""
    result = json_endpoint(application=app, endpoint='/api/config/')
    print(result)
    assert isinstance(Config.parse_obj(result), Config)
