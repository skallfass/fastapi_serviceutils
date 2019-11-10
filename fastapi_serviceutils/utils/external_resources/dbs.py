"""Functions and classes to use databases as external_resources in service."""
from dataclasses import dataclass
from typing import Dict

import databases
import sqlalchemy
from fastapi import FastAPI
from loguru._logger import Logger
from pydantic import BaseModel
from sqlalchemy.engine.base import Engine
from sqlalchemy.sql.schema import MetaData


class DatabaseDefinition(BaseModel):
    """Used by ``config.yml:external_resources`` to define db-dependency.

    Attributes:
        name: the name of the database.
        dsn: the connection string for the database.
        databasetype: the type of the database (currently only postgres
            supported).
        min_size: the minimum connections to open to the database.
        max_size: the maximum connections to open to the database.

    """
    name: str
    dsn: str
    databasetype: str
    min_size: int = 5
    max_size: int = 20


@dataclass
class Database:
    """Class to interact with database as defined in external_resources.

    Attributes:
        dsn: the connection string for the database.
        logger: the logger to use inside this class.
        min_size: the minimum connections to open to the database.
        max_size: the maximum connections to open to the database.
        engine: the sqlalchemy engine to use.
        meta: the sqlalchemy metadata to use.
        dbase: the instance of :class:`databases.Database` to use for this
            database.

    """
    dsn: str
    logger: Logger
    min_size: int
    max_size: int
    engine: Engine = None
    meta: MetaData = None
    dbase: databases.Database = None

    def __post_init__(self):
        """Set attributes ``self.dbase``, ``self.engine`` and ``self.meta``."""
        self.dbase = databases.Database(
            self.dsn,
            min_size=self.min_size,
            max_size=self.max_size
        )
        self.engine, self.meta = self.get_engine_metadata()

    def get_engine_metadata(self) -> [Engine, MetaData]:
        """Create the sqlalchemy-engine and -metadata for the database."""
        metadata = sqlalchemy.MetaData()
        engine = sqlalchemy.create_engine(self.dsn)
        metadata.create_all(engine)
        return engine, metadata

    async def connect(self):
        """Open connection to the database."""
        self.logger.info(f'connecting to {self.dsn}')
        await self.dbase.connect()

    async def disconnect(self):
        """Close connection to the database."""
        self.logger.info(f'disconnecting from {self.dsn}')
        await self.dbase.disconnect()


def add_databases_to_app(
        app: FastAPI,
        dbs: Dict[str,
                  DatabaseDefinition]
) -> FastAPI:
    """Add instances of :class:`Database` as attribute of app.

    For each database as defined in the ``config.yml`` as external-resource,
    create a :class:`Database` instance with defined parameters, add this
    instance to the ``app.databases``-attribute and add ``startup`` and
    ``shutdown`` handlers to connect / disconnect to the database on
    app-startup / app-shutdown.

    Parameters:
        app: the app to add the database definitions to.
        dbs: the databases to add to the app.

    Returns:
        modified app containing the attribute app.databases and event handler
        for startup and shutdown for the databases.

    """
    for _, db_definition in dbs.items():
        database = Database(
            dsn=db_definition.dsn,
            logger=app.logger,
            min_size=db_definition.min_size,
            max_size=db_definition.max_size
        )
        app.add_event_handler('startup', database.connect)
        app.add_event_handler('shutdown', database.disconnect)
        try:
            app.databases.update({db_definition.name: database})
        except AttributeError:
            app.databases = {db_definition.name: database}
    return app
