PACKAGE := typepy
DOCS_DIR := docs
DOCS_BUILD_DIR := $(DOCS_DIR)/_build


.PHONY: setup
setup:
	@pip install --upgrade --upgrade-strategy eager \
		.[build,docs,release,test] \
		autoflake black isort

.PHONY: build
build:
	@make clean
	@tox -e build
	ls -lh dist/*

.PHONY: check
check:
	@tox -e lint
	travis lint

.PHONY: clean
clean:
	@tox -e clean

.PHONY: docs
docs:
	@python setup.py build_sphinx --source-dir=$(DOCS_DIR)/ --build-dir=$(DOCS_BUILD_DIR) --all-files

.PHONY: fmt
fmt:
	@tox -e fmt

.PHONY: readme
readme:
	tox -e readme

.PHONY: release
release:
	@tox -e release
	@make clean
