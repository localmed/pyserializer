==========
Validation
==========
Add validation to fields defined in the serializer class.

Defining our deserailizer class with validators
===============================================
Lets consider a similar example that we used in deserialization example.
Lets assume we have a comment object and the comment object has a user attached to it, Now lets define a deserializer class with validators::

    from pyserializer.serializers import Serializer
    from pyserializer import fields
    from pyserializer import validators

    class UserDeserializer(Serializer):
        email = fields.CharField(
            validators=[
                validators.RequiredValidator(),
                validators.EmailValidator()
            ]
        )
        username = fields.CharField()
        age = fields.IntegerField(
            validators=[validators.MaxValueValidator(max_value=90)]
        )

        class Meta:
            fields = (
                'email',
                'username',
                'age',
            )

        def __repr__(self):
            return '<User(%r)>' % (self.username)

    class CommentDeserializer(Serializer):
        user = UserDeserializer()
        content = fields.CharField(
            validators=[validators.MaxLengthValidator(max_length=3)]
        )
        rating = fields.IntegerField(
            validators=[validators.MinValueValidator(min_value=0)]
        )

        class Meta:
            fields = (
                'user',
                'content',
                'rating',
            )

        def __repr__(self):
            return '<Comment(%r)>' % (self.content)


Validate the object
===================
Lets use the deserializer class we defined above to validate the data dict and deserialize a Python dict::

    data_dict = {
        'user': {
            'username': 'JohnSmith',
            'age': 100
        },
        'content': 'foo bar',
        'rating': -2
    }
    deserializer = CommentDeserializer(data_dict=data_dict)
    deserializer.is_valid()
    # False
    deserializer.errors
    # OrderedDict([('email', ['Value is required.', 'None is an invalid email address.']), ('age', ['Ensure this value is less than or equal to 90.']), ('content', ['Ensure the value has atmost 3 characters(it has 7 characters).']), ('rating', ['Ensure this value is greater than or equal to 0.'])])

