.. include:: sources.rst


Dependency management
---------------------

We use Poetry_ including the dependency definition inside the
``pyproject.toml`` and ``python-venv`` for environment management.
For a wrapper around these tools we use Dephell_ and ``make`` for easier
workflow.


.. code-block:: bash
    :caption: dependency-management files

    <SERVICENAME>
    ├── ...
    ├── poetry.lock
    ├── pyproject.toml
    ├── .python-version
    └── ...

* ``pyproject.toml``: stores what dependencies are required in which versions.
  Required by Dephell_ and Poetry_.
* ``poetry.lock``: locked definition of installed packages and their versions
  of currently used devs-environment. Created by Poetry_ using ``make
  init``, ``make update``, ``make tests`` or ``make finalize``.
* ``.python-version``: the version of the python-interpreter used for this
  project. Created by ``python-venv`` using ``make init``, required by
  Poetry_ and Dephell_.
