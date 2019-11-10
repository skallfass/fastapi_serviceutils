# -*- coding: utf-8 -*-
"""Contain the configuration for the sphinx-documentation of the service."""

project = 'fastapi-serviceutils'
copyright = '2019, Simon Kallfass (MIT-License)'
author = 'Simon Kallfass'
release = version = '2.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
    'sphinx.ext.viewcode',
    'sphinx_rtd_theme'
]

templates_path = ['_templates']

exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    'api/modules.rst',
]

html_theme = 'sphinx_rtd_theme'
pygments_style = 'solarized-dark'

html_static_path = ['_static']

html_logo = '_static/logo.png'
html_theme_options = {
    'canonical_url': '',
    'analytics_id': '',
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 5,
    'includehidden': True,
    'titles_only': False
}

intersphinx_mapping = {
    'python': ('https://docs.python.org/3',
               None),
}

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_use_param = True
