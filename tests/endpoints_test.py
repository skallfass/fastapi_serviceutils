from fastapi_serviceutils.app import Endpoint
from fastapi_serviceutils.app.endpoints import set_version_endpoints
from fastapi_serviceutils.app.endpoints.default.alive import ENDPOINT


def test_set_version_endpoints():
    endpoints = set_version_endpoints(
        endpoints=[ENDPOINT],
        version='v2',
        prefix_template='/api/{version}{route}'
    )
    endpoint = endpoints[0]
    assert isinstance(endpoints, list)
    assert isinstance(endpoint, Endpoint)
    assert endpoint.version == 'v2'
    assert endpoint.route == f'/api/v2{ENDPOINT.route}'
    assert endpoint.tags == ['v2']
    latest = set_version_endpoints(
        endpoints=endpoints,
        version='latest',
        prefix_template='{route}'
    )
    endpoint = latest[0]
    assert isinstance(latest, list)
    assert isinstance(endpoint, Endpoint)
    assert endpoint.version == 'latest'
    assert endpoint.route == f'/api/latest{ENDPOINT.route}'
    assert endpoint.tags == ['latest']
