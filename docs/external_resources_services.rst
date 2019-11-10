Services
========

If we need to call external services we first have to declare the service
inside the ``config.yml`` like the following:

.. code-block:: yaml
    :caption: ``app/config.yml``

    ...
    external_resources:
        services:
            testservice:
                url: http://someserviceurl:someport
                servicetype: rest
        databases: null
        other: null
    ...


.. code-block:: python
    :caption: ``app/endpoints/v1/models.py``

    from pydantic import BaseModel

    class CallExternalService(BaseModel):
        street: str
        street_number: str
        zip_code: str
        city: str
        country: str

    class ExternalServiceResult(BaseModel):
        longitude: str
        latitude: str


.. code-block:: python
    :caption: ``app/endpoints/v1/external_service.py``

    from fastapi import APIRouter
    from fastapi import Body
    from fastapi_serviceutils.app import Endpoint
    from fastapi_serviceutils.app import create_id_logger
    from fastapi_serviceutils.utils.external_resources.services import call_service
    from starlette.requests import Request

    from app.endpoints.v1.models import CallExternalService as Input
    from app.endpoints.v1.models import ExternalServiceResult as Output

    ENDPOINT = Endpoint(router=APIRouter(), route='/use_service', version='v1')
    SUMMARY = 'Example request using an external service.'
    EXAMPLE = Body(
        ...,
        example={
            'street': 'anystreetname',
            'street_number': '42',
            'city': 'anycity',
            'country': 'gallifrey'
        }
    )

    @ENDPOINT.router.post('/', response_model=Output, summary=SUMMARY)
    async def use_service(params: Input = EXAMPLE, request: Request) -> Output:
        data_to_fetch = {
            'street': params.street,
            'auth_key': 'fnbkjgkegej',
            'street_number': params.street_number,
            'city': params.city,
            'country': params.country
        }
        return await call_service(
            url=app.databases['testservice'].url,
            params=data_to_fetch,
            model=ExternalServiceResult
        )
