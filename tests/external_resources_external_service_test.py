from pathlib import Path
from typing import Any

from pydantic import BaseModel
from pydantic import Schema
from starlette.testclient import TestClient

from fastapi_serviceutils import make_app
from fastapi_serviceutils.utils.external_resources.services import call_service

app = make_app(
    config_path=Path('tests/configs/config.yml'),
    version='0.1.0',
    endpoints=[],
    enable_middlewares=[],
    additional_middlewares=[],
)


class ExampleModel(BaseModel):
    args: dict
    data: str
    files: dict
    form: dict
    headers: dict
    origin: str
    url: str
    json_: Any = Schema(None, alias='json')


@app.post('/test')
async def serviceendpoint():
    url = app.services['testservice'].url
    response = await call_service(url=url, params=None, model=ExampleModel)
    return response


def test_call_rest_service():
    """Test if endpoint "/api/alive/" works as expected."""
    with TestClient(app) as client:
        response = client.post('/test')
    assert ExampleModel.parse_obj(response.json())
