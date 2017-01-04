=============
Custom Fields
=============
A quick example on how to create custom fields.


Create Custom Fields
====================

Lets assume we want to create a custom UUID field. Creating a field only requires you to define the ``to_native`` and ``to_python`` on the field class. All custom fields should inherit from ``Field`` class. The class variables ``type_name`` and ``type_label`` are for meta information. Exaple UUID field::

    from pyserializer.fields import Field

    class UUIDField(Field):
        type_name = 'UUIDField'
        type_label = 'string'
        default_error_messages = {
            'invalid': ('The value received for UUIDField (%s)'
                        ' is not a valid UUID format.')
        }
        default_validators = [validators.UUIDValidator()] # All the validations should be handeled by the validator.

        def __init__(self,
                     *args,
                     **kwargs):
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
            return uuid.UUID(str(value))
