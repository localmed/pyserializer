from __future__ import absolute_import

from nose.tools import *
from mock import *

from datetime import datetime

from pyserializer.fields import *


class TestField(object):

    @patch.object(Field, 'to_native')
    @patch.object(Field, 'get_component')
    def test_field_to_native(self, get_component, to_native):
        obj = Mock(name='obj', display='Dr. John Smith')
        Field().field_to_native(obj=obj, field_name='display')
        get_component.assert_called_with(obj, 'display')
        to_native.assert_called_with(get_component())

    def test_get_component_with_object(self):
        obj = Mock(name='obj', display='Dr. John Smith')
        output = Field().get_component(obj, 'display')
        assert_equal(output, 'Dr. John Smith')

    def test_get_component_with_dict(self):
        obj = {'display':'Dr. John Smith'}
        output = Field().get_component(obj, 'display')
        assert_equal(output, 'Dr. John Smith')

    def test_to_native_with_iterable(self):
        output = Field().to_native(['123', '456'])
        assert_equal(output, ['123', '456'])

    def test_to_native_with_dict(self):
        output = Field().to_native({'id': '123'})
        assert_equal(output, {'id': '123'})


class TestDateTimeField(object):

    def test_to_native(self):
        value = datetime(2014, 1, 1, 10, 30)
        output = DateTimeField().to_native(value)
        assert_equal(output, '2014-01-01T10:30:00')

    def test_to_with_specified_format(self):
        value = datetime(2014, 1, 1, 10, 30)
        output = DateTimeField(format='%Y-%m-%dT%H:%M:%SZ').to_native(value)
        assert_equal(output, '2014-01-01T10:30:00Z')
