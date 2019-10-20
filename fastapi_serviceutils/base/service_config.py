"""Collect config for service and convert to instance of :class:`Config`."""
import copy
import os
from pathlib import Path
from typing import List
from typing import Union

import yaml
from pydantic import BaseModel
from toolz.dicttoolz import update_in


class AvailableEnvironmentVariables(BaseModel):
    """Represent section of available environment variables in config."""
    env_vars: List[str]
    external_resources_env_vars: List[str]
    rules_env_vars: List[str]


class ServiceConfig(BaseModel):
    """Represent configuration of the service inside the config.

    Attributes:
        name: the name of the service.
        mode: the runtime-mode of the service.
        development_port: port to use for service during development.
        description: short description of the service.
        documentation_dir: path where the documentation dir for the apidoc
            is located.
        readme: path to the readme-file to integrate into the
            swagger-documentation.

    """
    name: str
    mode: str
    development_port: int
    description: str
    apidoc_dir: str
    readme: str
    allowed_hosts: List[str]
    use_prometheus: bool
    use_default_endpoints: List[str]


class LoggerConfig(BaseModel):
    """Represent configuration of logger inside the config.

    Attributes:
        path: folder where the log-files should be saved.
        filename: the name of the log-file to use.
        level: the minimum log-level to log.
        rotation: when to rotate the log-file.
        retention: how long to keep log-files.
        format: log-format to use.

    """
    path: str
    filename: str
    level: str
    rotation: str
    retention: str
    format: str


class Config(BaseModel):
    """Represent config-content to configure service and its components.

    Attributes:
        service: general information about service, like name, where to find
            the readme, documentation-dir, etc.
        logger: configuration for the logger of the service.
        external_resources: if service depends on external-resources,
            this includes for example the url of such a dependency, etc.
        rules: special rules for the service.

    """
    service: ServiceConfig
    logger: LoggerConfig
    available_environment_variables: AvailableEnvironmentVariables
    external_resources: dict = None
    rules: dict = None


def collect_config_definition(config_path: Path) -> Config:
    """Collect the config for the service.

    Then convert its content to an instance of :class:`Config`.

    Parameters:
        config_path: the path of the config-file to use.

    Returns:
        the content of the config-file converted to an instance of
        :class:`Config`.

    """
    cfg_content = yaml.safe_load(config_path.read_text())
    return Config(**cfg_content)


def _update_value_in_nested_dict_by_keylist(
        dictionary: dict,
        key_list: List[str],
        new_value
) -> dict:
    """Update the value of a nested-dictionary by a keylist with new value.

    Wrapper around :func:`toolz.dicttoolz.update_in`.

    Note:
        Do not update the original dict, returns a new dict with same content
        as original dict, but with update and required location.

    Parameters:
        dictionary: the dictionary to update.
        key_list: list of subkeys where to update the dictionary.
        new_value: the new value to update to.

    Returns:
        the updated dictionary.

    """
    temp = copy.deepcopy(dictionary)
    return update_in(temp, key_list, lambda x: new_value)


def _use_environment_variable_for_variable(
        config: Union[Config,
                      dict],
        keys: List[str],
        model: BaseModel,
        content_env_var: Union[str,
                               int,
                               float,
                               None],
) -> Union[BaseModel,
           dict]:
    """Overwrite config with value of environment-variable.

    To be able to overwrite the config it must be converted to a dict (if it is
    not already). After updating the value it has to be converted back to an
    instance of the passed ``model``.

    Parameters:
        config: the config to update.
        keys: sublevels for the config to set the value.
        model: the model to convert back the config after update.
        content_env_var: the content of the environment-variable.
        env_var_name: the name of the variable.

    Returns:
        the updated config.

    """
    if isinstance(config, dict):
        temp_config = copy.deepcopy(config)
    else:
        temp_config = copy.deepcopy(config.dict())

    temp_config = _update_value_in_nested_dict_by_keylist(
        dictionary=temp_config,
        key_list=keys,
        new_value=content_env_var
    )

    if model:
        return model.parse_obj(temp_config)

    return temp_config


def _update_config_with_environment_variables(
        servicename: str,
        environment_variable_names: List[str],
        config: Union[Config,
                      dict],
        model: BaseModel = None
) -> Union[BaseModel,
           dict]:
    """Update the config if environment-variables exist.

    If an environment variable exist, overwrite the value in the config with
    the value of the environment-variable.

    Finally store into ``info`` if original config-value is used or
    environment-variable.

    Parameters:
        servicename: the name of the service.
        environment_variable_name: the name of the environment-variable to
            check and use if set.
        config: the config containing the value to use / the config to
            overwrite with the value of the environment-variable.
        model: the model of the config to use.

    Returns:
        the updated config and the updated info_dict.

    """
    for environment_variable_name in environment_variable_names:
        env_var_name = f'{servicename}_{environment_variable_name}'
        keys = env_var_name.replace(f'{servicename}_', '').lower().split('__')
        content_env_var = os.environ.get(env_var_name)

        if content_env_var:
            # overwrite config with the value of the environment-variable
            config = _use_environment_variable_for_variable(
                config=config,
                keys=keys,
                model=model,
                content_env_var=content_env_var,
            )
    return config


def update_config(
        servicename: str,
        config: Config,
        model: BaseModel,
        env_vars: List[str] = None,
        external_resources_env_vars: List[str] = None,
        rules_env_vars: List[str] = None,
):
    """Update config with environment-variables if defined."""
    # update mode and logger-definitions with environment-variables if defined
    # ATTENTION: the environment-variable has the prefix of the servicename
    if env_vars:
        config = _update_config_with_environment_variables(
            servicename=servicename,
            environment_variable_names=env_vars,
            config=config,
            model=model,
        )

    # load special environment variables which can't be accessed by converting
    # the config to a dict.
    # ATTENTION: like above the environment-variable has the prefix of the
    # servicename
    if external_resources_env_vars:
        config.external_resources = _update_config_with_environment_variables(
            servicename=servicename,
            environment_variable_names=external_resources_env_vars,
            config=config.external_resources,
        )

    # load special environment variables which can't be accessed by converting
    # the config to a dict.
    # ATTENTION: like above the environment-variable has the prefix of the
    # servicename
    if rules_env_vars:
        config.rules = _update_config_with_environment_variables(
            servicename=servicename,
            environment_variable_names=rules_env_vars,
            config=config.rules,
        )
    return config


__all__ = [
    'collect_config_definition',
    'Config',
    'update_config',
]
