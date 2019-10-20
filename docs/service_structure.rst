Service-structure
-----------------

A service using fastapi_serviceutils should have the following
folder-structure:

.. code-block:: bash
   :caption: service folder-structure

    <SERVICE_NAME>
    ├── app
    │   ├── config.yml
    │   ├── endpoints
    │   │   ├── __init__.py
    │   │   └── v1
    │   │       ├── errors.py
    │   │       ├── <ENDPOINT>.py
    │   │       └── models.py
    │   ├── __init__.py
    │   └── main.py
    ├── .codespell-ignore-words.txt
    ├── docker-compose.yml
    ├── Dockerfile
    ├── docs
    │   └── ...
    ├── .gitignore
    ├── Makefile
    ├── poetry.lock
    ├── .pre-commit-config.yaml
    ├── pyproject.toml
    ├── .python-version
    ├── README.md
    ├── setup.cfg
    ├── tests
    │   └── ...
    └── .tmuxp.yml


main.py
"""""""

.. code-block:: python
   :caption: main.py

    from pathlib import Path
    from typing import NoReturn

    from fastapi_serviceutils.service import make_app

    from app import __version__
    from app.endpoints import ENDPOINTS

    app = make_app(
        config_path=Path(__file__).with_name('config.yml'),
        version=__version__,
        endpoints=ENDPOINTS,
        enable_middlewares=['trusted_hosts', 'log_exception'],
        additional_middlewares=[]
    )

    def main() -> NoReturn:
        import uvicorn
        uvicorn.run(
            app,
            host='0.0.0.0',
            port=app.config.service.development_port
        )

    if __name__ == '__main__':
        main()


.. _config-content:

config
""""""

.. literalinclude:: _static/example_config.yml
   :caption: example for a config.yml required by a service using
             ``fastapi_serviceutils``.
