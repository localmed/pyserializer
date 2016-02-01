[![Build Status](https://travis-ci.org/localmed/pyserializer.svg?branch=development)](https://travis-ci.org/localmed/pyserializer)

[![Documentation Status](https://readthedocs.org/projects/pyserializer/badge/?version=latest)](http://pyserializer.readthedocs.org/en/latest/?badge=latest)


pyserializer
============

`pyserializer` is a simple python serialization/deserialization library. It is an ORM agnostic library for converting python objects to native Python datatypes, and vice versa.

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

[Contribution](CONTRIBUTING.md)


Features Currently Being Worked On
----------------------------------

- Support field validations

Copyright
---------

Copyright (c) 2016 [LocalMed, Inc.](http://www.localmed.com/). See LICENSE for details.
