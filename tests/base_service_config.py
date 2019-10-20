from pathlib import Path

from fastapi_serviceutils.base import collect_config_definition
from fastapi_serviceutils.base import Config


def test_collect_config_definition():
    config_path = Path('tests/config.yml')
    config = collect_config_definition(config_path=config_path)
    assert isinstance(config, Config)
