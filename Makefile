help:
	@IFS=$$'\n' ; \
    help_lines=(`fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//'`); \
    for help_line in $${help_lines[@]}; do \
        IFS=$$'#' ; \
        help_split=($$help_line) ; \
        help_command=`echo $${help_split[0]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
        help_info=`echo $${help_split[2]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
        printf "%-30s %s\n" $$help_command $$help_info ; \
    done

setup: ## Setup pipenv and run pipenv-setup sync
	PYTHONPATH=$PYTHONPATH:..
	pipenv --python 3
	pipenv install -d
	pipenv run pipenv-setup sync

.PHONY: init
init: ## Lint monitor and test
	pipenv run flake8 monitor
	pipenv run flake8 test

.PHONY: test
test: init ## Runs pytest with junit formatting
	pipenv run pytest test/monitor -v --junitxml=junit/test-results.xml

.PHONY: debug
debug: ## Runs monitor using debug and monitor/integrations.json configuration
	pipenv run python3 monitor -log debug -conf monitor/integrations.json

.PHONY: publish
publish: test ## Removes existing build, dist and egg, then creates bdist_wheel
	rm -rf build/
	rm -rf dist/
	rm -rf monitor.egg-info/
	pipenv run python3 setup.py sdist bdist_wheel

.PHONY: install-monitor
install-monitor: publish ## Installs monitor
	python3 -m pip install dist/monitor-0.1.1-py3-none-any.whl --force-reinstall

