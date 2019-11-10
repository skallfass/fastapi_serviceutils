fastapi-serviceutils
====================

.. include:: sources.rst

.. image:: https://img.shields.io/badge/python-3.7-green.svg
   :target: https://img.shields.io/badge/python-3.7-green.svg
   :alt: Python 3.7

.. image:: _static/coverage.svg
   :target: _static/coverage.svg
   :alt: coverage

.. image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://img.shields.io/badge/License-MIT-blue.svg
   :alt: License MIT

.. image:: _static/dephell.svg
   :target: https://github.com/dephell
   :alt: powered by dephell

.. image:: _static/logo.png
   :target: _static/logo.png
   :alt: logo
   :width: 300
   :align: center


Services stand for **portability** and **scalability**, so the **deployment**
and **configuration** of these service should be as easy as possible.
To achieve this a service based on fastapi-serviceutils is configured using
a ``config.yml``.
These settings can be overwritten using **environment-variables**.
Dependency management for these services is generalized using a combination of
Dephell_ and Poetry_.

For monitoring and chaining of service-calls some default endpoints should
always be defined.
For example an endpoint to check if the service is alive (``/api/alive``) and
an endpoint to access the config of the service (``/api/config``).
These endpoints are automatically added in services using fastapi-serviceutils
if defined in the ``config.yml`` of the service.

Because a service should focus on only one task it may be required to create
multiple small services in a short time.
As always time matters.
For this fastapi-serviceutils allows ** fast creation of new services** with
``create_service``.

If an error occurs during a service-call it is important to have **detailed
logs** with a **good traceback**.
To achieve this the default logging of fastapi is optimized in
fastapi-serviceutils using ``loguru``.

Fastapi allows easily created **swagger-documentation** for service-endpoints.
This is optimal for clients wanting to integrate these endpoints.
For developers of the service an additional **apidoc-documentation** of the
service and the source-code is required (most popular are documentations
created using Sphinx_ or MKDocs).
Fastapi-serviceutils based services **serve sphinx-based documentations** using
**google-documentation style** in the code and rst-files inside the
docs-folder.

The development of these services should be as much generalized as possible for
easy workflows, as less manual steps as possible for the developer and short
onboarding times.
For this fastapi-serviceutils includes a Makefile_ for most common tasks
during development.
There is also a Tmuxp_-config file to create a tmux-session for development.


Features
--------

* **optimized logging** using Loguru_
* **optimized exception handling** by additional exception handler
  ``log_exception handler``
* usage of a **config.yml**-file to configure the service
* usage of **environment-variables** (`Environment variable`_ overwrites
  config-value) to configure the service
* easily **serve the apidoc** with the service
* easy deploment using Docker_ combined with `Docker compose`_
* fast creation of new service with :doc:`/create_service`
* Makefile_ and Tmuxp_-config for easier development of services based on
  fastapi-serviceutils using **Make** and **tmux-session**


Content
-------

Fastapi-serviceutils contains three subpackages:

* :mod:`fastapi_serviceutils.app`
* :mod:`fastapi_serviceutils.cli`
* :mod:`fastapi_serviceutils.utils`

``fastapi_serviceutils.app`` contains functions and classes for
app-configuration (like config.yml file, logger, etc.), handlers and endpoint
creation.

``fastapi_serviceutils.cli`` contains executables for easier development like
``create_service`` to use the fastapi_serviceutils_template.

``fastapi_serviceutils.utils`` contain utils to interact with external
resources like databases and services, testutils and other utilities.

To see detailed usage of these functions and classes, and also recommended
service-structure, see :ref:`exampleservice`.

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :glob:

   usage.rst
   development.rst
   Code-documentation <api/fastapi_serviceutils>
   see_also.rst
