Basics
^^^^^^

.. include:: sources.rst

Docker
""""""

The basic Dockerfile_ should look like:

.. literalinclude:: _static/example_dockerfile


Docker-compose
""""""""""""""

The service can be deployed with `Docker compose`_ using the
`Docker compose file`_:


.. literalinclude:: _static/example_docker_compose.yml
   :caption: an example for a ``docker-compose.yml`` for a service using
             ``fastapi_serviceutils``.


Environment-variables
"""""""""""""""""""""

Setting environment-variables overwrites the default values defined in the
:ref:`config`.

Please ensure to use the **environment-variables** (`Environment variable`_)
if you want to overwrite some default-settings of the service.

The environment-variables to use should be defined inside the ``config.yml``.
Set the values of the environment-variables inside the ``docker-compose.yml``.
