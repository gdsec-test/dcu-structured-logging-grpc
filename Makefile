all: init

init:
	pip install -r test_requirements.txt
	pip install -r requirements.txt

.PHONY: unit-test
unit-test:
	@echo "----- No unit tests-----"

.PHONY: testcov
testcov:
	@echo "----- No tests to run for coverage-----"

.PHONY: flake8
flake8:
	@echo "----- Running linter -----"
	flake8 --config ./.flake8 .

.PHONY: isort
isort:
	@echo "----- Optimizing imports -----"
	isort --atomic --skip pb --skip .venv .

.PHONY: tools
tools: flake8 isort