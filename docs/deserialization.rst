===============
Deserialization
===============
Deserialization is similar to serialization. Deserialization allows native Python datatypes to be converted to Python objects.

Defining our deserailizer
========================

Lets consider a similar example taht we used in serialization example. Lets assume we have a comment object and the comment object has a user attached to it, Now lets define a deserializer class::

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


Deserailizer the object
=======================
Lets use the deserializer class we defined above to deserialize a Python dict::

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
