import six
from datetime import datetime, date
import warnings
import uuid

from pyserializer.utils import is_simple_callable, is_iterable
from pyserializer import constants
from pyserializer.constants import ISO_8601


__all__ = [
    'Field',
    'CharField',
    'DateField',
    'DateTimeField',
    'UUIDField',
    'IntegerField',
]


class Field(object):
    """
    A base class for fields in a Serializer.
    """

    type_name = None
    type_label = None
    default_validators = []

    def __init__(self,
                 source=None,
                 label=None,
                 help_text=None,
                 required=True,
                 validators=None,
                 *args,
                 **kwargs):
        """
        :param source: (str) The source name for the field.
            You can use dot syntax to specify nested source. Eg: 'version.name'
        :param label: (optional) The label for the field.
        :param help_text: (optional) The readable help text for the field.
        :param required: (bool) If the field is required or not.
            Defaults to True.
        """
        self.source = source
        self.label = label
        self.help_text = help_text
        self.required = required
        self.validators = self.default_validators + (validators or [])
        self.empty = kwargs.pop('empty', '')

    def field_to_native(self, obj, field_name):
        """
        Given an object and a field name, returns the value that should be
        serialized for that field.
        """
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
        """
        Given an object, and an attribute name,
        returns the attribute on the object.
        """
        if isinstance(obj, dict):
            return obj.get(attr_name)
        else:
            return getattr(obj, attr_name)

    def to_native(self, value):
        """
        Converts the field's value into a serialized representation.
        """
        if is_simple_callable(value):
            value = value()
        if (is_iterable(value) and not
                isinstance(value, (dict, six.string_types))):
            return [self.to_native(item) for item in value]
        if isinstance(value, dict):
            d = {}
            for key, val in six.iteritems(value):
                d[key] = self.to_native(val)
            return d
        return value

    def to_python(self, value):
        """
        Reverts a simple representation back to the field's value.
        """
        return value

    def initialize(self, parent, field_name):
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
    """
    A string field.
    """

    type_name = 'CharField'
    type_label = 'string'

    def __init__(self,
                 *args,
                 **kwargs):
        """
        :param args: Arguments passed directly into the parent
            :class:`~pyserializer.Field`.
        :param kwargs: Keyword arguments passed directly into the parent
            :class:`~pyserializer.Field`.
        """
        super(CharField, self).__init__(*args, **kwargs)


class DateField(Field):
    """
    A date field.
    """

    type_name = 'DateField'
    type_label = 'date'
    format = constants.DATE_FORMAT
    default_error_messages = {
        'invalid': ('The value received for DateField (%s) '
                    'is not a valid Date format (%s).')
    }

    def __init__(self,
                 format=None,
                 *args,
                 **kwargs):
        """
        :param format: The format of the date. Defaults to ISO_8601.
        :param args: Arguments passed directly into the parent
            :class:`~pyserializer.Field`.
        :param kwargs: Keyword arguments passed directly into the parent
            :class:`~pyserializer.Field`.
        """
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

    def to_python(self, value):
        if value in constants.EMPTY_VALUES:
            return None

        if isinstance(value, datetime):
            value = date(value.year, value.month, value.day)
            warnings.warn(
                'DateField received a date object (%s).' % value,
                RuntimeWarning
            )
            return value

        if isinstance(value, date):
            return value

        try:
            value = datetime.strptime(value, self.format).date()
        except (ValueError, TypeError):
            message = (
                self.default_error_messages['invalid'] % (value, self.format)
            )
            raise ValueError(message)
        return value


class DateTimeField(Field):
    """
    A datetime field.
    """

    type_name = 'DateTimeField'
    type_label = 'datetime'
    format = constants.DATETIME_FORMAT
    default_error_messages = {
        'invalid': ('The value received for DateTimeField (%s) '
                    ' is not a valid DateTime format (%s).')
    }

    def __init__(self,
                 format=None,
                 *args,
                 **kwargs):
        """
        :param format: The format of the datetime. Defaults to ISO_8601.
        :param args: Arguments passed directly into the parent
            :class:`~pyserializer.Field`.
        :param kwargs: Keyword arguments passed directly into the parent
            :class:`~pyserializer.Field`.
        """
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

    def to_python(self, value):
        if value in constants.EMPTY_VALUES:
            return None

        if isinstance(value, datetime):
            return value

        if isinstance(value, date):
            value = datetime(value.year, value.month, value.day)
            warnings.warn(
                'DateTimeField received a date (%s) object.' % value,
                RuntimeWarning
            )
            return value

        try:
            value = datetime.strptime(value, self.format)
        except (ValueError, TypeError):
            message = (
                self.default_error_messages['invalid'] % (value, self.format)
            )
            raise ValueError(message)
        return value


class UUIDField(Field):
    """
    A UUID4 field.
    """

    type_name = 'UUIDField'
    type_label = 'string'
    default_error_messages = {
        'invalid': ('The value received for UUIDField (%s)'
                    ' is not a valid UUID format.')
    }

    def __init__(self,
                 *args,
                 **kwargs):
        """
        :param args: Arguments passed directly into the parent
            :class:`~pyserializer.Field`.
        :param kwargs: Keyword arguments passed directly into the parent
            :class:`~pyserializer.Field`.
        """
        super(UUIDField, self).__init__(*args, **kwargs)

    def to_native(self, value):
        if value is None:
            return value
        return six.text_type(value)

    def to_python(self, value):
        if value in constants.EMPTY_VALUES:
            return None

        if isinstance(value, uuid.UUID):
            return value

        try:
            value = uuid.UUID(str(value))
        except (ValueError, TypeError):
            message = self.default_error_messages['invalid'] % value
            raise ValueError(message)
        return value


class IntegerField(Field):
    """
    A integer field.
    """

    type_name = 'IntegerField'
    type_label = 'integer'
    default_error_messages = {
        'invalid': ('The value received for IntegerField (%s)'
                    ' is not a valid Integer format.')
    }

    def __init__(self,
                 *args,
                 **kwargs):
        """
        :param args: Arguments passed directly into the parent
            :class:`~pyserializer.Field`.
        :param kwargs: Keyword arguments passed directly into the parent
            :class:`~pyserializer.Field`.
        """
        super(IntegerField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value in constants.EMPTY_VALUES:
            return None

        try:
            value = int(str(value))
        except (ValueError, TypeError):
            message = self.default_error_messages['invalid'] % value
            raise ValueError(message)
        return value
