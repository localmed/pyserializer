=============
Serialization
=============
Serializers allow Python objects to be converted to native Python datatypes. The serialized data can then be easily rendered to json.

Getting started
===============
If you haven't installed pyserializer, simply use pip to install it like so::

    $ pip install pyserializer

Example 1: Serialization with many objects
==========================================

Defining our serailizer
-----------------------

Let's start by creating a python object which we can use to demonstrate our serializer. Lets assume we have a user object::

    class User(object):
        def __init__(self, email, username):
            self.email = email
            self.username = username

Now let's define a serializer which we can use to serialize data that corresponds to User object::

    from pyserializer.serializers import Serializer
    from pyserializer import fields

    class UserSerializer(Serializer):
        email = fields.CharField()
        username = fields.CharField()

        class Meta:
            fields = (
                'email',
                'username'
            )

Serailize the object
---------------------
Get the serialized data::

    users = [User(email='foo_1@bar.com', username='foo_1'), User(email='foo_2@bar.com', username='foo_2')]

    serializer = UserSerializer(users, many=True)
    serializer.data
    # [OrderedDict([('email', 'foo_1@bar.com'), ('username', 'foo_1')]), OrderedDict([('email', 'foo_2@bar.com'), ('username', 'foo_2')])]

Get in json serialized format::

    import json
    json.dumps(serializer.data)
    # '[{"email": "foo_1@bar.com", "username": "foo_1"}, {"email": "foo_2@bar.com", "username": "foo_2"}]'


Example 2: Nested Serialization
===============================

Defining our serailizer
-----------------------

Let's start by creating a python object which we can use to demonstrate our serializer. Lets assume we have a comment object and the comment object has a user attached to it::

    from datetime import date, datetime

    class User(object):
        def __init__(self):
            self.email = 'foo@example.com'
            self.username = 'foobar'

    class Comment(object):
        def __init__(self):
            self.user = User()
            self.content = 'Some text content'
            self.created_date = date(2015, 1, 1)
            self.created_time = datetime(2015, 1, 1, 10, 30)

Now lets define a serializer which we can use to serialize data that currospond to User and Comment object::

    from pyserializer.serializers import Serializer
    from pyserializer import fields

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
        createdDate = fields.DateField(source='created_date', format='%d/%m/%y') # Eg: Specify you own datetime format. Defaults to ISO_8601
        created_time = fields.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ') # Eg: Specify you own datetime format. Defaults to ISO_8601

        class Meta:
            fields = (
                'user',
                'content',
                'createdDate',
                'created_time'
            )


Serailize the object
---------------------
Get the serialized data::

    user = User()
    comment = Comment()
    serializer = CommentSerializer(comment)
    serializer.data
    # OrderedDict([('user', OrderedDict([('email', 'foo@example.com'), ('username', 'foobar')])), ('content', 'Some text content'), ('createdDate', '01/01/15'), ('created_time', '2015-01-01T10:30:00Z')])

Get in json serialized format::

    import json
    json.dumps(serializer.data)
    # '{"user": {"email": "foo@example.com", "username": "foobar"}, "content": "Some text content", "createdDate": "01/01/15", "created_time": "2015-01-01T10:30:00Z"}'
