Databases
=========


config.yml
----------

If we use a database in our service we declare the connection info in the
``config.yml`` of the service like the following:

.. code-block:: yaml
    :caption: ``app/config.yml``

    ...
    external_resources:
        services: null
        databases:
            userdb:
                dsn: 'postgresql://postgres:1234@localhost:5434/userdb'
                databasetype: 'postgres'
                min_size: 5
                max_size: 20
        other: null
    ...

For each database we want to use in our service, we define a new item inside
``databases``.
The **key** will be the name of our database.
The connection itself is defined as ``dsn``.
The databasetype defines the type of the database we are using.
This setting is for future releases of fastapi-serviceutils.
Currently we only support ``postgres`` and this setting has no effect.
``min_size`` and ``max_size`` define the minimum and maximum amount of
connections to open to the database.


app/endpoints/v1/dbs.py
-----------------------

Inside the module ``dbs.py`` we define our datatables like the following:

.. code-block:: python
    :caption: ``app/endpoints/v1/dbs.py``

    from sqlalchemy import Boolean
    from sqlalchemy import Column
    from sqlalchemy import insert
    from sqlalchemy import Integer
    from sqlalchemy import String
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    class User(Base):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True, index=True)
        email = Column(String, unique=True, index=True)
        password = Column(String)


app/endpoints/v1/models.py
--------------------------

As for each endpoint we declare the input- and output-models we are using in
our new endpoints like the following:

.. code-block:: python
    :caption: ``app/endpoints/v1/models.py``

    from pydantic import BaseModel

    class InsertUser(BaseModel):
        email: str
        password: str

    class Inserted(BaseModel):
        msg: bool = True

    class User(BaseModel):
        id: int
        email: str
        password: str


app/endpoints/v1/insert_user.py
-------------------------------

.. code-block:: python
    :caption: ``app/endpoints/v1/insert_user.py``

    from fastapi import Body
    from fastapi import APIRouter
    from fastapi_serviceutils.app import Endpoint
    from fastapi_serviceutils.app import create_id_logger
    from sqlalchemy import insert

    from app.endpoints.v1.dbs import User
    from app.endpoints.v1.models import InsertUser as Input
    from app.endpoints.v1.models import Inserted as Output

    ENDPOINT = Endpoint(router=APIRouter(), route='/insert_user', version='v1')
    SUMMARY = 'Example request.'
    EXAMPLE = Body(
        ...,
        example={
            'email': 'dummy.user@something.info'
            'password': 'an3xampleP4ssword'
        }
    )

    @ENDPOINT.router.post('/', response_model=Output, summary=SUMMARY)
    async def insert_user(params: Input = EXAMPLE, request: Request) -> Output:
        _, log = create_id_logger(request=request, endpoint=ENDPOINT)
        log.debug(f'received request for {request.url} with params {params}.')
        database = app.databases['userdb'].dbase
        async with database.transaction():
            query = insert(User).values(
                email=params.email,
                password=params.password
            )
            await database.execute(query)
        return Output()


app/endpoints/v1/get_users.py
-----------------------------

.. code-block:: python
    :caption: ``app/endpoints/v1/get_users.py``

    from fastapi import Body
    from fastapi import APIRouter
    from fastapi_serviceutils.app import Endpoint
    from fastapi_serviceutils.app import create_id_logger

    from app.endpoints.v1.dbs import User
    from app.endpoints.v1.models import User as Output

    ENDPOINT = Endpoint(router=APIRouter(), route='/get_users', version='v1')
    SUMMARY = 'Example request.'

    @ENDPOINT.router.post('/', response_model=Output, summary=SUMMARY)
    async def get_users(request: Request) -> List[Output]:
        _, log = create_id_logger(request=request, endpoint=ENDPOINT)
        log.debug(f'received request for {request.url}.')
        database = app.databases['userdb'].dbase
        async with database.transaction():
            users = await database.fetch_all(User.__table__.select())
        return users


app/endpoints/v1/\__init\__.py
-------------------------------

Finally we include these endpoints to our ``ENDPOINTS``.

.. code-block:: python
    :caption: ``__init__.py``

    from fastapi_serviceutils.endpoints import set_version_endpoints

    from app.endpoints.v1 import get_users
    from app.endpoints.v1 import insert_user

    ENDPOINTS = set_version_endpoints(
        endpoints=[get_users, insert_user],
        version='v1',
        prefix_template='/api/{version}{route}'
    )

    __all__ = ['ENDPOINTS']


The rest of our service, like the ``main.py``, the ``__init__.py`` files of
the modules, etc. have the same content as described in ``exampleservice``.
