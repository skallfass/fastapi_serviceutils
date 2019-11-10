"""Helpers to test endpoints with pytest."""
from typing import Any

from fastapi import FastAPI
from starlette.testclient import TestClient


def json_endpoint(
        application: FastAPI,
        endpoint: str,
        payload: dict = None,
        expected: Any = None,
        status_code: int = 200
):
    """Test endpoint of app with payload."""
    client = TestClient(application)
    if payload:
        response = client.post(endpoint, json=payload)
    else:
        response = client.post(endpoint)

    assert response.status_code == status_code

    if status_code == 200:
        result = response.json()

        if expected:
            assert result == expected

        return result
    return True
