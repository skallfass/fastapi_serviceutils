Development
===========

.. include:: sources.rst


Getting Started
---------------
After cloning the repository, you can initialize your development environment
using

.. code-block:: bash

    make init

This will create the dev environment ``{{cookiecutter.service_name}}/dev``.
Activate it.

.. note::

   Make sure to always activate the environment when you start
   working on the project in a new terminal using

   .. code-block:: bash

       dephell venv shell --env devs


To update dependencies and lock-file use:

.. code-block:: bash

    make update


Dependency management
---------------------

We use Poetry_ including the dependency definition inside the
``pyproject.toml`` and ``python-venv`` for environment management.
For a wrapper around these tools we use Dephell_ and ``make`` for easier
workflow.


.. code-block:: bash
    :caption: dependency-management files

    {{cookiecutter.service_name}}
    ├── ...
    ├── poetry.lock
    ├── pyproject.toml
    ├── .python-version
    └── ...

* ``pyproject.toml``: stores what dependencies are required in which versions.
  Required by Dephell_ and Poetry_.
* ``poetry.lock``: locked definition of installed packages and their versions
  of currently used devs-environment. Created by Poetry_ using ``make
  init``, ``make update``, ``make tests`` or ``make finalize``.
* ``.python-version``: the version of the python-interpreter used for this
  project. Created by ``python-venv`` using ``make init``, required by
  Poetry_ and Dephell_.


Testing the project
-------------------

All tests are located inside the folder ``tests``.
Tests for a module should be names like ``<MODULE_NAME>_test.py``.

To run the tests run:

.. code-block:: bash

    make tests

A HTML coverage report is automatically created in the ``htmlcov`` directory.

.. seealso::

    For additional information how to test fastapi-applications:

    * https://fastapi.tiangolo.com/tutorial/testing/
    * https://fastapi.tiangolo.com/tutorial/testing-dependencies/

    For information how to test async functions:

    * https://github.com/pytest-dev/pytest-asyncio


Using tmux during development
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For a predefined development environment the ``.tmuxp.yml`` configuration can
be used.
Simply run the following command to create the tmux-session:

.. code-block:: bash

    tmuxp load .


Documentation
-------------
The project's developer documentation is written using Sphinx_.

The documentation sources can be found in the ``docs`` subdirectory. They are
written using restructuredText_.

The API-documentation is auto-generated from the docstrings of modules, classes,
and functions. We're using the `Google docstring standard`_ for documentation.

To generate the documentation, run

.. code-block:: bash

    make docs

The generated HTML files will be in the ``docs/_build`` directory.

There is also a swagger-documentation to be used for users of the service.
The documentation is at:

* http://0.0.0.0:{{cookiecutter.service_port}}/docs
* http://0.0.0.0:{{cookiecutter.service_port}}/redoc

The sphinx-documentation can be viewed after service-started and docs created
at http://0.0.0.0:{{cookiecutter.service_port}}/apidoc/index.html.

.. code-block:: bash
   :caption: documentation related files

    {{cookiecutter.service_name}}
    ├── ...
    ├── docs
    │   ├── _build
    │   │   └── ...
    │   ├── conf.py
    │   ├── development.rst
    │   ├── index.rst
    │   ├── <ADDITIONAL_DOCUMENTATION_PAGE>.rst
    │   └── _static
    │       ├── coverage.svg
    │       └── logo.png
    ├── ...
    ├── README.md
    └── ...

