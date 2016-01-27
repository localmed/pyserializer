[![Build Status](https://travis-ci.org/localmed/pyserializer.svg?branch=development)](https://travis-ci.org/localmed/pyserializer)

pyserializer
============

`pyserializer` is a simple python serialization library. It is an ORM agnostic library for converting python objects to and from native Python datatypes.

Installation
------------

You can to use [pip](https://pypi.python.org/pypi/pip) to install pyserializer:
``` bash
$ pip install pyserializer
```
Or using last source:
``` bash
$ pip install git+git://github.com/localmed/pyserializer.git
```

Usage
-----

Serialization Example:
``` python
from pyserializer.serializers import Serializer
from pyserializer import fields

# Define a serializer class
class UserSerializer(Serializer):
    email = fields.CharField()
    username = fields.CharField()

    class Meta:
        fields = (
            'email',
            'username'
        )


class CommentSerializer(Serializer):
    user = UserSerializer(source='user') # Eg: Nested serialization
    content = fields.CharField()
    versionName = fields.CharField(source='version.name') # Eg: specifying the source
    created_date = fields.DateField(format='%d/%m/%y') # Eg: Specify you own datetime format. Defaults to ISO_8601
    created_time = fields.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ') # Eg: Specify you own datetime format. Defaults to ISO_8601

    class Meta:
        fields = (
            'user',
            'content',
            'versionName',
            'created_date',
            'created_time'
        )

serializer = CommentSerializer(pyobject)

# Get the serialized data
serializer.data
```

Deserialization Example:

``` python
from pyserializer.serializers import Serializer
from pyserializer import fields


class UserDeserializer(Serializer):
    email = fields.CharField()
    username = fields.CharField()

    class Meta:
        fields = (
            'email',
            'username'
        )

    def __repr__(self):
        return '<User(%r)>' % (self.username)

class CommentDeserializer(Serializer):
    user = UserDeserializer()
    content = fields.CharField()
    created_date = fields.DateField(format='%Y-%m-%d')
    created_time = fields.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')

    class Meta:
        fields = (
            'user',
            'content',
            'created_date',
            'created_time',
        )

    def __repr__(self):
        return '<Comment(%r)>' % (self.content)

# The dictionary data to be serialized
data_dict = {'user': {'email': 'foo@example.com', 'username': 'JohnSmith'}, 'content': 'foo bar', 'created_date': '2015-01-01', 'created_time': '2012-01-01T16:00:00Z'}

deserializer = CommentDeserializer(data_dict=data_dict)
deserializer.object.user.username
'JohnSmith'
deserializer.object.created_time
datetime.datetime(2012, 1, 1, 16, 0)
```

Feature Requests and Bug Reports
--------------------------------

Should all be reported on the Github Issue Tracker

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
Submit a pull request. Before submitting a pull request, make sure pull request add the functionality, it is tests and docs are updated

Features Currently Being Worked On
----------------------------------

- Support field validations

Copyright
---------

Copyright (c) 2016 [LocalMed, Inc.](http://www.localmed.com/). See LICENSE for details.
