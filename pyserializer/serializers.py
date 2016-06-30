import six
import copy
from collections import OrderedDict

from pyserializer.exceptions import ValidationError
from pyserializer.utils import get_object_by_source


__all__ = [
    'SerializerOptions',
    'SerializerMetaclass',
    'BaseSerializer',
    'Serializer',
]


class SerializerOptions(object):
    """
    Meta class options for Serializer
    """
    def __init__(self, meta):
        self.fields = getattr(meta, 'fields', ())
        self.exclude = getattr(meta, 'exclude', ())


class SerializerMetaclass(type):

    def __new__(cls, name, bases, attrs):
        """
        Arguments passed in to new method are
        upperattr_metaclass, future_class_name, future_class_parents,
        future_class_attr.
        Get Fields defined in parent classes and final class
        """
        new_class = super(
            SerializerMetaclass, cls
        ).__new__(cls, name, bases, attrs)
        parent_fields = new_class.get_parent_fields(bases)
        declared_fields = new_class.get_declared_fields(attrs)
        new_class.set_fields(parent_fields, declared_fields)
        return new_class

    def get_parent_fields(cls, bases):
        fields = OrderedDict()
        for base in bases:
            if hasattr(base, 'base_fields'):
                fields.update(base.base_fields)
        return fields

    def get_declared_fields(cls, attrs):
        fields = OrderedDict()
        for field_name, obj in six.iteritems(attrs):
            # if isinstance(obj, Field):
            fields[field_name] = attrs.get(field_name)
        return fields

    def set_fields(cls, parent_fields, declared_fields):
        cls.base_fields = OrderedDict()
        cls.base_fields.update(parent_fields)
        cls.base_fields.update(declared_fields)


class BaseSerializer(object):
    """
    This is the Serializer implementation.
    """

    _options_class = SerializerOptions

    class Meta(object):
        pass

    def __init__(self,
                 instance=None,
                 data_dict=None,
                 source=None,
                 many=False,
                 *args,
                 **kwargs):
        """
        :param instance: Python object which has to be serialized.
        :param data_dict: Dictionary object which has to be deserialized.
        :param source: The source name.
        """
        self.instance = instance
        self.data_dict = data_dict
        self.source = source
        self.many = many
        self.options = self._options_class(self.Meta)
        self.fields = self.get_fields()
        self._data = None
        self._object = None
        self._errors = None

        if many and instance is not None and not hasattr(instance, '__iter__'):
            msg = ('`instance` should be a queryset or other iterable with '
                   'many=True')
            raise ValueError(msg)

    @property
    def errors(self):
        """
        Runs the deserialization and returns any validations errors.
        Also, sets the object property if no errors occurred during validation.
        """
        if self._errors is None:
            self.perform_validation(
                fields=self.fields,
                data=self.data_dict
            )
        return self._errors

    def is_valid(self):
        return not self.errors

    def perform_validation(self, fields, data):
        """
        Runs the validators specified on the fields.
        """
        # Reset the `self_errors` dict, and run the validation
        self._errors = OrderedDict()
        for field_name, field in six.iteritems(fields):
            if isinstance(field, Serializer):
                self.perform_validation(
                    fields=field.fields,
                    data=data.get(field_name)
                )
            else:
                self.invoke_validators(
                    field_name=field_name,
                    validators=field.validators,
                    value=data.get(field_name)
                )

    def invoke_validators(self,
                          field_name,
                          validators,
                          value):
        """
        Calls the validators on the fields.
        Catches the `ValidationError` raised and stores the
        validation error message to `self._errors` object.
        """
        self._errors[field_name] = []
        for validator in validators:
            try:
                validator(value)
            except ValidationError as e:
                validator.error_dict['message'] = str(e)
                self._errors[field_name].append(validator.error_dict)
        # Delete the key from the dict, if no error is appended to the list
        if not self._errors[field_name]:
            del self._errors[field_name]

    @property
    def object(self):
        """
        The deserialized object.
        Runs the validators and checks the error object
        before deserializing the object .
        Caches the object once created.
        Uses the cached version next time when the object property is accessed.
        """
        if not self._object and self.is_valid():
            self._object = self.restore_object()
        return self._object

    def restore_object(self, instance=None):
        """
        Deserialize a dictionary of attributes into an object instance.

        :param instance: The isntance on which the
            deserialized object should be set.
        """
        if not self.data_dict:
            raise AttributeError(
                'Cannot restore object unless `data_dict` value is set'
            )
        # Create an instance of the Serializer class
        instance = copy.copy(self)
        restored_fields = self.restore_fields(self.data_dict)
        for field_name, field in six.iteritems(self.fields):
            self.set_field_value_on_instance(
                instance=instance,
                field_name=field_name,
                field=field,
                data=restored_fields
            )
        return instance

    def set_field_value_on_instance(self,
                                    instance,
                                    field_name,
                                    field,
                                    data):
        """
        Fetches the field value from data and,
        sets the field name and value of the field on the instance.
        """
        if isinstance(field, Serializer):
            inst = copy.deepcopy(field)
            for fldname, fld in six.iteritems(field.fields):
                self.set_field_value_on_instance(
                    instance=inst,
                    field_name=fldname,
                    field=fld,
                    data=data.get(field_name)
                )
            return setattr(instance, field_name, inst)

        return setattr(instance, field_name, data.get(field_name))

    def restore_fields(self, data):
        """
        Converts a dictionary of data into a dictionary of deserialized fields.

        :param data: The data dictionary passed in to be deserialized.
        """
        output = {}

        if data is None and not isinstance(data, dict):
            raise ValueError('%s must be a  instance of dict.' % data)

        for field_name, field in six.iteritems(self.fields):
            fldname, value = self.restore_field(field_name, field, data)
            output[fldname] = value
        return output

    def restore_field(self, field_name, field, data):
        """
        Given a field and a deserializable data dictionary,
        fetches the relevent field data from the data dictionary and
        returns the deserialized version of the field data
        along with the field name.
        Calls the to_python method on each field.

        :param field_name: The field name.
        :param field: The field object.
        :param data: The data dictionary which contains restored field objects.
        """
        if isinstance(field, Serializer):
            nested_field_name = field_name
            nested_data = data.get(nested_field_name)
            output = {}
            for fldname, fld in six.iteritems(field.fields):
                name, python_value = self.restore_field(
                    field_name=fldname,
                    field=fld,
                    data=nested_data
                )
                output[name] = python_value
            return nested_field_name, output

        return field_name, field.to_python(data.get(field_name))

    def get_fields(self):
        """
        Returns the complete set of fields defined in the Serializer
        class as a dict.
        """
        # Maintain the order in which the fields were defined
        output = OrderedDict()

        # Get the explicitly declared fields
        base_fields = copy.copy(self.base_fields)
        for key, field in six.iteritems(base_fields):
            output[key] = field

        # Check for specified fields.
        if self.options.fields:
            if not isinstance(self.options.fields, (list, tuple)):
                raise ValueError('`fields` must be a list or tuple.')
            d = OrderedDict()
            for key in self.options.fields:
                d[key] = output[key]
            output = d

        # Remove anything in 'exclude'
        if self.options.exclude:
            if not isinstance(self.options.fields, (list, tuple)):
                raise ValueError('`exclude` must be a list or tuple.')
            for key in self.options.exclude:
                output.pop(key, None)
        return output

    def to_native(self, obj):
        """
        Serializes objects. Calls the field_to_native method on each fields.

        :param obj: The python object passed in to be serialized.
        """
        # Maintain the order in which the fields were defined
        output = OrderedDict()

        for field_name, field in six.iteritems(self.fields):
            key = field_name
            if isinstance(field, Serializer):
                if field.source:
                    serializable_obj = get_object_by_source(obj, field.source)
                else:
                    serializable_obj = getattr(obj, key)
                field.instance = serializable_obj
                value = field.data
            else:
                field.initialize(parent=self, field_name=field_name)
                value = field.field_to_native(obj, field_name)
            output[key] = value
        return output

    @property
    def data(self):
        """
        Returns the serialized data on the serializer.
        Caches the data once created.
        Uses the cached version next time when the data property is accessed.
        """
        if not self._data:
            obj = self.instance
            if isinstance(obj, (list, tuple)):
                self._data = [self.to_native(item) for item in obj]
            else:
                self._data = self.to_native(obj)
        return self._data

    def metadata(self):
        """
        Return a dictionary of metadata about the fields on the serializer.
        """
        return dict(
            (field_name, field.metadata()) for field_name, field in six.iteritems(self.fields)
        )


class Serializer(six.with_metaclass(SerializerMetaclass, BaseSerializer)):
    """
    Create the serializer class with Meta class and BaseSerializer
    """
    pass
