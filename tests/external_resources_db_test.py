from pathlib import Path

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import insert
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from starlette.testclient import TestClient

from fastapi_serviceutils import make_app

Base = declarative_base()
app = make_app(
    config_path=Path('tests/configs/config.yml'),
    version='0.1.0',
    endpoints=[],
    enable_middlewares=[],
    additional_middlewares=[],
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


@app.post('/test')
async def example_endpoint():
    database = app.databases['testdb'].dbase
    async with database.transaction(force_rollback=True):
        Base.metadata.create_all(
            app.databases['testdb'].engine,
            tables=[User.__table__]
        )
        query = insert(User).values(
            email='test',
            hashed_password='bla',
            is_active=True
        )
        await database.execute(query)
        return await database.fetch_all(User.__table__.select())


def test_create_schema():
    expected = {'email': 'test', 'hashed_password': 'bla', 'is_active': True}
    with TestClient(app) as client:
        response = client.post('/test')
    result = response.json()[0]
    result.pop('id')
    assert result == expected
