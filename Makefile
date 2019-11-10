.DEFAULT_GOAL := help
SHELL := zsh

.PHONY : check clean docker docs finalize info init tests update help
.SILENT: check clean docker docs finalize info init tests update _create_env _update_env

python_meant=$(cat .python-version)
python_used=$(which python)
python_version=$(python --version)
project_version=$(grep 'version = ' pyproject.toml | sed 's/version = //' | sed 's/"//' | sed 's/"//')


# Show info about current project.
info:
	echo "Project:"
	echo "========"
	echo "version: $(value project_version)"
	echo ""
	echo 'Python:'
	echo '======='
	echo "used python: $(value python_used)"
	echo "version:     $(value python_version)"
	echo ""
	echo "Info about current environment:"
	echo '==============================='
	poetry show

# Clean the working directory from temporary files and caches.
clean:
	rm -rf htmlcov; \
	rm -rf *.egg-info; \
	rm -rf dist; \
	rm -rf **/__pycache__; \
	rm -rf docs/_build; \
	rm -rf docs/api; \
	rm -rf .pytest_cache; \
	rm -rf .coverage; \
	rm -rf log; \
	rm -rf pip-wheel-metadata

_create_env:
	poetry install

_update_env:
	poetry update

_coverage_badge:
	coverage-badge -f -o docs/_static/coverage.svg

_lock_it:
	poetry lock
	dephell deps convert --to requirements.txt
	cp requirements.txt docs/doc_requirements.txt

_makefile_doc:
	make help > docs/makefile_help.txt

_extract_docstrings:
	sphinx-apidoc -o docs/api --force --implicit-namespaces --module-first fastapi_serviceutils

_html_documentation:
	PYTHONPATH=. sphinx-build -b html docs docs/_build

_servicetools_doc:
	poetry run create_service --help > docs/create_service_help.txt && \

# Run tests using pytest.
tests:
	docker-compose down; docker-compose up -d; sleep 2; pytest tests; docker-compose down

# Finalize the main env.
finalize: tests _lock_it

# Create sphinx documentation for the project.
docs: tests _coverage_badge _makefile_doc _servicetools_doc _extract_docstrings _html_documentation _lock_it

doc: _makefile_doc _servicetools_doc _extract_docstrings _html_documentation

# Initialize project
init: _create_env _lock_it

# Update environments based on pyproject.toml definitions.
update: _update_env _lock_it

# Run all checks defined in .pre-commit-config.yaml.
check:
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

