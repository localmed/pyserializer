from nose.tools import *  # flake8: noqa
from mock import *  # flake8: noqa

from collections import OrderedDict

from pyserializer import fields
from pyserializer.serializers import Serializer
from pyserializer import validators


class TestSetsCustomErrorMessageWhenErrorMessagesArgIsSetWhenDeclaringField:

    def setup(self):
        class UserDeserializer(Serializer):
            name = fields.CharField(
                validators=[
                    validators.MaxLengthValidator(3)
                ]
            )
            age = fields.IntegerField(
                validators=[
                    validators.MinValueValidator(18),
                    validators.MaxValueValidator(30)
                ],
                error_messages={
                  'min_value': 'You must be at least 18 years old to signup',
                  'max_value': 'You are too old.'
                }
            )
            dob = fields.DateField(
                error_messages={'invalid': 'Custom error message.'}
            )

            def __repr__(self):
                return '<User(%r)>' % (self.name)

        self.UserDeserializer = UserDeserializer


    def test_sets_custom_error_message(self):
        input_data = {
            'name': 'John Smith',
            'age': 50,
            'dob': 'invalid_date'
        }
        deserializer = self.UserDeserializer(data_dict=input_data)
        assert_false(deserializer.is_valid())
        assert_equal(
            deserializer.errors['name'],
            [OrderedDict([
                ('type_name', 'MaxLengthValidator'),
                ('type_label', 'max_length'),
                ('message', 'Ensure the value has atmost 3 characters(it has 10 characters).')
            ])]
        )
        assert_equal(
            deserializer.errors['age'][0]['type_name'],
            'IntegerField'
        )
        assert_equal(
            deserializer.errors['age'][0]['type_label'],
            'integer'
        )
        assert_equal(
            deserializer.errors['age'][0]['max_value'],
            'You are too old.'
        )
        assert_equal(
            deserializer.errors['age'][0]['min_value'],
            'You must be at least 18 years old to signup'
        )
        assert_equal(
            deserializer.errors['dob'],
            [OrderedDict([
                ('type_name', 'DateField'),
                ('type_label', 'date'),
                ('invalid', 'Custom error message.')
            ])]
        )
