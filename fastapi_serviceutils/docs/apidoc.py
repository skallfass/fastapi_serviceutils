"""Apidoc related functions.

Contain function to mount the apidoc at route ``/apidoc`` to the service.
"""
import logging
from typing import NoReturn

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles


def mount_apidoc(app: FastAPI) -> NoReturn:
    """Mount the apidoc at defined documentation_dir if it exists.

    Parameters:
        app: the app to mount the apidoc to.

    """
    apidoc_dir = app.config.service.apidoc_dir
    try:
        app.mount('/apidoc', StaticFiles(directory=apidoc_dir), name='apidoc')
        logging.debug('Mounted apidoc')
    except RuntimeError:
        logging.warning(f'no doc-folder at {apidoc_dir} to serve at /apidoc')


__all__ = ['mount_apidoc']
