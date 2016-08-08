===============
Deserialization
===============
Deserialization is similar to serialization. Deserialization allows native Python datatypes to be converted to Python objects.

Defining our deserailizer
=========================

Let's consider a similar example that we used in serialization example. Let's assume we have a comment object and the comment object has a user attached to it, Now let's define a deserializer class::

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

        def __repr__(self):
            return '<Comment(%r)>' % (self.content)


Deserialize the object
======================
Let's use the deserializer class we defined above to deserialize a Python dict::

    data_dict = {
        'user': {
            'email': 'foo@example.com',
            'username': 'JohnSmith'
        },
        'content': 'foo bar',
        'created_date': '2015-01-01',
        'created_time': '2012-01-01T16:00:00Z'
    }
    deserializer = CommentDeserializer(data_dict=data_dict)
    deserializer.object.user.username
    'JohnSmith'
    deserializer.object.created_time
    datetime.datetime(2012, 1, 1, 16, 0)


.. note:: If your fields in the deserializer class has validators defined, the validators will run before deserializing the objects. If any error is encountered during the validation process, the ``deserializer.object`` will return ``None``. You can check the error object on the deserializer (``deserializer.errors``) to get detailed information on the errors.
