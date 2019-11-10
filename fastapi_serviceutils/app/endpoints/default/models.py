"""Contain not version depending models for default-endpoints of service.

For each endpoint requiring parameters as input on call an input-model should
be defined here.

For each endpoint returning data on call an output-model should be defined
here, too.

Currently both default-endpoints do not require input-parameters, so no
input-models are defined here yet.

The config-endpoint returns data of model
:class:`fastapi_serviceutils.app.service_config.Config` so this one is not
defined here, because already defined.

The alive-endpoint returns data of model :class:`Alive`.
"""
from pydantic import BaseModel


class Alive(BaseModel):
    """Represent the alive-result of the endpoint ``/api/alive``."""
    alive: bool
