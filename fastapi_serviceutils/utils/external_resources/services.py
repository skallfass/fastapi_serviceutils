"""Interact with external services."""
import logging
from typing import Dict

import requests
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import ValidationError


class ServiceDefinition(BaseModel):
    """Definition for a service as defined in ``config.yml:external_resources``.

    Attributes:
        name: the name of the service.
        url: the url to the endpoint of the service.
        servicetype: the type of the service (currently only rest is
            supported.)

    """
    name: str
    url: str
    servicetype: str


async def _convert_response_to_model(
        model: BaseModel,
        response,
        info_msg: str
) -> BaseModel:
    """Extract request-result and convert it into an instance of ``model``.

    Parameters:
        model: the model to convert the service-result into.
        response: the result of the made service-call.
        info_msg: the message to return if something goes wrong during
            conversion to the model.

    Raises:
        if something goes wrong during conversion to the model a
        :class:`HTTPException` is raised.

    Returns:
        the service-call response converted to an instance of model.

    """
    try:
        result = response.json()
        return model.parse_obj(result)
    except ValidationError as error:
        raise HTTPException(
            status_code=500,
            detail=(
                f'{info_msg} => Invalid result: {response}. Error was {error}.'
            )
        )


async def _check_response_status(response, info_msg: str):
    """Check if the status of the response is valid.

    Parameters:
        response: the result of the made service-call.
        info_msg: the message to return if something goes wrong during
            service-call.

    Raises:
        if response has an invalid status-code a :class:`HTTPException` is
        raised.

    """
    try:
        response.raise_for_status()
    except requests.HTTPError as error:
        raise HTTPException(
            status_code=500,
            detail=f'{info_msg} => Could not make request. Error was {error}.'
        )


async def _make_external_rest_request(
        url: str,
        method: str,
        params: dict,
        info_msg: str
):
    """Request external service at ``url`` using ``method`` with ``params``.

    Parameters:
        url: the url to the service-endpoint to use.
        method: the service-method to use. Supported are ``get`` and ``post``.
        params: the request-params for the service-call.
        info_msg: the message to return if something goes wrong during
            service-call.

    Raises:
        an instance of :class:`HTTPException` if something goes wrong during
        service-call.

    Returns:
        the result of the service-call.

    """
    method_mapping = {
        'post': requests.post,
        'get': requests.get,
    }
    try:
        if params:
            return method_mapping[method](url, params=params)
        return method_mapping[method](url)
    except requests.ConnectionError as error:
        raise HTTPException(
            status_code=500,
            detail=f'{info_msg} => Could not connect! Error was {error}.'
        )


async def call_service(
        url: str,
        model: BaseModel,
        params: dict = None,
        method: str = 'post',
) -> BaseModel:
    """Call the rest-service at the ``url`` using ``method`` with ``params``.

    The result of the service-call is converted to an instance of ``model``.
    If any error occur this function will raise an
    :class:`HTTPException`.

    Parameters:
        url: the url of the service to call.
        model: the model to convert the service-result into.
        params: the params to use for the request.
        method: the method to use to make the service-call.

    Returns:
        the service-result as an instance of the defined ``model``.

    Raises:
        if any error occur a :class:`HTTPException` will be raised.

    """
    info_msg = (
        f'external service call (url: {url}, method: {method.upper()}, '
        f'params: {params})'
    )

    logging.debug(info_msg)

    # make the request for the url with params using method
    response = await _make_external_rest_request(
        url=url,
        method=method,
        params=params,
        info_msg=info_msg
    )

    # check if the request worked as expected
    await _check_response_status(response=response, info_msg=info_msg)

    # convert the result of the request to an instance of model
    result = await _convert_response_to_model(
        model=model,
        response=response,
        info_msg=info_msg
    )
    logging.debug(f'{info_msg} => returned result {result}.')
    return result


def add_services_to_app(
        app: FastAPI,
        services: Dict[str,
                       ServiceDefinition]
) -> FastAPI:
    """Add instances of :class:`ServiceDefinition` as attribute of app.

    For each service as defined in the ``config.yml`` as external-resource,
    create a :class:`ServiceDefinition` instance with defined parameters, add
    this instance to the ``app.services``-attribute.

    Parameters:
        app: the app to add the services as dependencies.
        services: the services to add to the app.

    Returns:
        modified app containing the attribute ``services`` to interact with
        the services inside the endpoints.

    """
    for service_name, service_definition in services.items():
        service = ServiceDefinition(
            url=service_definition.url,
            name=service_name,
            servicetype=service_definition.servicetype
        )
        try:
            app.services.update({service_name: service})
        except AttributeError:
            app.services = {service_name: service}
    return app


__all__ = ['add_services_to_app', 'call_service', 'ServiceDefinition']
