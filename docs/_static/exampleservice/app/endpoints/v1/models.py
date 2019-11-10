from pydantic import BaseModel


class GetExample(BaseModel):
    msg: str


class Example(BaseModel):
    msg: str


__all__ = ['Example', 'GetExample']
