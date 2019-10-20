"""Interact with external services."""
import logging

import requests
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import ValidationError


async def _convert_request_result_to_model(
        model: BaseModel,
        request,
        info_msg
) -> BaseModel:
    """Extract request-result and convert it into an instance of ``model``."""
    try:
        result = request.json()
        return model(**result)
    except ValidationError as error:
        raise HTTPException(
            status_code=500,
            detail=(
                f'{info_msg} => Invalid result: {request}. Error was {error}.'
            )
        )


async def _check_request_status(request, info_msg: str):
    """Check if the status of the request is valid."""
    try:
        request.raise_for_status()
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
    """Request external service at ``url`` using ``method`` with ``params``."""
    method_mapping = {
        'post': requests.post,
        'get': requests.get,
    }
    try:
        if params:
            return method_mapping[method](url, params=params)
        else:
            return method_mapping[method](url)
    except requests.ConnectionError as error:
        raise HTTPException(
            status_code=500,
            detail=f'{info_msg} => Could not connect! Error was {error}.'
        )


async def call_rest_service(
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
        params: the params to use for the request.
        model: the model to convert the service-result into.
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
    request_result = await _make_external_rest_request(
        url=url,
        method=method,
        params=params,
        info_msg=info_msg
    )

    # check if the request worked as expected
    await _check_request_status(request=request_result, info_msg=info_msg)

    # convert the result of the request to an instance of model
    result = await _convert_request_result_to_model(
        model=model,
        request=request_result,
        info_msg=info_msg
    )
    logging.debug(f'{info_msg} => returned result {result}.')
    return result


__all__ = ['call_rest_service']
