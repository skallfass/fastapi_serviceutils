"""Endpoint definition for {{cookiecutter.endpoint}}."""
import logging

from fastapi import APIRouter

from app.endpoints.v1.models import Input
from app.endpoints.v1.models import Output
# from fastapi_serviceutils.external_resources import call_rest_service

ROUTER = APIRouter()
PREFIX = '/api/v1/{{cookiecutter.endpoint}}'
TAGS = ['v1', '{{cookiecutter.endpoint}}']


@ROUTER.post(
    '/',
    response_model=Output,
    summary='Example requests.',
    tags=TAGS,
)
async def {{cookiecutter.endpoint}}(input_: Input) -> Output:
    """Demonstrate a basic endpoint.

    Parameters:
        input: the request-parameters converted to an instance of
            :class:`Input`.

    Returns:
        the result for the requested parameters.

    """
    result = Output(msg=input_.msg)
    logging.debug(f'handling request for endpoint {PREFIX}')
    return result
