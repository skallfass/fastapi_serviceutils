"""Endpoint registration and configuration helpers.

Also includes default endpoint handling.
"""
import copy
from typing import List

from fastapi_serviceutils.app import Endpoint
from fastapi_serviceutils.app.endpoints.default import alive as alive_endpoint
from fastapi_serviceutils.app.endpoints.default import config as config_endpoint
from fastapi_serviceutils.app.service_config import Config


def set_version_endpoints(
        endpoints: List[Endpoint],
        version: str,
        prefix_template: str,
        **kwargs: dict
) -> List[Endpoint]:
    """Configures the endpoints inside a version-module.

    Modify the route to the correct route using the ``route``-attribute of
    each endpoint and modify it using the passed prefix_template in
    combination with the passed kwargs.

    Also used to set the ``'latest'`` endpoints.

    Parameters:
        endpoints: the endpoints to set the version and correct route.
        version: the version to set for the endpoints.
        prefix_template: the template to use for the resulting route.
        kwargs: additional kwargs required by the prefix_template. As default
            the following keys inside kwargs are already set:

            * ``route``
            * ``version``

            So these can already be used inside the prefix_template.

    Returns:
        the resulting endpoints.

    """
    version_endpoints = []
    if not kwargs:
        kwargs = {}
    else:
        kwargs = copy.deepcopy(kwargs)

    for endpoint_definition in endpoints:
        if isinstance(endpoint_definition, Endpoint):
            endpoint = Endpoint(
                route=endpoint_definition.route,
                router=endpoint_definition.router,
                version=endpoint_definition.version
            )
        else:
            endpoint = Endpoint(
                route=endpoint_definition.ENDPOINT.route,
                router=endpoint_definition.ENDPOINT.router,
                version=endpoint_definition.ENDPOINT.version
            )
        endpoint.tags = [version]
        if version == 'latest':
            route = endpoint.route.replace(
                endpoint_definition.version,
                version
            )
        else:
            route = endpoint.route
        kwargs.update({'route': route, 'version': version})
        endpoint.version = version
        endpoint.route = prefix_template.format(**kwargs)
        version_endpoints.append(endpoint)
    return version_endpoints


def add_default_endpoints(endpoints: List[Endpoint],
                          config: Config) -> List[Endpoint]:
    """Add default endpoints to existing endpoints.

    Currently the following default-endpoints are available:

    * ``'alive``
    * ``'config'``

    Parameters:
        endpoints: the already set endpoints to add the default ones.
        config: the config of the service to extract the information which
            default-endpoints to add.

    Returns:
        the passed endpoints with added default endpoints.

    """
    default_endpoints = {
        'alive': alive_endpoint.ENDPOINT,
        'config': config_endpoint.ENDPOINT
    }

    for endpoint in config.service.use_default_endpoints:
        current = default_endpoints[endpoint]
        current.tags = ['status']
        endpoints.append(current)
    return endpoints


__all__ = ['add_default_endpoints', 'set_version_endpoints']
