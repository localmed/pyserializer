.PHONY: help
help:
	@echo "Please use \`make <target>' where <target> is one of"

	@echo "  unit_test        Runs unit tests and coverage."
	@echo "  lint             Runs lint."


.PHONY: unit_test
unit_test:
	@bin/unit_test

.PHONY: lint
lint:
	@bin/lint
