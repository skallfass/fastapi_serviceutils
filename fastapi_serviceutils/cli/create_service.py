"""Create new service using the fastapi_serviceutils-template.

For this functionality we use Cookiecutter.
"""
import sys
from argparse import ArgumentParser
from argparse import Namespace
from pathlib import Path
from string import ascii_letters
from string import digits

from cookiecutter import generate
from cookiecutter.exceptions import OutputDirExistsException
from cookiecutter.vcs import clone
from toolz import curry


def _check_name(name: str, variable_name: str) -> bool:
    """Check if the passed ``name`` doesn't include invalid chars."""
    allowed_chars = (f'{str(set(ascii_letters.lower()))}_{digits}')
    try:
        assert all(_ in allowed_chars for _ in name)
        assert ' ' not in name
    except AssertionError:
        print('!!! Creation of service skipped!!!')
        print(f'Invalid {variable_name}: {name}!')
        print('Only ascii-letters and numbers are allowed!')
        sys.exit(1)
    try:
        assert not any(name.startswith(_) for _ in digits)
    except AssertionError:
        print('!!! Creation of service skipped!!!')
        print(f'Invalid {variable_name}: {name}!')
        print('Must not start with number!')
        sys.exit(1)
    return name


def _build_arguments(args) -> Namespace:
    """Create required arguments for create_service."""
    parser = ArgumentParser(
        description=(
            'create new service based on fastapi using fastapi_serviceutils.'
        )
    )
    parser.add_argument(
        '-n',
        '--service_name',
        type=curry(_check_name,
                   variable_name='service_name'),
        required=True,
        help=(
            'the name of the service to create. '
            'ATTENTION: only ascii-letters, "_" and digits are allowed. '
            'Must not start with a digit!'
        )
    )
    parser.add_argument(
        '-p',
        '--service_port',
        type=str,
        required=True,
        default='50001',
        help='the port for the service to listen.'
    )
    parser.add_argument(
        '-a',
        '--author',
        type=str,
        required=True,
        help='the name of the author of the service.'
    )
    parser.add_argument(
        '-e',
        '--author_email',
        type=str,
        required=True,
        help='the email of the author of the service.'
    )
    parser.add_argument(
        '-ep',
        '--endpoint',
        type=curry(_check_name,
                   variable_name='endpoint'),
        required=True,
        help=(
            'the name of the endpoint for the service to create. '
            'ATTENTION: only lower ascii-letters, "_" and digits are allowed. '
            'Must not start with a digit!'
        )
    )
    parser.add_argument('-o', '--output_dir', required=True, type=Path)
    return parser.parse_args(args)


def _create_service_folder(
        repo_url: str,
        context: dict,
        output_dir: str,
        clone_to_dir: str = '/tmp'
) -> bool:
    """Clone the template and create service-folder based on this template."""
    filepath = clone(repo_url, clone_to_dir=clone_to_dir, no_input=True)
    try:
        generate.generate_files(
            filepath,
            context=context,
            output_dir=output_dir,
            overwrite_if_exists=False
        )
    except OutputDirExistsException:
        print('Folder already exists!')
        print('Skipped creation of new service!')
        return False
    return True


def _create_context(params: Namespace):
    """Create the context required for :func:`generate.generate_files`."""
    return {
        'cookiecutter': {
            'service_name': params.service_name,
            'service_port': params.service_port,
            'author': params.author,
            'author_email': params.author_email,
            'endpoint': params.endpoint
        }
    }


def main():
    """Combine required parameters, clone the template, create the service."""
    repo_url = 'git+ssh://git@github.com/skallfass/fastapi_serviceutils_template.git'
    params = _build_arguments(sys.argv[1:])
    create_service_result = _create_service_folder(
        repo_url=repo_url,
        context=_create_context(params),
        output_dir=str(params.output_dir)
    )
    if not create_service_result:
        sys.exit(1)
    print('Service creation successful.')
    print(f'Service is at {params.output_dir}')


if __name__ == '__main__':
    main()
