fastapi_serviceutils
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


Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :glob:

   usage.rst
   development.rst
   Code-documentation <api/fastapi_serviceutils>
   see_also.rst
