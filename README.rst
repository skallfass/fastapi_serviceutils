

.. image:: apidoc/_static/coverage.svg
   :target: apidoc/_static/coverage.svg
   :alt: coverage


Installation
------------

Development
-----------

Initialize project
^^^^^^^^^^^^^^^^^^

After cloning the repository, you can initialize your development environment using

.. code-block:: bash

       make init

This will create the dev environment exampleservice/dev. Activate it using:

.. code-block:: bash

       dephell venv shell --env devs

Start development
-----------------

**Note:**

Make sure to always activate the environment when you start working on the
project in a new terminal using

.. code-block:: bash

       dephell venv shell --env devs

Updating dependencies
---------------------

After each change in dependencies defined at ``pyproject.toml`` run the
following to ensure the environment-definition and lock-file are up to date:

.. code-block:: bash

       make update

Checking with linters and checkers
----------------------------------

To run all pre-commit-hooks manually run:

.. code-block:: bash

       make check

Info about project-state
------------------------

To show summary about project run:

.. code-block:: bash

       make info

Documentation
-------------

The project's developer documentation is written using Sphinx.

The documentation sources can be found in the docs subdirectory.
They are written using restructuredText.

The API-documentation is auto-generated from the docstrings of modules,
classes, and functions.
We're using the Google docstring standard.

To generate the documentation, run

.. code-block:: bash

       make docs

The generated HTML files will be in the ``docs/_build`` directory.

There is also a swagger-documentation to be used for users of the service.
The documentation can be found at (after starting service):


* `http://0.0.0.0:9992/docs <http://0.0.0.0:9992/docs>`_
* `http://0.0.0.0:9992/redoc <http://0.0.0.0:9992/redoc>`_

The apidoc can be found at
`http://0.0.0.0:9992/apidoc/index.html <http://0.0.0.0:9992/apidoc/index.html>`_.

Tests
-----

For testing we use ``pytest``\ , for details see
`Pytest Docs <http://doc.pytest.org/en/latest/>`_.
To run all tests:

.. code-block:: bash

       make tests
