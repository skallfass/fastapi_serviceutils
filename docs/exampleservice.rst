.. _exampleservice:

exampleservice
==============

.. include:: sources.rst

The easiest way to explain how to use fastapi-serviceutils is to demonstrate
usage inside an exampleservice.
Here we will explain the parts of the service and which functions and classes
when to use.


Creating new service
--------------------

To create a new service we use the tool ``create_service`` which is available
after installing fastapi-serviceutils.

.. code:: bash

    create_service -n exampleservice \
        -p 50001 \
        -a "Dummy User" \
        -e dummy.user@something.info \
        -ep example \
        -o /tmp

This creates the service **exampleservice** inside the folder
**/tmp/exampleservice**.
As author with email we define **Dummy User** and
**dummy.user@something.info**.
The initial endpoint we want to create is **example**.
The service should listen to port **50001**.

If we change into the created directory we will have the following
folder-structure:

.. code:: bash

    exampleservice
    ├── app
    │   ├── config.yml
    │   ├── endpoints
    │   │   ├── __init__.py
    │   │   └── v1
    │   │       ├── errors.py
    │   │       ├── example.py
    │   │       ├── __init__.py
    │   │       └── models.py
    │   ├── __init__.py
    │   └── main.py
    ├── .codespell-ignore-words.txt
    ├── docker-compose.yml
    ├── Dockerfile
    ├── docs
    │   └── ...
    ├── .gitignore
    ├── Makefile
    ├── .pre-commit-config.yaml
    ├── pyproject.toml
    ├── .python-version
    ├── README.md
    ├── setup.cfg
    ├── tests
    │   └── __init__.py
    └── .tmuxp.yml


The files ``docker-compose.yml`` and ``Dockerfile`` are required for
deployment of the service as docker-container.

``.tmuxp.yml`` is used for development of the service if you prefer to develop
inside tmux in combination with for example vim or emacs.

The ``.python-version`` defines which python-version this service uses and is
used by poetry / dephell workflow inside virtual-environments.

The ``pyproject.toml`` is used for dependency-management and package-creation.

``setup.cfg`` contains configurations for tools used during development like
yapf, flake8, pytest, etc.

The ``.pre-commit-config.yaml`` allows the usage of pre-commit and is also
used in the make command ``make check``.
It enables running of multiple linters, checkers, etc. to ensure a fixed
codestyle.

The ``Makefile`` contains helper command like initializing the project,
updating the virtual-environment, running tests, etc.

Because codespell is used inside the configuration of pre-commit, the file
``.codespell-ignore-words.txt`` is used to be able to define words to be
ignored during check with codespell.


Initialising project
^^^^^^^^^^^^^^^^^^^^

To initialise the project after creation we run:

.. code:: bash

    make init

This creates the virtual-environment and installs the dependencies as defined
in the ``pyproject.toml``.
It also initialises the project as a git-folder and creates the initial
commit.

We now activate the poetry-shell to enable the environment:

.. code:: bash

    poetry shell


.. Attention::

    Please ensure to always enable the poetry-shell before development using:

    .. code:: bash

        poetry shell

    The Makefile assumes the environment is activated on usage.


Folder-structure
----------------

Following shows code-relevant files for an exampleservice as created using the
create_service-tool of fastapi-serviceutils.

.. code:: bash

    exampleservice
    ├── app
    │   ├── config.yml
    │   ├── endpoints
    │   │   ├── __init__.py
    │   │   └── v1
    │   │       ├── errors.py
    │   │       ├── example.py
    │   │       ├── __init__.py
    │   │       └── models.py
    │   ├── __init__.py
    │   └── main.py
    ├── pyproject.toml
    └── tests
        ├── __init__.py
        └── service_test.py


pyproject.toml
--------------

The dependencies and definitions like the package-name, version, etc. are
defined inside the ``pyproject.toml``.
This file is used by Poetry_ and Dephell_.
Following the ``pyproject.toml`` for our exampleservice:

.. literalinclude:: _static/exampleservice/pyproject.toml
   :caption: the ``pyproject.toml`` of the exampleservice.


app/config.yml
--------------

The service is configured using a config-file (``config.yml``).
It is possible to overwrite these setting using environment-variables.
An example for the ``config.yml`` of the exampleservice is shown below:

.. literalinclude:: _static/exampleservice/app/config.yml
   :caption: ``config.yml`` of exampleservice.

The config contains four main sections:

* **service**
* **external_resources**
* **logger**
* **available_environment_variables**


config: [service]
^^^^^^^^^^^^^^^^^

Inside this section we define the name of the service ``name``.
This name is used for the **swagger-documentation** and **extraction of the
environment-variables**.

The ``mode`` define the **runtime-mode** of the service.
This mode can be overwritten with the environment-variable
``EXAMPLESERVICE__SERVICE__MODE`` (where ``'EXAMPLESERVICE'`` is the name of
the service, meaning if you have a service named ``SOMETHING`` the
environment-variable would be ``SOMETHING__SERVICE__MODE``).

The ``port`` configure the **port the service will listen to**.
This can also be overwritten using the environment variable
``EXAMPLESERVICE__SERVICE__PORT``.

The ``description`` is used for the swagger-documentation.

To define the folder where the to find the **apidoc to serve by route**
``/api/apidoc/index.html`` the keyword ``apidoc_dir`` is used.

``readme`` defines where to get the readme from to be used as main description
for the swagger-documentation at ``/docs`` / ``/redoc``.

To controll if only specific hosts are allowed to controll the service we use
``allowed_hosts``.
Per default a service would allow all hosts (``'*'``) but this can be
customized here in the config.

To define which default endpoints should be included in our service we use
``use_default_endpoints``.
Currently we support the default endpoints ``/api/alive`` (inside config:
``'alive'``) and ``/api/config`` (inside config: ``'alive'``).


config: [external_resources]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Inside this section external dependencies (resources) are defines.
A service can depend on other services, databases, remote-connections or
files / folders.

Dependencies to other services should be defined inside ``services``.
Database connections inside ``databases`` (currently only postgres is
supported).
If any other dependency exist define it in ``other``.

Defined services can be accessed in the code using
``app.config.external_resources.services`` or
``ENDPOINT.config.external_resources.services`` depending if you are in a main
part of the app or inside an endpoint.

Databases are automatically included into the ``startup`` and ``shutdown``
handlers.
You can access the database connection using ``app.databases['DATABASE_NAME']``
or ``ENDPOINT.databases['DATABASE_NAME']`` depending if you are in a main part
of the app or inside an endpoint.


config: [logger]
^^^^^^^^^^^^^^^^

All settings inside this section are default Loguru_ settings to configure the
logger.
You can control where to log (``path``) and how the logfile should be named
(``filename``).
Also which minimum level to log (``level``).
To control when to rotate the logfile use ``rotation``.
``retention`` defines when to delete old logfiles.
The ``format`` defines the format to be used for log-messages.


config: [available_environment_variables]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The environment-variables are seperated into three types:

* ``env_vars``
* ``external_resources_env_vars``
* ``rules_env_vars``

Here you can control which environment-variables to use if they are set.

The environment-variables are named like the following:
``<SERVICENAME>__<MAJOR_SECTION>__<PARAMETER_NAME>``.
The servicename would be ``'EXAMPLESERVICE'`` in our example.
The major-section is one of:

* ``'SERVICE'``
* ``'LOGGER'``
* ``'EXTERNAL_RESOURCES'``

``env_vars`` control the sections ``service`` and ``logger``.
``external_resources_env_vars`` control the configurations inside the section
``external_resources``.
The ``rules_env_vars`` should overwrite settings of a ruleset of the service.
Such a ruleset defines constants and other rules for the logic of the
endpoints.
For example a default time-range for your pandas dataframes, etc.
Currently this is not implemented, so you would have to use these definitions
yourself to overwrite your ruleset-definitions.


app/\__init\__.py
-----------------

Inside the ``__init__.py`` file of the app we only define the version of our
service.

.. Note::

    We use semantic-versioning style for services based on
    fastapi-serviceutils.

    This means we have the following version-number:
    ``<MAJOR>.<MINOR>.<PATCH>``.

    For details about semantic-versioning see Semver_.

If we bump the version using either ``dephell bump {major, minor, fix}`` or
``poetry version {major, minor, patch}``, both the version defined here, and
the version defined inside the ``pyproject.toml`` will be increased.

.. literalinclude:: _static/exampleservice/app/__init__.py
   :caption: ``__init__.py`` of app.


app/main.py
-----------

Inside this file we glue all parts of our service together.

Here the ``app`` is created which is used either in development inside the
function ``main`` or in production using ``uvicorn`` from command line (or
docker-container).

.. literalinclude:: _static/exampleservice/app/main.py
   :caption: ``main.py`` of app.

We define where to collect the config-file of the service from, the version of
the service and which endpoints and middlewares to use.


app/endpoints/v1/example.py
---------------------------

The following shows the example-endpoint we created:

.. literalinclude:: _static/exampleservice/app/endpoints/v1/example.py
   :caption: ``example.py`` in version 1. Define the endpoint example.

The ``ENDPOINT`` includes the ``router``, ``route`` and the ``version`` of our
endpoint.

Inside the endpoint-function we create a new bound logger with the request-id
of the request to allow useful traceback.

.. Note::

    Defining endpoints like this allows our worklow with endpoint-versioning
    and usage of :func:`fastapi_serviceutils.endpoints.set_version_endpoints`
    inside ``app/endpoints/v1/__init__.py`` and ``app/endpoints/__init__.py``.


app/endpoints/v1/models.py
--------------------------

The models.py contains models for the endpoints in version 1 of our
exampleservice.

For each endpoint we create the model for the input (request) and the model
for the output (response).

The models are of type :class:`pydantic.BaseModel`

.. literalinclude:: _static/exampleservice/app/endpoints/v1/models.py
   :caption: ``models.py`` of endpoints of version 1.

More complex models could look like the following:

.. code:: python

    """
    In special cases also an ``alias_generator`` has to be defined.
    An example for such a special case is the attribute ``schema`` of
    :class:`SpecialParams`. The schema is already an attribute of a BaseModel,
    so it can't be used and an alias is required.

    To be able to add post-parse-methods the pydantic ``dataclass`` can be
    used.
    An example for this can be seen in :class:`Complex`.
    """

    from pydantic import BaseModel
    from pydantic import Schema
    from pydantic.dataclasses import dataclass

    @dataclass
    class Complex:
        """Represent example model with attribute-change of model after init."""
        accuracy: str

        def __post_init_post_parse__(self) -> NoReturn:
            """Overwrite self.accuracy with a mapping as defined below."""
            accuracy_mapping = {
                'something': 's',
                'match': 'm',
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


app/endpoints/v1/\__init\__.py
------------------------------

Inside this file we include our example-endpoint to the version 1 endpoints.

.. Note::

    If additional endpoints are available, these should be added here, too.

The created ``ENDPOINTS`` is used inside ``app/endpoints/__init__.py`` later.

.. Note::

    If we would increase our version to version 2 and we want to change the
    endpoint ``example`` we would add an additional folder inside
    ``app/endpoints`` named ``v2`` and place the new version files there.

.. literalinclude:: _static/exampleservice/app/endpoints/v1/__init__.py
   :caption: ``__init__.py`` of v1.


app/endpoints/\__init\__.py
---------------------------

In this file we import all endpoint-versions like in this example
``from app.endpoints.v1 import ENDPOINTS as v1``.

.. Note::

    If we would have an additional version 2 we would also add ``from
    app.endpoints.v2 import ENDPOINTS as v2``.

Then we use :func:`fastapi_serviceutils.endpoints.set_version_endpoints` with
the latest version endpoints to create ``LATEST``.

.. Note::

    If we would have version 2, too we would replace parameter ``endpoints``
    with ``v2``.

The ``ENDPOINTS`` is a list of all available versions.

These ``ENDPOINTS`` are used inside ``app/main.py`` to include them to the
service.

.. literalinclude:: _static/exampleservice/app/endpoints/__init__.py
   :caption: ``__init__.py`` of endpoints.


tests
-----

The tests for the exampleservice are using Pytest_.
We also used the testutils of ``fastapi-serviceutils``.
An example for simple endpoint tests of our exampleservice:

.. literalinclude:: _static/exampleservice/tests/service_test.py
   :caption: ``tests/service_test.py``
