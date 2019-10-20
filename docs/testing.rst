.. include:: sources.rst


Testing
-------

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
