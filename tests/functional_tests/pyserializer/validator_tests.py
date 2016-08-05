from nose.tools import *  # flake8: noqa
from mock import *  # flake8: noqa

from collections import OrderedDict

from pyserializer.serializers import Serializer
from pyserializer import fields
from pyserializer import validators


class TestValidator:

    def setup(self):
        class UserDeserializer(Serializer):
            email = fields.CharField(
                validators=[validators.RequiredValidator()]
            )
            username = fields.CharField()

            def __repr__(self):
                return '<User(%r)>' % (self.username)

        self.UserDeserializer = UserDeserializer

    def test_simple_validator(self):
        input_data = {
            'username': 'JohnSmith'
        }
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_false(deserializer.is_valid())
        assert_true('email' in deserializer.errors.keys())


class TestValidatorWithNestedSerialization:

    def setup(self):
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

            def __repr__(self):
                return '<Comment(%r)>' % (self.content)

        self.CommentDeserializer = CommentDeserializer

    def test_validator_with_nested_serialization(self):
        input_data = {
            'user': {
                'username': 'JohnSmith',
                'age': 100
            },
            'content': 'foo bar',
            'rating': -2
        }

        deserializer = self.CommentDeserializer(data_dict=input_data)
        deserializer.is_valid()
        error_keys = deserializer.errors.keys()
        assert_false(deserializer.is_valid())
        assert_true('email' in error_keys)
        assert_true('age' in error_keys)
        assert_true('content' in error_keys)
        assert_true('rating' in error_keys)
        assert_equal(
            deserializer.errors['email'],
            [
                OrderedDict([
                    ('type_name', 'RequiredValidator'),
                    ('type_label', 'required'),
                    ('message', 'Value is required.')
                ])
            ]
        )
        assert_equal(
            deserializer.errors['age'],
            [OrderedDict([
                ('type_name', 'MaxValueValidator'),
                ('type_label', 'max_value'),
                ('message', 'Ensure this value is less than or equal to 90.')
            ])]
        )
        assert_equal(
            deserializer.errors['content'],
            [OrderedDict([
                ('type_name', 'MaxLengthValidator'),
                ('type_label', 'max_length'),
                ('message', 'Ensure the value has atmost 3 characters(it has 7 characters).')
            ])]
        )
        assert_equal(
            deserializer.errors['rating'],
            [OrderedDict([
                ('type_name', 'MinValueValidator'),
                ('type_label', 'max_value'),
                ('message', 'Ensure this value is greater than or equal to 0.')
            ])]
        )
