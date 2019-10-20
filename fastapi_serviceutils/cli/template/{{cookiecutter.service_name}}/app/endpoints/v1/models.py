"""Contain models required for the endpoint ``example`` (in version 1).

For models in fastapi-based services pydantic is used.
So each model inherits from :class:`BaseModel`.

In special cases the also an ``alias_generator`` has to be defined.
An example for such a special case is the attribute ``schema`` of
:class:`SpecialParams`. The schema is already an attribute of a BaseModel, so
it can't be used and an alias is required.

To be able to add post-parse-methods the pydantic ``dataclass`` can be used.
An example for this can be seen in :class:`Complex`.
"""
from typing import NoReturn

from pydantic import BaseModel
from pydantic import Schema
from pydantic.dataclasses import dataclass


class Input(BaseModel):
    """Represent example model used for requests to example endpoint."""
    msg: str


class Output(BaseModel):
    """Represent example model used for response of example endpoint."""
    msg: str


@dataclass
class Complex:
    """Represent example model with attribute-change of model after init."""
    accuracy: str

    def __post_init_post_parse__(self) -> NoReturn:
        """Overwrite self.accuracy with a mapping as defined below."""
        accuracy_mapping = {
            'street_number': 'H',
            'street': 'S',
            'city': 'L',
            'zip': 'Z',
            'district': 'D',
        }
        self.accuracy = accuracy_mapping[self.accuracy]


def _alias_for_special_model_attribute(alias: str) -> str:
    """Use as ``alias_generator`` for models with special attribute-names."""
    return alias if not alias.endswith('_') else alias[:-1]


class SpecialParams(BaseModel):
    """Represent example model with special attribute name requiring alias."""
    msg: str
    schema_: str = Schema(None, alias='schema')

    class Config:
        """Required for special attribute ``schema``."""
        alias_generator = _alias_for_special_model_attribute


__all__ = [
    'Complex',
    'Input',
    'Output',
    'SpecialParams',
]
