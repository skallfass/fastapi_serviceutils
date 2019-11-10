![coverage](https://github.com/skallfass/fastapi_serviceutils/blob/master/docs/_static/coverage.svg)
[![PyPI version fury.io](https://badge.fury.io/py/fastapi-serviceutils.svg)](https://pypi.python.org/pypi/fastapi-serviceutils/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/fastapi-serviceutils.svg)](https://pypi.python.org/pypi/fastapi-serviceutils/)
[![Documentation Status](https://readthedocs.org/projects/fastapi-serviceutils/badge/?version=latest)](http://fastapi-serviceutils.readthedocs.io/?badge=latest)
![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)
![Powered by Dephell](https://github.com/dephell/dephell/blob/master/assets/badge.svg)


## Installation

```bash
    pip install fastapi-serviceutils
```


## Usage

For more details and usage see: [readthedocs](https://fastapi-serviceutils.readthedocs.io/en/latest/)


## Development


### Getting started

After cloning the repository initialize the development environment using:

```bash
    make init
```

This will create the dev environment exampleservice/dev. Activate it using:
```bash
    poetry shell
```

**Note:**

Make sure to always activate the environment when you start working on the
project in a new terminal using
```bash
    poetry shell
```

**ATTENTION:** the environment should also be activated before using ``make``.


### Updating dependencies

After each change in dependencies defined at `pyproject.toml` run the
following to ensure the environment-definition and lock-file are up to date:
```bash
    make update
```


### Checking with linters and checkers

To run all pre-commit-hooks manually run:
```bash
    make check
```


### Info about project-state

To show summary about project run:
```bash
    make info
```


### Documentation

The project's developer documentation is written using Sphinx.

The documentation sources can be found in the docs subdirectory.

The API-documentation is auto-generated from the docstrings of modules,
classes, and functions.
We're using the Google docstring standard.

To generate the documentation, run:
```bash
    make docs
```

The output for generated HTML files is in the `docs/_build` directory.


### Tests

For testing we use `pytest`, for details see
[Pytest Docs](http://doc.pytest.org/en/latest/).
To run all tests:

```bash
    make tests
```
