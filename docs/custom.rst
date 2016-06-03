======
Custom
======
A quick example on how to create custom Fields and vaildators.


Create Custom Fields
====================

Lets assume we want to create a custom UUID field. Creating a field only requires you to define the ``to_native`` and ``to_python`` on the field class. All custom fields should inherit from ``Field`` class. The class variables ``type_name`` and ``type_label`` are for meta information. Exaple UUID field::

    from pyserializer.fields import Field

    class UUIDField(Field):
        type_name = 'UUIDField'
        type_label = 'string'
        default_error_messages = {
            'invalid': 'The value received for UUIDField (%s) is not a valid UUID format.'
        }

        def __init__(self, *args, **kwargs):
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


Create Custom Validators
========================

Lets assume we want to create a custom validator which validates a max value on the field. Creating a validator only requires you to define the ``__call__`` method on the validator class. All custom validators should inherit from ``BaseValidator`` class. The validator should raise ``ValidationError`` if the validation criteria is not met.
Example MaxValueValidator::

    from pyserializer.validators import BaseValidator
    from pyserializer.exceptions import ValidationError

    class MaxValueValidator(BaseValidator):
        default_error_messages = {
            'invalid': 'Ensure this value is less than or equal to %s.'
        }

        def __init__(self, max_value):
            self.max_value = max_value
            super(MaxValueValidator, self).__init__(*args, **kwargs)

        def __call__(self, value):
            if not self.is_valid(value):
                raise ValidationError(
                    self.default_error_messages['invalid'] % self.max_value
                )

        def is_valid(self, value):
            if isinstance(value, six.string_types):
                value = Decimal(value)
            return self.max_value > value
