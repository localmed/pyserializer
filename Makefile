.PHONY: help
help:
	@echo "Please use \`make <target>' where <target> is one of"

	@echo "  unit_test        Runs unit tests and coverage."
	@echo "  lint             Runs lint."
	@echo "  docs             Buils the docs."
	@echo "  open_docs        Opens the docs in the browser."
	@echo "  publish_test     Publishes the lib to pypi test server. Make sure ~/.pypirc is set up correctly. See .pypirc.example for example."
	@echo "  publish          Publishes the lib to pypi. Make sure ~/.pypirc is set up correctly. See .pypirc.example for example."
	@echo "  clean            Cleans the temp files and folders."
	@echo "  watch_doc        Starts up the docs server and autobuilds the doc when file changes."

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

.PHONY: publish_test
publish_test:
	@python setup.py sdist upload -r pypitest

.PHONY: publish
publish:
	@python setup.py sdist upload -r pypipersonal

.PHONY: clean
clean:
	@rm -rf dist && rm -rf pyserializer.egg-info

.PHONY: watch_doc
watch_doc:
	@bin/watch_doc
