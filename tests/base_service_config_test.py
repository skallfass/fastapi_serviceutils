from pathlib import Path

import pytest
from pydantic import ValidationError

from fastapi_serviceutils.app import collect_config_definition
from fastapi_serviceutils.app import Config


@pytest.mark.parametrize(
    'config_path',
    [
        'tests/configs/config.yml',
        'tests/configs/config2.yml',
        'tests/configs/config3.yml',
    ]
)
def test_collect_config_definition(config_path):
    config_path = Path(config_path)
    config = collect_config_definition(config_path=config_path)
    assert isinstance(config, Config)


@pytest.mark.parametrize(
    'config_path',
    [
        'tests/invalid_configs/invalid_config.yml',
        'tests/invalid_configs/invalid_config2.yml',
        'tests/invalid_configs/invalid_config3.yml',
        'tests/invalid_configs/invalid_config4.yml',
        'tests/invalid_configs/invalid_config5.yml',
        'tests/invalid_configs/invalid_config6.yml',
        'tests/invalid_configs/invalid_config7.yml',
        'tests/invalid_configs/invalid_config8.yml',
        'tests/invalid_configs/invalid_config9.yml',
        'tests/invalid_configs/invalid_config10.yml',
        'tests/invalid_configs/invalid_config11.yml',
        'tests/invalid_configs/invalid_config12.yml',
        'tests/invalid_configs/invalid_config13.yml',
        'tests/invalid_configs/invalid_config14.yml',
        'tests/invalid_configs/invalid_config15.yml',
        'tests/invalid_configs/invalid_config16.yml',
        'tests/invalid_configs/invalid_config17.yml',
        'tests/invalid_configs/invalid_config18.yml',
        'tests/invalid_configs/invalid_config19.yml',
        'tests/invalid_configs/invalid_config20.yml',
    ]
)
def test_collect_config_definition_invalid(config_path):
    config_path = Path(config_path)
    with pytest.raises(ValidationError):
        collect_config_definition(config_path=config_path)
