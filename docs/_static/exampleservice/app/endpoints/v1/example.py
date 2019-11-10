from app.endpoints.v1.models import Example as Output
from app.endpoints.v1.models import GetExample as Input
from fastapi import APIRouter
from fastapi import Body
from starlette.requests import Request

from fastapi_serviceutils.app import create_id_logger
from fastapi_serviceutils.app import Endpoint

ENDPOINT = Endpoint(router=APIRouter(), route='/example', version='v1')
SUMMARY = 'Example request.'
EXAMPLE = Body(..., example={'msg': 'some message.'})


@ENDPOINT.router.post('/', response_model=Output, summary=SUMMARY)
async def example(request: Request, params: Input = EXAMPLE) -> Output:
    _, log = create_id_logger(request=request, endpoint=ENDPOINT)
    log.debug(f'received request for {request.url} with params {params}.')
    return Output(msg=params.msg)
