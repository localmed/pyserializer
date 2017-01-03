from nose.tools import *  # flake8: noqa
from mock import *  # flake8: noqa

from collections import OrderedDict

from pyserializer import fields
from pyserializer.serializers import Serializer


class TestSetsCustomErrorMessageWhenErrorMessagesArgIsSetWhenDeclaringField:

    def setup(self):
        class UserDeserializer(Serializer):
            age = fields.IntegerField()
            dob = fields.DateField(
                error_messages={'invalid': 'Custom error message.'}
            )

            def __repr__(self):
                return '<User(%r)>' % (self.dob)

        self.UserDeserializer = UserDeserializer

    def test_sets_custom_error_message(self):
        input_data = {
            'age': 'invalid_age',
            'dob': 'invalid_date'
        }
        deserializer = self.UserDeserializer(data_dict=input_data)
        assert_false(deserializer.is_valid())
        assert_equal(
            deserializer.errors['age'],
            [OrderedDict([
                ('type_name', 'IntegerValidator'),
                ('type_label', 'integer'),
                ('message', 'Ensure the value invalid_age is of type integer.')
            ])]
        )
        assert_equal(
            deserializer.errors['dob'],
            [OrderedDict([
                ('type_name', 'DateField'),
                ('type_label', 'date'),
                ('message', 'Custom error message.')
            ])]
        )
