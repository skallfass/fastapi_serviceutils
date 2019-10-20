.. include:: sources.rst


Getting Started
---------------
After cloning the repository, you can initialize your development environment
using

.. code-block:: bash

    make init

This will create the dev environment ``fastapi_serviceutils/dev``.
Activate it.

.. note::

   Make sure to always activate the environment when you start
   working on the project in a new terminal using

   .. code-block:: bash

       dephell venv shell --env devs


To update dependencies and lock-file use:

.. code-block:: bash

    make update
