from argparse import ArgumentParser
from argparse import Namespace
from pathlib import Path
from string import ascii_letters
from string import digits

from cookiecutter import generate
from cookiecutter.vcs import clone
from cookiecutter.exceptions import OutputDirExistsException
import yaml


def check_name(name: str, variable_name: str):
    allowed_chars = (
        f'{str(set(ascii_letters.lower()))}_{digits}'
    )
    try:
        assert all(_ in allowed_chars for _ in name)
    except AssertionError:
        print('!!! Creation of service skipped!!!')
        print(f'Invalid {variable_name}: {name}!')
        print('Only ascii-letters and numbers are allowed!')
        exit(1)
    try:
        assert not any(name.startswith(_) for _ in digits)
    except AssertionError:
        print('!!! Creation of service skipped!!!')
        print(f'Invalid {variable_name}: {name}!')
        print('Must not start with number!')
        exit(1)


def build_arguments() -> Namespace:
    parser = ArgumentParser(
        description=(
            'create new service based on fastapi using fastapi_serviceutils.'
        )
    )
    parser.add_argument(
        '-n',
        '--service_name',
        type=str,
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
        '-prom',
        '--use_prometheus',
        action='store_true',
        default=True,
        help='expose metrics for prometheus-usage.'
    )
    parser.add_argument(
        '-ep',
        '--endpoint',
        type=str,
        required=True,
        help=(
            'the name of the endpoint for the service to create. '
            'ATTENTION: only lower ascii-letters, "_" and digits are allowed. '
            'Must not start with a digit!'
        )
    )
    parser.add_argument(
        '-o',
        '--output_dir',
        required=True,
        type=Path
    )
    return parser.parse_args()


def main():
    repo_url = 'git+ssh://git@github.com/skallfass/fastapi_serviceutils_template.git'
    params = build_arguments()
    check_name(name=params.service_name, variable_name='service_name')
    check_name(name=params.endpoint, variable_name='endpoint')
    context = {
        'cookiecutter': {
            'service_name': params.service_name,
            'service_port': params.service_port,
            'author': params.author,
            'author_email': params.author_email,
            'use_prometheus': params.use_prometheus,
            'endpoint': params.endpoint
        }
    }
    try:
        filepath = clone(
            repo_url,
            clone_to_dir='/tmp',
            no_input=False
        )
        generate.generate_files(
            filepath,
            context=context,
            output_dir=str(params.output_dir),
            overwrite_if_exists=False
        )
    except OutputDirExistsException:
        print('Folder already exists!')
        print('Skipped creation of new service!')
        exit(1)
    print('Service creation sucessfull.')
    print(f'Service is at {params.output_dir}')


if __name__ == '__main__':
    main()
