.. include:: sources.rst


Documentation
-------------
The project's developer documentation is written using Sphinx_.

The documentation sources can be found in the ``docs`` subdirectory.
They are using restructuredText_-files.

The API-documentation is auto-generated from the docstrings of modules, classes,
and functions.
For documentation inside the source-code the `Google docstring standard`_ is
used.

To generate the documentation, run

.. code-block:: bash

    make docs

The created documentation (as html files) will be inside the ``docs/_build``
directory.

There is also a swagger-documentation to be used for users of the service.
After starting the service the documentation can be viewed at:

* http://0.0.0.0:<SERVICE_PORT>/docs
* http://0.0.0.0:<SERVICE_PORT>/redoc

The sphinx-documentation can be viewed after service-started and docs created
at http://0.0.0.0:<SERVICE_PORT>/apidoc/index.html.

.. code-block:: bash
   :caption: documentation related files

    <SERVICENAME>
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

