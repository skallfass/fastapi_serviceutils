![coverage](doc/_static/coverage.svg)


## Installation

## Development


### Initialize project

After cloning the repository, you can initialize your development environment using

```bash
    make init
```

This will create the dev environment exampleservice/dev. Activate it using:
```bash
    dephell venv shell --env devs
```


## Start development

**Note:**

Make sure to always activate the environment when you start working on the
project in a new terminal using
```bash
    dephell venv shell --env devs
```


## Updating dependencies

After each change in dependencies defined at `pyproject.toml` run the
following to ensure the environment-definition and lock-file are up to date:
```bash
    make update
```


## Checking with linters and checkers

To run all pre-commit-hooks manually run:
```bash
    make check
```


## Info about project-state

To show summary about project run:
```bash
    make info
```


## Documentation

The project's developer documentation is written using Sphinx.

The documentation sources can be found in the docs subdirectory.
They are written using restructuredText.

The API-documentation is auto-generated from the docstrings of modules,
classes, and functions.
We're using the Google docstring standard.

To generate the documentation, run
```bash
    make docs
```

The generated HTML files will be in the `docs/_build` directory.

There is also a swagger-documentation to be used for users of the service.

The apidoc can be found at ``/apidoc/index.html``.


## Tests

For testing we use `pytest`, for details see
[Pytest Docs](http://doc.pytest.org/en/latest/).
To run all tests:

```bash
    make tests
```
