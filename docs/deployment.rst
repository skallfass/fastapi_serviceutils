Deployment
----------

.. include:: sources.rst

For more detailed information about deployment of fastapi-based services see
`FastAPI deployment`_


Services based on ``fastapi_serviceutils`` can be easily deployed inside
a docker-container.


Before deployment you need to:

* **update the dependencies**
* **run all tests**
* **create the current** ``requirements.txt``
* **ensure the** ``docker-compose.yml`` **is defined correctly including the**
  ``environment-variables``

To run these tasks run:

.. code-block:: bash

   make finalize

To run the service using docker-compose customize the ``docker-compose.yml``
and run:

.. code-block:: bash

    sudo docker-compose up -d


.. include:: deployment_basics.rst
