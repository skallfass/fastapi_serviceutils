"""Glue all parts of the {{cookiecutter.service_name}} together.

Set up the app for the {{cookiecutter.service_name}}.
"""
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
    """Use for entrypoint of package.

    Start the service using uvicorn.
    """
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=app.config.service.development_port)


if __name__ == '__main__':
    main()
