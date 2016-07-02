from nose.tools import *  # flake8: noqa
from mock import *  # flake8: noqa

import uuid
import decimal
import json
from datetime import datetime, date
from collections import OrderedDict

from pyserializer import fields
from pyserializer.serializers import Serializer


class TestDateFieldDeserializer:

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


class TestDateFieldSerializer:

    def setup(self):
        class UserSerializer(Serializer):
            dob = fields.DateField()

            class Meta:
                fields = (
                    'dob',
                )

            def __repr__(self):
                return '<User(%r)>' % (self.dob)

        self.UserSerializer = UserSerializer

    def test_date_field(self):
        class User:
            def __init__(self):
                self.dob = date(1985, 10, 10)

        expected_output = {
            'dob': '1985-10-10'
        }
        user = User()
        serializer = self.UserSerializer(user)
        serialized_json = json.loads(json.dumps(serializer.data))
        assert_equal(serialized_json, expected_output)


class TestDateTimeFieldDeserializer:

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


class TestDateTimeFieldSerializer:

    def setup(self):
        class UserSerializer(Serializer):
            created_at = fields.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')

            class Meta:
                fields = (
                    'created_at',
                )

            def __repr__(self):
                return '<User(%r)>' % (self.created_at)

        self.UserSerializer = UserSerializer

    def test_datetime_field(self):
        class User:
            def __init__(self):
                self.created_at = datetime(1985, 10, 10, 10, 30)

        expected_output = {
            'created_at': '1985-10-10T10:30:00Z'
        }
        user = User()
        serializer = self.UserSerializer(user)
        serialized_json = json.loads(json.dumps(serializer.data))
        assert_equal(serialized_json, expected_output)


class TestUUIDFieldDeserializer:

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


class TestUUIDFieldSerializer:

    def setup(self):
        class UserSerializer(Serializer):
            user_id = fields.UUIDField()

            class Meta:
                fields = (
                    'user_id',
                )

            def __repr__(self):
                return '<User(%r)>' % (self.user_id)

        self.UserSerializer = UserSerializer

    def test_uuid_field(self):
        class User:
            def __init__(self):
                self.user_id = uuid.UUID('14e2e05e-4eab-478c-8677-907d09aed856')

        expected_output = {
            'user_id': '14e2e05e-4eab-478c-8677-907d09aed856'
        }
        user = User()
        serializer = self.UserSerializer(user)
        serialized_json = json.loads(json.dumps(serializer.data))
        assert_equal(serialized_json, expected_output)


class TestIntegerFieldDeserializer:

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


class TestIntegerFieldSerializer:

    def setup(self):
        class UserSerializer(Serializer):
            age = fields.IntegerField()

            class Meta:
                fields = (
                    'age',
                )

            def __repr__(self):
                return '<User(%r)>' % (self.age)

        self.UserSerializer = UserSerializer

    def test_integer_field(self):
        class User:
            def __init__(self):
                self.age = 20

        expected_output = {
            'age': 20
        }
        user = User()
        serializer = self.UserSerializer(user)
        serialized_json = json.loads(json.dumps(serializer.data))
        assert_equal(serialized_json, expected_output)


class TestFloatFieldDeserializer:

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


class TestFloatFieldSerializer:

    def setup(self):
        class UserSerializer(Serializer):
            score = fields.FloatField()

            class Meta:
                fields = (
                    'score',
                )

            def __repr__(self):
                return '<User(%r)>' % (self.score)

        self.UserSerializer = UserSerializer

    def test_float_field(self):
        class User:
            def __init__(self):
                self.score = 20.22

        expected_output = {
            'score': 20.22
        }
        user = User()
        serializer = self.UserSerializer(user)
        serialized_json = json.loads(json.dumps(serializer.data))
        assert_equal(serialized_json, expected_output)


class TestDecimalFieldDeserializer:

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


class TestDecimalFieldSerializer:

    def setup(self):
        class UserSerializer(Serializer):
            amount = fields.DecimalField()

            class Meta:
                fields = (
                    'amount',
                )

            def __repr__(self):
                return '<User(%r)>' % (self.amount)

        self.UserSerializer = UserSerializer

    def test_decimal_field(self):
        class User:
            def __init__(self):
                self.amount = 20.22

        expected_output = {
            'amount': 20.22
        }
        user = User()
        serializer = self.UserSerializer(user)
        serialized_json = json.loads(json.dumps(serializer.data))
        assert_equal(serialized_json, expected_output)


class TestDictFieldDeserializer:

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


class TestDictFieldSerializer:

    def setup(self):
        class UserSerializer(Serializer):
            preference = fields.DictField()

            class Meta:
                fields = (
                    'preference',
                )

            def __repr__(self):
                return '<User(%r)>' % (self.preference)

        self.UserSerializer = UserSerializer

    def test_dict_field(self):
        class User:
            def __init__(self):
                self.preference = {'contact': 'email'}

        expected_output = {
            'preference': {'contact': 'email'}
        }
        user = User()
        serializer = self.UserSerializer(user)
        serialized_json = json.loads(json.dumps(serializer.data))
        assert_equal(serialized_json, expected_output)


class TestBooleanFieldDeserializer:

    def setup(self):
        class UserDeserializer(Serializer):
            enabled = fields.BooleanField()

            class Meta:
                fields = (
                    'enabled',
                )

            def __repr__(self):
                return '<User(%r)>' % (self.enabled)

        self.UserDeserializer = UserDeserializer

    def test_boolean_field_valid(self):
        input_data = {
            'enabled': 'True'
        }
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_true(deserializer.is_valid())
        assert_equal(deserializer.object.enabled, True)

    def test_boolean_field_with_error(self):
        input_data = {
            'enabled': 'wrong_field'
        }
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_false(deserializer.is_valid())
        assert_true('enabled' in deserializer.errors.keys())
        assert_equal(
            deserializer.errors,
            OrderedDict(
                [('enabled', [OrderedDict([
                    ('type_name', 'BooleanValidator'),
                    ('type_label', 'boolean'),
                    ('message', 'Ensure the value wrong_field is a boolean.')
                ])])]
            )
        )

    def test_boolean_field_with_empty_value(self):
        input_data = {}
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_true(deserializer.is_valid())


class TestBooleanFieldSerializer:

    def setup(self):
        class UserSerializer(Serializer):
            enabled = fields.BooleanField()

            class Meta:
                fields = (
                    'enabled',
                )

            def __repr__(self):
                return '<User(%r)>' % (self.enabled)

        self.UserSerializer = UserSerializer

    def test_dict_field(self):
        class User:
            def __init__(self):
                self.enabled = True

        expected_output = {
            'enabled': True
        }
        user = User()
        serializer = self.UserSerializer(user)
        serialized_json = json.loads(json.dumps(serializer.data))
        assert_equal(serialized_json, expected_output)


class TestRawFieldDeserializer:

    def setup(self):
        class UserDeserializer(Serializer):
            notes = fields.RawField()

            class Meta:
                fields = (
                    'notes',
                )

            def __repr__(self):
                return '<User(%r)>' % (self.notes)

        self.UserDeserializer = UserDeserializer

    def test_raw_field_valid(self):
        input_data = {
            'notes': 'some note'
        }
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_true(deserializer.is_valid())
        assert_equal(deserializer.object.notes, 'some note')

    def test_raw_field_with_empty_value(self):
        input_data = {}
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_true(deserializer.is_valid())


class TestRawFieldSerializer:

    def setup(self):
        class UserSerializer(Serializer):
            note = fields.RawField()

            class Meta:
                fields = (
                    'note',
                )

            def __repr__(self):
                return '<User(%r)>' % (self.note)

        self.UserSerializer = UserSerializer

    def test_note_field(self):
        class User:
            def __init__(self):
                self.note = 'some note'

        expected_output = {
            'note': 'some note'
        }
        user = User()
        serializer = self.UserSerializer(user)
        serialized_json = json.loads(json.dumps(serializer.data))
        assert_equal(serialized_json, expected_output)


class TestUrlFieldDeserializer:

    def setup(self):
        class UserDeserializer(Serializer):
            url = fields.UrlField()

            class Meta:
                fields = (
                    'url',
                )

            def __repr__(self):
                return '<User(%r)>' % (self.url)

        self.UserDeserializer = UserDeserializer

    def test_url_field_valid(self):
        input_data = {
            'url': 'https://www.foobar.com/'
        }
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_true(deserializer.is_valid())
        assert_equal(deserializer.object.url, 'https://www.foobar.com/')

    def test_url_field_with_basic_auth_and_port(self):
        input_data = {
            'url': 'https://user:password>@foobar.com:8080'
        }
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_true(deserializer.is_valid())
        assert_equal(deserializer.object.url, 'https://user:password>@foobar.com:8080')

    def test_url_field_with_invalid_scheme(self):
        input_data = {
            'url': 'ps://www.foobar.com/'
        }
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_false(deserializer.is_valid())
        assert_true('url' in deserializer.errors.keys())
        assert_equal(
            deserializer.errors,
            OrderedDict(
                [('url', [OrderedDict([
                    ('type_name', 'UrlValidator'),
                    ('type_label', 'url'),
                    ('message', 'Ensure the value ps://www.foobar.com/ is a valid URL.')
                ])])]
            )
        )

    def test_url_field_with_empty_value(self):
        input_data = {}
        deserializer = self.UserDeserializer(data_dict=input_data)
        deserializer.is_valid()
        assert_true(deserializer.is_valid())


class TestUrlFieldSerializer:

    def setup(self):
        class UserSerializer(Serializer):
            url = fields.UrlField()

            class Meta:
                fields = (
                    'url',
                )

            def __repr__(self):
                return '<User(%r)>' % (self.url)

        self.UserSerializer = UserSerializer

    def test_url_field(self):
        class User:
            def __init__(self):
                self.url = 'https://www.foobar.com/'

        expected_output = {
            'url': 'https://www.foobar.com/'
        }
        user = User()
        serializer = self.UserSerializer(user)
        serialized_json = json.loads(json.dumps(serializer.data))
        assert_equal(serialized_json, expected_output)


class TestMethodFieldSerializer:

    def setup(self):
        class UserSerializer(Serializer):
            first_name = fields.CharField()
            last_name = fields.CharField()
            full_name = fields.MethodField(
                method_name='get_full_name'
            )

            def get_full_name(self, obj):
                return '{0} {1}'.format(
                    obj.first_name,
                    obj.last_name
                )

            class Meta:
                fields = (
                    'first_name',
                    'last_name',
                    'full_name',
                )

            def __repr__(self):
                return '<User(%r)>' % (self.full_name)

        self.UserSerializer = UserSerializer

    def test_method_field(self):
        class User:
            def __init__(self):
                self.first_name = 'John'
                self.last_name = 'Smith'

        expected_output = {
            'first_name': 'John',
            'last_name': 'Smith',
            'full_name': 'John Smith'
        }
        user = User()
        serializer = self.UserSerializer(user)
        serialized_json = json.loads(json.dumps(serializer.data))
        assert_equal(serialized_json, expected_output)
