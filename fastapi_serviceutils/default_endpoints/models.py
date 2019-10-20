"""Contain not version depending models for default-endpoints of service."""
from pydantic import BaseModel


class Alive(BaseModel):
    """Represent the alive-result of the endpoint ``/api/alive``."""
    alive: bool
