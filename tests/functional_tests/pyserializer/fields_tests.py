from nose.tools import *  # flake8: noqa
from mock import *  # flake8: noqa

import uuid
import decimal
from datetime import datetime, date
from collections import OrderedDict

from pyserializer import fields
from pyserializer.serializers import Serializer


class TestDateField:

    def setup(self):
        class UserDeserializer(Serializer):
            dob = fields.DateField()

            class Meta:
                fields = (
                    'dob',
                )

            def __repr__(self):
                return '<User(%r)>' % (self.dob)

        self.UserDeserializer = UserDeserializer

    def test_date_field_valid(self):
        date_str = '2016-06-16'
        input_data = {
            'dob': date_str
        }
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_true(deserializer.is_valid())
        assert_equal(
            deserializer.object.dob,
            date(2016, 6, 16)
        )

    def test_date_field_valid_with_date_obj(self):
        dob = date(2016, 6, 16)
        input_data = {
            'dob': dob
        }
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_true(deserializer.is_valid())
        assert_equal(
            deserializer.object.dob,
            date(2016, 6, 16)
        )

    def test_date_field_with_error(self):
        input_data = {
            'dob': '123'
        }
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_false(deserializer.is_valid())
        assert_true('dob' in deserializer.errors.keys())
        assert_equal(
            deserializer.errors,
            OrderedDict(
                [('dob', [OrderedDict([
                    ('type_name', 'DateValidator'),
                    ('type_label', 'date'),
                    ('message', 'Ensure the Date value 123 is of format %Y-%m-%d.')
                ])])]
            )
        )


class TestDateTimeField:

    def setup(self):
        class UserDeserializer(Serializer):
            created_at = fields.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')

            class Meta:
                fields = (
                    'created_at',
                )

            def __repr__(self):
                return '<User(%r)>' % (self.created_at)

        self.UserDeserializer = UserDeserializer

    def test_time_field_valid(self):
        time_str = '2016-06-16T18:21:00Z'
        input_data = {
            'created_at': time_str
        }
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_true(deserializer.is_valid())
        assert_equal(
            deserializer.object.created_at,
            datetime(2016, 6, 16, 18, 21)
        )

    def test_datetime_field_with_datetime_obj(self):
        created_at = datetime(2016, 6, 16, 18, 21)
        input_data = {
            'created_at': created_at
        }
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_true(deserializer.is_valid())
        assert_equal(
            deserializer.object.created_at,
            datetime(2016, 6, 16, 18, 21)
        )

    def test_datetime_field_with_error(self):
        input_data = {
            'created_at': '123'
        }
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_false(deserializer.is_valid())
        assert_true('created_at' in deserializer.errors.keys())
        assert_equal(
            deserializer.errors,
            OrderedDict(
                [('created_at', [OrderedDict([
                    ('type_name', 'DateTimeValidator'),
                    ('type_label', 'date_time'),
                    ('message', 'Ensure the DateTime value 123 is of format %Y-%m-%dT%H:%M:%SZ.')
                ])])]
            )
        )


class TestUUIDField:

    def setup(self):
        class UserDeserializer(Serializer):
            user_id = fields.UUIDField()

            class Meta:
                fields = (
                    'user_id',
                )

            def __repr__(self):
                return '<User(%r)>' % (self.user_id)

        self.UserDeserializer = UserDeserializer

    def test_uuid_field_valid(self):
        input_data = {
            'user_id': 'ffbbc644-42c4-4feb-a144-6500858e25af'
        }
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_true(deserializer.is_valid())
        assert_equal(
            deserializer.object.user_id,
            uuid.UUID(input_data['user_id'])
        )

    def test_uuid_field_with_uuid_obj(self):
        user_id = uuid.UUID('ffbbc644-42c4-4feb-a144-6500858e25af')
        input_data = {
            'user_id': user_id
        }
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_true(deserializer.is_valid())
        assert_equal(deserializer.object.user_id, user_id)

    def test_uuid_field_with_error(self):
        input_data = {
            'user_id': '123'
        }
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_false(deserializer.is_valid())
        assert_true('user_id' in deserializer.errors.keys())
        assert_equal(
            deserializer.errors,
            OrderedDict(
                [('user_id', [OrderedDict([
                    ('type_name', 'UUIDValidator'),
                    ('type_label', 'uuid'),
                    ('message', 'Ensure the value 123 is of type uuid.')
                ])])]
            )
        )


class TestIntegerField:

    def setup(self):
        class UserDeserializer(Serializer):
            age = fields.IntegerField()

            class Meta:
                fields = (
                    'age',
                )

            def __repr__(self):
                return '<User(%r)>' % (self.age)

        self.UserDeserializer = UserDeserializer

    def test_integer_field_valid(self):
        input_data = {
            'age': '10'
        }
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_true(deserializer.is_valid())
        assert_equal(deserializer.object.age, 10)

    def test_integer_field_with_error(self):
        input_data = {
            'age': '10.20'
        }
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_false(deserializer.is_valid())
        assert_true('age' in deserializer.errors.keys())
        assert_equal(
            deserializer.errors,
            OrderedDict(
                [('age', [OrderedDict([
                    ('type_name', 'IntegerValidator'),
                    ('type_label', 'integer'),
                    ('message', 'Ensure the value 10.20 is of type integer.')
                ])])]
            )
        )

    def test_integer_field_with_empty_value(self):
        input_data = {}
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_true(deserializer.is_valid())


class TestFloatField:

    def setup(self):
        class UserDeserializer(Serializer):
            score = fields.FloatField()

            class Meta:
                fields = (
                    'score',
                )

            def __repr__(self):
                return '<User(%r)>' % (self.score)

        self.UserDeserializer = UserDeserializer

    def test_float_field_valid(self):
        input_data = {
            'score': '10.20'
        }
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_true(deserializer.is_valid())
        assert_equal(deserializer.object.score, 10.20)

    def test_float_field_with_error(self):
        input_data = {
            'score': 'wrong_field'
        }
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_false(deserializer.is_valid())
        assert_true('score' in deserializer.errors.keys())
        assert_equal(
            deserializer.errors,
            OrderedDict(
                [('score', [OrderedDict([
                    ('type_name', 'FloatValidator'),
                    ('type_label', 'float'),
                    ('message', 'Ensure the value wrong_field is of type float.')
                ])])]
            )
        )

    def test_float_field_with_empty_value(self):
        input_data = {}
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_true(deserializer.is_valid())


class TestDecimalField:

    def setup(self):
        class UserDeserializer(Serializer):
            amount = fields.DecimalField()

            class Meta:
                fields = (
                    'amount',
                )

            def __repr__(self):
                return '<User(%r)>' % (self.amount)

        self.UserDeserializer = UserDeserializer

    def test_decimal_field_valid(self):
        input_data = {
            'amount': '10.20'
        }
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_true(deserializer.is_valid())
        assert_equal(deserializer.object.amount, decimal.Decimal('10.20'))

    def test_decimal_field_with_error(self):
        input_data = {
            'amount': 'wrong_field'
        }
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_false(deserializer.is_valid())
        assert_true('amount' in deserializer.errors.keys())
        assert_equal(
            deserializer.errors,
            OrderedDict(
                [('amount', [OrderedDict([
                    ('type_name', 'DecimalValidator'),
                    ('type_label', 'decimal'),
                    ('message', 'Ensure the value wrong_field is of type decimal.')
                ])])]
            )
        )

    def test_decimal_field_with_empty_value(self):
        input_data = {}
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_true(deserializer.is_valid())


class TestDictField:

    def setup(self):
        class UserDeserializer(Serializer):
            preference = fields.DictField()

            class Meta:
                fields = (
                    'preference',
                )

            def __repr__(self):
                return '<User(%r)>' % (self.preference)

        self.UserDeserializer = UserDeserializer

    def test_dict_field_valid(self):
        input_data = {
            'preference': {'contact': 'email'}
        }
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_true(deserializer.is_valid())
        assert_equal(deserializer.object.preference, {'contact': 'email'})

    def test_dict_field_with_error(self):
        input_data = {
            'preference': 'wrong_field'
        }
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_false(deserializer.is_valid())
        assert_true('preference' in deserializer.errors.keys())
        assert_equal(
            deserializer.errors,
            OrderedDict(
                [('preference', [OrderedDict([
                    ('type_name', 'DictValidator'),
                    ('type_label', 'dict'),
                    ('message', 'Ensure the value wrong_field is of type dict.')
                ])])]
            )
        )

    def test_dict_field_with_empty_value(self):
        input_data = {}
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_true(deserializer.is_valid())
