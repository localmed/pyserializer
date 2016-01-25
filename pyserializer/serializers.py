import six
import copy
from collections import OrderedDict


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
        instance: Python object which has to be serialized.
        data_dict: Dictionary object which has to be serialized.
        """
        self.instance = instance
        self.data_dict = data_dict
        self.source = source
        self.many = many
        self.options = self._options_class(self.Meta)
        self.fields = self.get_fields()
        self._data = None
        self._objects = None

        if many and instance is not None and not hasattr(instance, '__iter__'):
            raise ValueError(
                'instance should be a queryset or other iterable with \
                many=True'
            )

    @property
    def object(self):
        return self.restore_objects()

    def restore_objects(self, instance=None):
        """
        Deserialize a dictionary of attributes into an object instance.
        """
        if not self.data_dict:
            raise AttributeError(
                'Cannot restore object unless `data_dict` value is set'
            )
        # Create an instance of the serialized class
        instance = copy.deepcopy(self)
        restored_fields = self.restore_fields(self.data_dict)
        for field_name, field in six.iteritems(self.fields):
            self.restore_object(
                instance=instance,
                field_name=field_name,
                field=field,
                data=restored_fields
            )

        self._objects = instance
        return self._objects

    def restore_object(self, instance, field_name, field, data):
        if isinstance(field, Serializer):
            inst = copy.deepcopy(field)
            for fldname, fld in six.iteritems(field.fields):
                self.restore_object(
                    instance=inst,
                    field_name=fldname,
                    field=fld,
                    data=data.get(field_name)
                )
            return setattr(self, field_name, inst)

        return setattr(instance, field_name, data.get(field_name))

    def restore_fields(self, data):
        """
        Converts a dictionary of data into a dictionary of deserialized fields.
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
        Returns the complete set of fields for the object as a dict.
        """
        # Maintain the order in which the fields were defined
        output = OrderedDict()

        # Get the explicitly declared fields
        base_fields = copy.deepcopy(self.base_fields)
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
        Serializes objects.
        Calls the field_to_native method on each fields.
        """
        # Maintain the order in which the fields were defined
        output = OrderedDict()

        for field_name, field in six.iteritems(self.fields):
            key = field_name
            if isinstance(field, Serializer):
                if field.source:
                    serializable_obj = getattr(obj, field.source)
                else:
                    serializable_obj = getattr(obj, key)
                field.object = serializable_obj
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
