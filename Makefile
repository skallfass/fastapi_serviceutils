.DEFAULT_GOAL := help
SHELL := bash

.PHONY : check clean docker docs finalize info init tests update help
.SILENT: check clean docker docs finalize info init tests update _create_devs_env _create_main_env _update_devs_env _update_main_env

python_meant=$(cat .python-version)
python_used=$(which python)
python_version=$(python --version)
project_version=$(grep 'version = ' pyproject.toml | sed 's/version = //' | sed 's/"//' | sed 's/"//')


# Show info about current project.
info:
	echo "Project:"
	echo "========"
	echo "version: $(value project_version)"
	echo "" && \
	echo 'Python:' && \
	echo '=======' && \
	echo "used python: $(value python_used)" && \
	echo "version:     $(value python_version)" && \
	echo "" && \
	echo "Info about current environment:" && \
	echo '===============================' && \
	dephell inspect venv && \
	echo "" && \
	echo "Outdated dependencies:" && \
	echo '=====================' && \
	dephell deps outdated

# Clean the working directory from temporary files and caches.
clean:
	rm -rf htmlcov && \
	rm -rf *.egg-info && \
	rm -rf dist && \
	rm -rf **/__pycache__ && \
	rm -rf **/**/__pycache__ && \
	rm -rf **/**/**/__pycache__ && \
	rm -rf docs/_build && \
	rm -rf docs/api && \
	rm -rf .pytest_cache && \
	rm -f .coverage

_create_devs_env:
	dephell venv create --env devs --python=$(value python_meant)

_update_devs_env:
	dephell deps install --env devs

_create_main_env:
	dephell venv create --env main --python=$(value python_meant)

_update_main_env:
	dephell deps install --env main

# Run tests using pytest.
tests:
	PYTHONPATH=. pytest -s

# Finalize the main env.
finalize: update tests

# Create sphinx documentation for the project.
docs: update
	make help > docs/makefile_help.txt && \
	poetry run create_service --help > docs/create_service_help.txt && \
	coverage-badge -f -o docs/_static/coverage.svg ; \
	sphinx-apidoc -o docs/api --force --module-first fastapi_serviceutils && \
	PYTHONPATH=. sphinx-build -b html docs docs/_build

# Initialize project
init: _create_main_env _create_devs_env _update_main_env _update_devs_env
	poetry lock

# Update environments based on pyproject.toml definitions.
update: _update_main_env _update_devs_env
	poetry lock; \
	dephell deps convert --to requirements.txt && \
	cp requirements.txt docs/doc_requirements.txt

# Run all checks defined in .pre-commit-config.yaml.
check: update
	pre-commit run --all-files

# Show the help prompt.
help:
	@ echo 'Helpers for development of fastapi_serviceutils.'
	@ echo
	@ echo '  Usage:'
	@ echo ''
	@ echo '    make <target> [flags...]'
	@ echo ''
	@ echo '  Targets:'
	@ echo ''
	@ awk '/^#/{ comment = substr($$0,3) } comment && /^[a-zA-Z][a-zA-Z0-9_-]+ ?:/{ print "   ", $$1, comment }' $(MAKEFILE_LIST) | column -t -s ':' | sort
	@ echo ''
	@ echo '  Flags:'
	@ echo ''
	@ awk '/^#/{ comment = substr($$0,3) } comment && /^[a-zA-Z][a-zA-Z0-9_-]+ ?\?=/{ print "   ", $$1, $$2, comment }' $(MAKEFILE_LIST) | column -t -s '?=' | sort
	@ echo ''
	@ echo ''
	@ echo '  Note:'
	@ echo '      This workflow requires the following programs / tools to be installed:'
	@ echo '      - poetry'
	@ echo '      - dephell'
	@ echo '      - pyenv'

