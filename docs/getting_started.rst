.. include:: sources.rst


Getting Started
---------------
After cloning the repository the development environment can be initialized
using:

.. code-block:: bash

    make init

This will create the dev environment ``fastapi_serviceutils/dev``.
Activate it.

.. note::

   Make sure to always activate the environment when you start
   working on the project in a new terminal using

   .. code-block:: bash

       dephell venv shell --env devs


To update dependencies and ``poetry.lock``:

.. code-block:: bash

    make update

This also creates ``requirements.txt`` to be used for Docker_.
