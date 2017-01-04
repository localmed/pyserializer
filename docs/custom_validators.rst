=================
Custom Validators
=================
A quick example on how to create custom validators.


Create Custom Validators
========================

Lets assume we want to create a custom validator which validates a max value on the field. Creating a validator only requires you to define the ``__call__`` method on the validator class. All custom validators should inherit from ``BaseValidator`` class. The validator should raise ``ValidationError`` if the validation criteria is not met.
Example MaxValueValidator::

    from pyserializer.validators import BaseValidator
    from pyserializer.exceptions import ValidationError


    class MaxValueValidator(BaseValidator):
        """
        A max value validator.
        """
        type_name = 'MaxValueValidator'
        type_label = 'max_value'
        default_error_messages = {
            'invalid': 'Ensure this value is less than or equal to {max_value}.'
        }

        def __init__(self,
                     max_value,
                     *args,
                     **kwargs):
            """
            :param max_value: (required) A maximum value in integer.
                This will ensure that the value passed in to this validator
                is less than or equal to max_value.
            """
            self.max_value = max_value
            super(MaxValueValidator, self).__init__(*args, **kwargs)

        def __call__(self, value):
            # Only run the validator
            # if the value is not empty ie: (None, '', [], (), {})
            if value not in constants.EMPTY_VALUES and not self.is_valid(value):
                self.fail('invalid', max_value=self.max_value)

        def is_valid(self, value):
            if isinstance(value, six.string_types):
                value = Decimal(value)
            return self.max_value > value
