import six
from datetime import datetime

from pyserializer.utils import is_simple_callable, is_iterable
from pyserializer import constants
from pyserializer.constants import ISO_8601


__all__ = [
    'Field',
    'CharField',
    'DateField',
    'DateTimeField',
    'UUIDField',
]


class Field(object):

    def __init__(self,
                 source=None,
                 label=None,
                 help_text=None,
                 required=True,
                 *args,
                 **kwargs):
        self.source = source
        self.label = label
        self.help_text = help_text
        self.required = required
        self.empty = kwargs.pop('empty', '')

    def field_to_native(self, obj, field_name):
        '''
        Given an object and a field name, returns the value that should be
        serialized for that field.
        '''
        if obj is None:
            return self.empty
        if not self.source:
            value = self.get_component(obj, field_name)
        else:
            try:
                value = None
                for index, component in enumerate(self.source.split('.')):
                    if index == 0:
                        value = self.get_component(obj, component)
                    else:
                        value = self.get_component(value, component)
            except AttributeError as e:
                if self.required is False:
                    return None
                raise AttributeError(str(e))
        return self.to_native(value)

    def get_component(self, obj, attr_name):
        '''
        Given an object, and an attribute name,
        return that attribute on the object.
        '''
        if isinstance(obj, dict):
            return obj.get(attr_name)
        else:
            return getattr(obj, attr_name)

    def to_native(self, value):
        '''
        Converts the field's value into it's simple representation.
        '''
        if is_simple_callable(value):
            value = value()
        if is_iterable(value) and not isinstance(value, (dict, six.string_types)):
            return [self.to_native(item) for item in value]
        if isinstance(value, dict):
            d = {}
            for key, val in six.iteritems(value):
                d[key] = self.to_native(val)
            return d
        return value

    def initialize(self, parent, field_name):
        '''
        Called to set up a field prior to field_to_native.

        parent - The parent serializer.
        field_name - The name of the field being initialized.
        '''
        self.parent = parent
        self.field_name = field_name

    def metadata(self):
        metadata = {}
        metadata['type'] = self.type_label
        metadata['type_name'] = self.type_name
        metadata['required'] = getattr(self, 'required', False)
        optional_attrs = [
            'label',
            'help_text',
        ]
        for attr in optional_attrs:
            value = getattr(self, attr, None)
            if value is not None and value != '':
                metadata[attr] = '%s' % (value)
        return metadata


class CharField(Field):
    type_name = 'CharField'
    type_label = 'string'

    def __init__(self, *args, **kwargs):
        super(CharField, self).__init__(*args, **kwargs)


class DateField(Field):
    type_name = 'DateField'
    type_label = 'date'
    format = constants.DATE_FORMAT

    def __init__(self, format=None, *args, **kwargs):
        self.format = format or self.format
        super(DateField, self).__init__(*args, **kwargs)

    def to_native(self, value):
        if value is None or self.format is None:
            return value
        if isinstance(value, datetime):
            value = value.date()
        if self.format.lower() == ISO_8601:
            return value.isoformat()
        return value.strftime(self.format)


class DateTimeField(Field):
    type_name = 'DateTimeField'
    type_label = 'datetime'
    format = constants.DATETIME_FORMAT

    def __init__(self, format=None, *args, **kwargs):
        self.format = format or self.format
        super(DateTimeField, self).__init__(*args, **kwargs)

    def to_native(self, value):
        if value is None or self.format is None:
            return value
        if self.format.lower() == ISO_8601:
            ret = value.isoformat()
            if ret.endswith('+00:00'):
                ret = ret[:-6] + 'Z'
            return ret
        return value.strftime(self.format)


class UUIDField(Field):
    type_name = 'UUIDField'
    type_label = 'string'

    def __init__(self, format=None, *args, **kwargs):
        super(UUIDField, self).__init__(*args, **kwargs)

    def to_native(self, value):
        if value is None:
            return value
        return six.text_type(value)


class IntegerField(Field):
    type_name = 'IntegerField'
    type_label = 'integer'

    def __init__(self, format=None, *args, **kwargs):
        super(IntegerField, self).__init__(*args, **kwargs)

