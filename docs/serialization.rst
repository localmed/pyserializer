=============
Serialization
=============

Getting started
===============
If you haven't installed pyserializer, simply use pip to install it like so::

    $ pip install pyserializer

Defining our serailizer
=======================

Define a serializer class::

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


Get the serialized data::

    serializer = CommentSerializer(pyobject)
    serializer.data
