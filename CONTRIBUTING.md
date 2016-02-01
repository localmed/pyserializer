pyserializer
============

Contribution
------------

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
