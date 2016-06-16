.PHONY: help
help:
	@echo "Please use \`make <target>' where <target> is one of"

	@echo "  unit_test        Runs unit tests and coverage."
	@echo "  lint             Runs lint."
	@echo "  docs             Buils the docs."
	@echo "  open_docs        Opens the docs in the browser."

.PHONY: unit_test
unit_test:
	@bin/unit_test

.PHONY: lint
lint:
	@bin/lint

.PHONY: docs
docs:
	@cd docs && make html && cd .. && open ./docs/_build/html/index.html

.PHONY: open_docs
open_docs:
	@open ./docs/_build/html/index.html
