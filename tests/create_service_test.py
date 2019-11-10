# -*- coding: utf-8 -*-
from argparse import Namespace
from pathlib import Path

import pytest

from fastapi_serviceutils.cli.create_service import _build_arguments
from fastapi_serviceutils.cli.create_service import _check_name
from fastapi_serviceutils.cli.create_service import _create_context
from fastapi_serviceutils.cli.create_service import _create_service_folder


@pytest.mark.parametrize(
    'name',
    ['fastapi',
     'fastapi_serviceutils',
     'pathlib2']
)
def test_check_name(name: str):
    assert _check_name(name=name, variable_name='test')


@pytest.mark.parametrize(
    'name',
    ['1fastapi',
     'fastapi serviceutils',
     'pathlib-2']
)
def test_check_name_invalid(name: str):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        _check_name(name=name, variable_name='test')
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


@pytest.mark.parametrize('output_dir', ['/tmp'])
@pytest.mark.parametrize('endpoint', ['example', 'example1', 'example_1'])
@pytest.mark.parametrize('author_email', ['bla@blub.info'])
@pytest.mark.parametrize('author', ['bla'])
@pytest.mark.parametrize('service_port', ['50000', '50001'])
@pytest.mark.parametrize(
    'service_name',
    ['fastapi',
     'fastapi_serviceutils',
     'pathlib2']
)
def test_build_arguments(
        service_name: str,
        service_port: str,
        author: str,
        author_email: str,
        endpoint: str,
        output_dir: str
):
    params = _build_arguments(
        [
            '--service_name',
            service_name,
            '--service_port',
            service_port,
            '--author',
            author,
            '--author_email',
            author_email,
            '--endpoint',
            endpoint,
            '--output_dir',
            output_dir
        ]
    )
    assert params.service_name == service_name
    assert params.service_port == service_port
    assert params.author == author
    assert params.author_email == author_email
    assert params.endpoint == endpoint
    assert params.output_dir == Path(output_dir)


def test_create_context():
    params = Namespace(
        service_name='exampleservice',
        service_port='50000',
        author='john smith',
        author_email='jsmith@something.info',
        endpoint='example',
        output_dir=Path('/tmp')
    )
    result = _create_context(params=params)
    assert result['cookiecutter']


def test_create_service_folder(tmpdir):
    repo_url = 'git+ssh://git@github.com/skallfass/fastapi_serviceutils_template.git'
    params = Namespace(
        service_name='exampleservice',
        service_port='50000',
        author='john smith',
        author_email='jsmith@something.info',
        endpoint='example',
        output_dir=Path('/tmp')
    )
    context = _create_context(params=params)
    clone_to_dir = str(tmpdir)
    assert _create_service_folder(
        repo_url=repo_url,
        context=context,
        output_dir=str(tmpdir),
        clone_to_dir=clone_to_dir
    )
    assert (tmpdir / 'exampleservice').exists()
    assert (tmpdir / 'fastapi_serviceutils_template').exists()
    assert not _create_service_folder(
        repo_url=repo_url,
        context=context,
        output_dir=str(tmpdir),
        clone_to_dir=clone_to_dir
    )
