# define the name of the virtual environment directory
VENV := venv

# default target, when make executed without arguments
all: venv

$(VENV)/bin/activate: requirements.txt requirements-dev.txt
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements.txt -r requirements-dev.txt

# venv is a shortcut target
venv: $(VENV)/bin/activate

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

run: venv ## Runs monitor using debug and monitor/integrations.json configuration
	./$(VENV)/bin/python3 -m monitor -log debug -conf monitor/integrations.json

test: venv ## Lint monitor and test	and runs pytest with junit formatting
	./$(VENV)/bin/python3 -m flake8 monitor
	./$(VENV)/bin/python3 -m flake8 test
	./$(VENV)/bin/python3 -m pytest test/monitor -v --junitxml=junit/test-results.xml

publish: test ## Removes existing build, dist and egg, then creates bdist_wheel
	rm -rf build/
	rm -rf dist/
	rm -rf monitor.egg-info/
	./$(VENV)/bin/python3  -m build --sdist --wheel

clean: ## Removes virtual env and pyc
	rm -rf $(VENV)
	rm -rf build/
	rm -rf dist/
	rm -rf monitor.egg-info/
	find . -type f -name '*.pyc' -delete

.PHONY: help all venv run test publish clean