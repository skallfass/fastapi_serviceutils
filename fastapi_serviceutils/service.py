"""Create service-apps."""
from pathlib import Path
from typing import Dict
from typing import List
from typing import Union

from fastapi import APIRouter
from fastapi import FastAPI
from starlette.middleware.trustedhost import TrustedHostMiddleware

from fastapi_serviceutils.base import collect_config_definition
from fastapi_serviceutils.base import Config
from fastapi_serviceutils.base import customize_logging
from fastapi_serviceutils.base import errors
from fastapi_serviceutils.base import update_config
from fastapi_serviceutils.default_endpoints import add_default_endpoints
from fastapi_serviceutils.docs import mount_apidoc
from fastapi_serviceutils.middlewares import prometheus

Endpoints = List[Dict[str, Union[APIRouter, str]]]


def include_endpoints_and_middlewares_to_app(
        app: FastAPI,
        endpoints: Endpoints,
        enable_middlewares: List[str],
        additional_middlewares: list
) -> FastAPI:
    """Include passed endpoints and passed middlewares (and defaults) to app.

    Note:
        :func:`errors.log_exception_handler` is not really a middleware but if
        it should be enabled, ``'log_exception'`` should be included in
        ``enable_middlewares``.

    Parameters:
        app: the app to add the endpoints and middlewares.
        endpoints: the endpoints to include into the app.
        enable_middlewares: the default middlewares to enable.
        additional_middlewares: additional middlewares to add to the app.

    Returns:
        the modified app.

    """
    for endpoint in endpoints:
        endpoint['router'].mode = app.mode
        endpoint['router'].config = app.config
        endpoint['router'].logger = app.logger
        app.include_router(endpoint['router'], prefix=endpoint['prefix'])

    # add the apidoc to app
    if app.config.service.apidoc_dir:
        mount_apidoc(app=app)

    # add middleware to be able to limit access to service to specific hosts
    if 'trusted_hosts' in enable_middlewares:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=app.config.service.allowed_hosts
        )

    # add exposing of metrics for prometheus monitoring
    if app.config.service.use_prometheus:
        app.add_middleware(prometheus.PrometheusMiddleware)
        app.add_route('/metrics/', prometheus.metrics)

    # add custom exception handler to log exceptions
    if 'log_exception' in enable_middlewares:
        app.exception_handler(Exception)(errors.log_exception_handler)

    for middleware in additional_middlewares:
        app.add_middleware(middleware)

    return app


def make_app(
        config_path: Path,
        version: str,
        endpoints: Endpoints,
        enable_middlewares: List[str],
        additional_middlewares: list
) -> FastAPI:
    """Create app with endpoints and middlewares.

    App is configured using the config of the service and defined
    environment-variables.
    Also logger is configured and default endpoints and additional endpoints
    added. Same for middlewares.
    """
    # load the config and environment-variables for the service and
    # combine these information to initialize the app
    config = collect_config_definition(config_path=config_path)
    servicename = config.service.name.upper()

    # update mode and logger-definitions with environment-variables if defined
    # ATTENTION: the environment-variable has the prefix of the servicename
    config = update_config(
        servicename=servicename,
        env_vars=config.available_environment_variables.env_vars,
        external_resources_env_vars=(
            config.available_environment_variables.external_resources_env_vars
        ),
        rules_env_vars=config.available_environment_variables.rules_env_vars,
        config=config,
        model=Config,
    )

    # convert config-attribute types if necessary
    config.logger.path = Path(config.logger.path)
    config.service.readme = Path(config.service.readme)

    # initialize the app, add combined configuration, mode and logger
    app = FastAPI(
        title=f'{config.service.name} [{config.service.mode.upper()}]',
        description=config.service.readme.read_text(),
        version=version,
    )
    app.config = config
    app.mode = config.service.mode

    # Set the logging-configuration
    app.logger = customize_logging(
        config.logger.path / config.logger.filename.format(mode=app.mode),
        level=config.logger.level,
        retention=config.logger.retention,
        rotation=config.logger.rotation,
        _format=config.logger.format
    )

    # include defined routers and middlewares to the app
    endpoints = add_default_endpoints(endpoints=endpoints, config=app.config)
    app = include_endpoints_and_middlewares_to_app(
        app=app,
        endpoints=endpoints,
        enable_middlewares=enable_middlewares,
        additional_middlewares=additional_middlewares
    )
    return app


__all__ = ['include_endpoints_and_middlewares_to_app', 'make_app', 'Endpoints']
