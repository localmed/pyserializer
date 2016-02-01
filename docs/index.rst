==============================
pyserializer User Documentation
==============================

pyserializer
============

`pyserializer` is a simple python serialization/deserialization library. It is an ORM agnostic library for converting python objects to native Python datatypes, and vice versa.


Installation
------------

pyserializer is available on PyPI, so to use it you can use :program:`pip`:

To install pyserializer, simply run::

    $ pip install pyserializer

Alternatively, if you don't have setuptools installed, `download it from PyPi <https://pypi.python.org/pypi/pyserializer>`_ and run::

    $ python setup.py install

Also, you can get the source from `GitHub <https://github.com/localmed/pyserializer>`_ and install it as above::

    $ git clone https://github.com/localmed/pyserializer.git
    $ cd pyserializer
    $ python setup.py install


:doc:`serialization`
  A quick serialization example. Shows examples on how to define your serializer class and serialize a python object to native datatype.


Contribute
----------
Always looking for contributions, additions and improvements.

The source is available on `GitHub <https://github.com/localmed/pyserializer>`_
and contributions are always encouraged.

To contribute, fork the project on
`GitHub <https://github.com/localmed/pyserializer>`_ and submit a
pull request. If you have notices bugs or issues with the library, you can add it to the `Issue Tracker <https://github.com/localmed/pyserializer/issues>`_.

Install development requirements. It is highly recommended that you use a `virtualenv <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_, and activate the virtualenv before installing the requirements.

Install project requirements::

    $ pip install -r requirements.txt

Run tests with coverage::

    $ make unit_test

Run test Using Tox (Runs the tests in different supported python interpreter)::

    $ tox

Run Lint::

    $ make lint

Create a new local branch to submit a pull request::

    $ git checkout -b name-of-feature

Commit your changes::

    $ git commit -m "Detailed commit message"

Push up your changes::

    $ git push origin name-of-feature

Submit a pull request. Before submitting a pull request, make sure pull request add the functionality, it is tested and docs are updated.


License
-------

The project is licensed under the MIT license.

Contents:

.. toctree::
   :maxdepth: 2
   :numbered:

   serialization

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`