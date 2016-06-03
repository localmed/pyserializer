pyserializer
============

Contribution
------------

## Bugfixes and New Features
Before starting to tackle a bugfix or add a new feature, look for existing [issues](https://github.com/localmed/pyserializer/issues) or create one a specific issue or feature request. This way you can avoid working on something that has already been addressed or is being worked on.

## Style Guide
Pyserializer aims to follow [PEP8](https://www.python.org/dev/peps/pep-0008/) including 4 space indents. When possible we try to stick to 79 character line limits.

## Testing
All tests run on [Travis](https://travis-ci.org/localmed/pyserializer/) and pull requests are automatically tested by Travis. Pull requests are encourages to have tests.
You may also submit a simple failing test as a pull request, if you don't know how to fix it, it will be easier for other people to work on it and it may get fixed faster.

## General Guidelines
* If possible avoid breaking backward changes.
* Write inline documentation for new classes and methods.
* Write tests and make sure they pass.
* Add improvements and bug fixes to docs/changelog.rst

## Documentation
To contribute to the [API documentation](http://pyserializer.readthedocs.io/en/latest/) just make your changes to the inline documentation of the appropriate [source code](https://github.com/localmed/pyserializer/tree/master) or [rst file](https://github.com/localmed/pyserializer/tree/master/docs) in a branch and submit a pull request.

## Workflow
Fork pyserializer on Github
``` bash
$ git clone https://github.com/localmed/pyserializer.git
$ cd pyserializer
```
Install development requirements. It is highly recommended that you use a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/), and activate the virtualenv before installing the requirements.
``` bash
$ pip install -r requirements.txt
```
Run tests with coverage.
``` bash
$ make unit_test
```
Run test Using Tox (Runs the tests in different supported python interpreter):
``` bash
$ tox
```

Run Lint:
``` bash
$ make lint
```

Create a new local branch to submit a pull request.
``` bash
$ git checkout -b name-of-feature
```

Commit your changes
``` bash
$ git commit -m "Detailed commit message"
$ git push origin name-of-feature
```

Submit a pull request. Before submitting a pull request, make sure pull request add the functionality, it is tested and docs are updated.
