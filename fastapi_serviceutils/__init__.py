"""Contain utils for fastapi based services.

This contains:

* optimized logging using Loguru
* optimized exception handling by additional exception handler
  log_exception handler
* usage of a config.yml-file to configure the service
* usage of environment-variables (Environment variable overwrites config-value)
  to configure the service
* easily serve the apidoc with the service
* easy deploment using Docker combined with Docker compose
* fast creation of new service with create_service
* Makefile and Tmuxp-config for easier development of services based on
  fastapi-serviceutils using Make and tmux-session

This module defines the function :func:`make_app` to create an app containing
the above mentioned features.
"""
from pathlib import Path
from typing import List

from fastapi import FastAPI
from starlette.middleware.trustedhost import TrustedHostMiddleware

from .app import collect_config_definition
from .app import Config
from .app import customize_logging
from .app import Endpoint
from .app import update_config
from .app.endpoints import add_default_endpoints
from .app.handlers import log_exception_handler
from .utils.docs import mount_apidoc
from .utils.external_resources.dbs import add_databases_to_app
from .utils.external_resources.services import add_services_to_app

__version__ = '2.0.0'


def include_endpoints_and_middlewares_to_app(
        app: FastAPI,
        endpoints: List[Endpoint],
        enable_middlewares: List[str],
        additional_middlewares: list
) -> FastAPI:
    """Include endpoints and middlewares (and defaults) to app.

    Note:
        :func:`log_exception_handler` is not really a middleware but if
        it should be enabled, ``'log_exception'`` should be included in
        ``enable_middlewares``.

    Note:
        A router included by this function has additional attributes:

        * ``router.mode``
        * ``router.config``
        * ``router.logger``
        * ``router.databases``
        * ``router.services``

    Parameters:
        app: the app to add the endpoints and middlewares.
        endpoints: the endpoints to include into the app.
        enable_middlewares: the default middlewares to enable.
        additional_middlewares: additional middlewares to add to the app.

    Returns:
        the modified app containing the endpoints, middlewares and handlers.

    """
    # iterate over endpoints, define additional attributes required inside the
    # endpoints and include the endpoint to the router of the app.
    for endpoint in endpoints:
        endpoint.router.mode = app.mode
        endpoint.router.config = app.config
        endpoint.router.logger = app.logger
        endpoint.router.databases = app.databases
        endpoint.router.services = app.services
        if endpoint.tags:
            app.include_router(
                endpoint.router,
                prefix=endpoint.route,
                tags=endpoint.tags
            )
        else:
            app.include_router(endpoint.router, prefix=endpoint.route)

    # add the apidoc to app
    if app.config.service.apidoc_dir:
        mount_apidoc(app=app)

    # add middleware to be able to limit access to service to specific hosts
    if 'trusted_hosts' in enable_middlewares:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=app.config.service.allowed_hosts
        )

    # add custom exception handler to log exceptions
    if 'log_exception' in enable_middlewares:
        app.exception_handler(Exception)(log_exception_handler)

    # add additional defined middlewares
    # TODO: in future releases the addition of more complex middlewares should
    # be possible
    for middleware in additional_middlewares:
        app.add_middleware(middleware)

    return app


def make_app(
        config_path: Path,
        version: str,
        endpoints: List[Endpoint],
        enable_middlewares: List[str],
        additional_middlewares: list,
) -> FastAPI:
    """Create app with endpoints and middlewares.

    App is configured using the config of the service and defined
    environment-variables.
    Also logger is configured and default endpoints and additional endpoints
    added.
    Same for middlewares.

    Note:
        An app created by this function has additional attributes:

        * ``app.logger``
        * ``app.config``
        * ``app.databases``
        * ``app.services``
        * ``app.mode``

    Parameters:
        config_path: the path for the config file to use for the app.
        version: current version of the service, should be ``__version__``
            variable inside the module ``app`` of your service.
        endpoints: the endpoints to include to the app.
        enable_middlewares: list of the middlewares to add.
        additional_middlewares: list of non default middlewares to add to the
            app.

    Returns:
        the created app.

    """
    # load the config and environment-variables for the service and
    # combine these information to initialize the app
    config = collect_config_definition(config_path=config_path)

    # update mode and logger-definitions with environment-variables if defined
    # ATTENTION: the environment-variable has the prefix of the servicename
    config = update_config(
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

    # add additional attributes to the app like the config and the runtime-mode
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

    # if dependencies for external databases are defined in the config, add
    # these database-definitions to the app
    if config.external_resources.databases:
        app = add_databases_to_app(
            app,
            dbs=config.external_resources.databases
        )
    else:
        app.databases = {}

    # if dependencies for external services are defined in the config, add
    # these service-definitions to the app
    if config.external_resources.services:
        app = add_services_to_app(
            app,
            services=config.external_resources.services
        )
    else:
        app.services = {}

    # add default endpoints if defined in the config
    endpoints = add_default_endpoints(endpoints=endpoints, config=app.config)

    # include defined routers and middlewares to the app
    return include_endpoints_and_middlewares_to_app(
        app=app,
        endpoints=endpoints,
        enable_middlewares=enable_middlewares,
        additional_middlewares=additional_middlewares
    )


__all__ = ['make_app', 'include_endpoints_and_middlewares_to_app']
