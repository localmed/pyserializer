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

``` python
from pyserializer.serializers import Serializer
from pyserializer import fields

# Define a serializer class
class UserSerializer(Serializer):
    email = fields.CharField()
    username = fields.CharField()


class CommentSerializer(Serializer):
    user = UserSerializer(source='user') # Eg: Nested serialization
    content = fields.CharField()
    versionName = fields.CharField(source='version.name') # Eg: specifying the source
    created = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ') # Eg: Specify you own datetime format. Defaults to ISO_8601

    class Meta:
        fields = (
            'user',
            'content',
            'versionName',
            'created',
        )

serializer = MySerializer(pyobject)

# Get the serialized data
serializer.data
```

Feature Requests and Bug Reports
--------------------------------

Should all be reported on the Github Issue Tracker

Contribution
------------

Fork pyserializer on Github
``` bash
$ git clone <clone_url>
$ cd pyserializer
```
Install development requirements. It is highly recommended that you use a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/), and activate the virtualenv before installing the requirements.
``` bash
$ pip install -r requirements.txt
```
Install pyserializer in development mode.
``` bash
$ pip install -e .
```
Run tests.
``` bash
$ nosetests
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

- Support deserialization
- Support field validations

Copyright
---------

Copyright (c) 2014 [LocalMed, Inc.](http://www.localmed.com/). See LICENSE for details.
