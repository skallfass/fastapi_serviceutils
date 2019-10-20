"""Middleware to collect and expose metrics of service for prometheus."""
from starlette_prometheus import metrics
from starlette_prometheus import PrometheusMiddleware

__all__ = [
    'metrics',
    'PrometheusMiddleware',
]
