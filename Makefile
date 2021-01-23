setup:
	PYTHONPATH=$PYTHONPATH:..
	pipenv --python 3
	pipenv install -d
	pipenv run pipenv-setup sync

init:
	pipenv run flake8 monitor
	pipenv run flake8 test

.PHONY: test
test: init
	pipenv run pytest test/monitor -v --junitxml=junit/test-results.xml

.PHONY: debug
debug: init
	pipenv run python3 monitor -log debug -conf monitor/integrations.json


.PHONY: publish
publish: init
	rm -rf build/
	rm -rf dist/
	rm -rf monitor.egg-info/
	pipenv run python3 setup.py sdist bdist_wheel

.PHONY: install-monitor
install-monitor:
	python3 -m pip install dist/monitor-0.1.1-py3-none-any.whl --force-reinstall

