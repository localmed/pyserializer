from __future__ import absolute_import

from nose.tools import *  # flake8: noqa
from mock import *  # flake8: noqa

from datetime import datetime, date
import uuid
import six

from pyserializer.fields import *  # flake8: noqa


class TestCharField:

    def test_to_native_with_string(self):
        output = CharField().to_native('123')
        assert_equal(output, '123')


class TestDateField(object):

    def test_to_native_with_datetime(self):
        value = datetime(2014, 1, 1, 10, 30)
        output = DateField().to_native(value)
        assert_equal(output, '2014-01-01')

    def test_to_native_with_date(self):
        value = datetime(2014, 1, 1, 10, 30)
        output = DateField().to_native(value)
        assert_equal(output, '2014-01-01')

    def test_to_with_specified_format(self):
        value = datetime(2014, 1, 1, 10, 30)
        output = DateField(format='%d/%m/%y').to_native(value)
        assert_equal(output, '01/01/14')

    def test_to_python(self):
        native_date = '2014-01-01'
        output = DateField(format='%Y-%m-%d').to_python(native_date)
        assert_equal(output, date(2014, 1, 1))

    def test_to_python_with_datetime_object(self):
        input_value = datetime(2014, 1, 1, 10, 30)
        output = DateField(format='%Y-%m-%d').to_python(input_value)
        assert_equal(output, date(2014, 1, 1))

    def test_to_python_with_date_object(self):
        input_value = date(2014, 1, 1)
        output = DateField(format='%Y-%m-%d').to_python(input_value)
        assert_equal(output, date(2014, 1, 1))

    def test_to_python_with_empty(self):
        output = DateField(format='%Y-%m-%d').to_python('')
        assert_equal(output, None)


class TestDateTimeField:

    def test_to_native(self):
        value = datetime(2014, 1, 1, 10, 30)
        output = DateTimeField().to_native(value)
        assert_equal(output, '2014-01-01T10:30:00')

    def test_to_with_specified_format(self):
        value = datetime(2014, 1, 1, 10, 30)
        output = DateTimeField(format='%Y-%m-%dT%H:%M:%SZ').to_native(value)
        assert_equal(output, '2014-01-01T10:30:00Z')

    def test_to_python(self):
        input_value = '2014-01-01T10:30:00Z'
        output = DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')\
            .to_python(input_value)
        assert_equal(output, datetime(2014, 1, 1, 10, 30))

    def test_to_python_with_datetime_object(self):
        input_value = datetime(2014, 1, 1, 10, 30)
        output = DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')\
            .to_python(input_value)
        assert_equal(output, datetime(2014, 1, 1, 10, 30))

    def test_to_python_with_date_object(self):
        input_value = date(2014, 1, 1)
        output = DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')\
            .to_python(input_value)
        assert_equal(output, datetime(2014, 1, 1, 0, 0))

    def test_to_python_with_empty(self):
        input_value = ''
        output = DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')\
            .to_python(input_value)
        assert_equal(output, None)


class TestUUIDField:

    def test_to_native(self):
        value = uuid.uuid4()
        output = UUIDField().to_native(value)
        assert_equal(output, six.text_type(value))

    def test_to_python(self):
        value = 'a3a99fba-ccb5-4616-95b8-205dd0cfb84a'
        output = UUIDField().to_python(value)
        assert_equal(output, uuid.UUID(value))

    def test_to_python_with_empty(self):
        value = ''
        output = UUIDField().to_python(value)
        assert_equal(output, None)


class TestIntegerField:

    def test_to_python(self):
        value = '20'
        output = IntegerField().to_python(value)
        assert_equal(output, 20)

    def test_to_python_with_empty(self):
        value = ''
        output = IntegerField().to_python(value)
        assert_equal(output, None)
