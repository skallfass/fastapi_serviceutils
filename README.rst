

.. image:: https://github.com/skallfass/fastapi_serviceutils/blob/master/docs/_static/coverage.svg
   :target: https://github.com/skallfass/fastapi_serviceutils/blob/master/docs/_static/coverage.svg
   :alt: coverage


.. image:: https://badge.fury.io/py/fastapi-serviceutils.svg
   :target: https://pypi.python.org/pypi/fastapi-serviceutils/
   :alt: PyPI version fury.io


.. image:: https://img.shields.io/pypi/pyversions/fastapi-serviceutils.svg
   :target: https://pypi.python.org/pypi/fastapi-serviceutils/
   :alt: PyPI pyversions


.. image:: https://readthedocs.org/projects/fastapi-serviceutils/badge/?version=latest
   :target: http://fastapi-serviceutils.readthedocs.io/?badge=latest
   :alt: Documentation Status


.. image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://img.shields.io/badge/License-MIT-blue.svg
   :alt: MIT License


.. image:: https://github.com/dephell/dephell/blob/master/assets/badge.svg
   :target: https://github.com/dephell/dephell/blob/master/assets/badge.svg
   :alt: Powered by Dephell


Installation
------------

.. code-block:: bash

       pip install fastapi-serviceutils

Usage
-----

For more details and usage see: `readthedocs <https://fastapi-serviceutils.readthedocs.io/en/latest/>`_

Development
-----------

Getting started
^^^^^^^^^^^^^^^

After cloning the repository initialize the development environment using:

.. code-block:: bash

       make init

This will create the dev environment exampleservice/dev. Activate it using:

.. code-block:: bash

       poetry shell

**Note:**

Make sure to always activate the environment when you start working on the
project in a new terminal using

.. code-block:: bash

       poetry shell

**ATTENTION:** the environment should also be activated before using ``make``.

Updating dependencies
^^^^^^^^^^^^^^^^^^^^^

After each change in dependencies defined at ``pyproject.toml`` run the
following to ensure the environment-definition and lock-file are up to date:

.. code-block:: bash

       make update

Checking with linters and checkers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To run all pre-commit-hooks manually run:

.. code-block:: bash

       make check

Info about project-state
^^^^^^^^^^^^^^^^^^^^^^^^

To show summary about project run:

.. code-block:: bash

       make info

Documentation
^^^^^^^^^^^^^

The project's developer documentation is written using Sphinx.

The documentation sources can be found in the docs subdirectory.

The API-documentation is auto-generated from the docstrings of modules,
classes, and functions.
We're using the Google docstring standard.

To generate the documentation, run:

.. code-block:: bash

       make docs

The output for generated HTML files is in the ``docs/_build`` directory.

Tests
^^^^^

For testing we use ``pytest``\ , for details see
`Pytest Docs <http://doc.pytest.org/en/latest/>`_.
To run all tests:

.. code-block:: bash

       make tests
