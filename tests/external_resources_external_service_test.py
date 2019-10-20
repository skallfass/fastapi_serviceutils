from fastapi_serviceutils.external_resources import call_rest_service
from typing import Any



from pathlib import Path

import pytest
from starlette.testclient import TestClient

from fastapi_serviceutils.default_endpoints.alive import Alive
from fastapi_serviceutils.service import make_app
from pydantic import BaseModel
from pydantic import Schema


def _app():
    return make_app(
        config_path=Path('tests/config.yml'),
        version='0.1.0',
        endpoints=[],
        enable_middlewares=[],
        additional_middlewares=[],
    )

CLIENT = TestClient(_app())


class TestModel(BaseModel):
    args: dict
    data: str
    files: dict
    form: dict
    headers: dict
    origin: str
    url: str
    json_: Any = Schema(None, alias='json')


@pytest.mark.parametrize(
    'params, url, model',
    [
        (
            None,
            'https://httpbin.org/post',
            TestModel
        )
    ]
)
@pytest.mark.asyncio
async def test_call_rest_service(params, url, model):
    """Test if endpoint "/api/alive/" works as expected."""
    response = await call_rest_service(url=url, params=params, model=TestModel)
    assert isinstance(response, TestModel)
