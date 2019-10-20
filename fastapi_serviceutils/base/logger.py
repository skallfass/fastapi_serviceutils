"""Contain helpers to customize logging for the service."""
import logging
from pathlib import Path

from loguru import logger


class _InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: 'CRITICAL',
        40: 'ERROR',
        30: 'WARNING',
        20: 'INFO',
        10: 'DEBUG',
        0: 'NOTSET',
    }

    def emit(self, record):
        try:
            loglevel = self.loglevel_mapping[record.levelno]
        except KeyError:
            loglevel = record.levelno
        logger.log(loglevel, record.getMessage())


def customize_logging(
        filepath: Path,
        level: str,
        rotation: str,
        retention: str,
        _format: str
):
    """Define the logger to be used by the service based on loguru.

    Parameters:
        filepath: the path where to store the logfiles.
        level: the minimum log-level to log.
        rotation: when to rotate the logfile.
        retention: when to remove logfiles.
        _format: the logformat to use.

    Returns:
        the logger to be used by the service.

    """
    filepath.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(handlers=[_InterceptHandler()], level=0)
    logger.add(
        str(filepath),
        rotation=rotation,
        retention=retention,
        enqueue=True,
        backtrace=True,
        level=level.upper(),
        format=_format
    )
    return logger


__all__ = [
    'customize_logging',
]
