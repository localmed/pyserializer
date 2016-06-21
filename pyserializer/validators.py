import six
import re
import uuid
import copy
from encodings import idna
from decimal import Decimal
from collections import OrderedDict
from datetime import datetime, date
from pyserializer.exceptions import ValidationError
from pyserializer.utils import force_str
from pyserializer import constants


__all__ = [
    'BaseValidator',
    'RequiredValidator',
    'MaxValueValidator',
    'MinValueValidator',
    'MaxLengthValidator',
    'MinLengthValidator',
    'EmailValidator',
    'NumberValidator',
    'IntegerValidator',
    'FloatValidator',
    'UUIDValidator',
    'DateTimeOrDateValidator',
]


class BaseValidator(object):
    """
    A base class for validators.
    """
    type_name = None
    type_label = None
    default_error_messages = {
        'invalid': 'Not valid.'
    }

    def __init__(self, *args, **kwargs):
        error_messages = copy.deepcopy(self.default_error_messages)
        error_messages.update(kwargs.pop('error_messages', {}))
        self.error_messages = error_messages
        self.error_dict = OrderedDict([
            ('type_name', kwargs.pop('type_name', self.type_name)),
            ('type_label', kwargs.pop('type_label', self.type_label)),
            ('message', self.error_messages['invalid'])
        ])

    def __call__(self, value):
        # Only run the validator
        # if the value is not empty ie: (None, '', [], (), {})
        if value not in constants.EMPTY_VALUES and not self.is_valid(value):
            self.fail('invalid')

    def is_valid(self, value):
        raise NotImplementedError(
            '`is_valid` should be implemented by the child class.'
        )

    def fail(self, key, **kwargs):
        """
        A helper method to raise `ValidationError`
        """
        try:
            msg = self.error_messages[key]
            if kwargs:
                msg = msg.format(**kwargs)
        except KeyError:
            class_name = self.__class__.__name__
            msg = constants.MISSING_ERROR_MESSAGE.format(
                class_name=class_name,
                key=key
            )
            raise AssertionError(msg)
        raise ValidationError(msg)


class RequiredValidator(BaseValidator):
    """
    A required field validator.
    """
    type_name = 'RequiredValidator'
    type_label = 'required'
    default_error_messages = {
        'invalid': 'Value is required.'
    }

    def __call__(self, value):
        if not self.is_valid(value):
            self.fail('invalid')

    def is_valid(self, value):
        if value in constants.EMPTY_VALUES:
            return False
        return True


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


class MinValueValidator(BaseValidator):
    """
    A min value validator.
    """
    type_name = 'MinValueValidator'
    type_label = 'max_value'
    default_error_messages = {
        'invalid': 'Ensure this value is greater than or equal to {min_value}.'
    }

    def __init__(self,
                 min_value,
                 *args,
                 **kwargs):
        """
        :param min_value: (required) A minimum value in integer.
            This will ensure that the value passed in to this validator
            is greater than or equal to min_value.
        """
        self.min_value = min_value
        super(MinValueValidator, self).__init__(*args, **kwargs)

    def __call__(self, value):
        # Only run the validator
        # if the value is not empty ie: (None, '', [], (), {})
        if value not in constants.EMPTY_VALUES and not self.is_valid(value):
            self.fail('invalid', min_value=self.min_value)

    def is_valid(self, value):
        if isinstance(value, six.string_types):
            value = Decimal(value)
        return value >= self.min_value


class MaxLengthValidator(BaseValidator):
    """
    A mix length validator.
    """
    type_name = 'MaxLengthValidator'
    type_label = 'max_length'
    default_error_messages = {
        'invalid': ('Ensure the value has atmost {max_lenght} characters'
                    '(it has {lenght} characters).')
    }

    def __init__(self,
                 max_length,
                 *args,
                 **kwargs):
        """
        :param max_length: (required) A maximum length value in integer.
            This will ensure that the value passed in to this validator
            will have atmost max_length characters.
        """
        self.max_length = max_length
        super(MaxLengthValidator, self).__init__(*args, **kwargs)

    def __call__(self, value):
        # Only run the validator
        # if the value is not empty ie: (None, '', [], (), {})
        if value not in constants.EMPTY_VALUES:
            value = force_str(value)
            value_length = len(value)
            if not self.is_valid(value_length):
                self.fail(
                    'invalid',
                    max_lenght=self.max_length,
                    lenght=value_length
                )

    def is_valid(self, value_length):
        return value_length <= self.max_length


class MinLengthValidator(BaseValidator):
    """
    A min length validator.
    """
    type_name = 'MinLengthValidator'
    type_label = 'min_length'
    default_error_messages = {
        'invalid': ('Ensure the value has atlest {min_length} characters'
                    '(it has {lenght} characters).')
    }

    def __init__(self,
                 min_length,
                 *args,
                 **kwargs):
        """
        :param min_length: (required) A minimum length value in integer.
            This will ensure that the value passed in to this validator
            will have atleast min_length characters.
        """
        self.min_length = min_length
        super(MinLengthValidator, self).__init__(*args, **kwargs)

    def __call__(self, value):
        # Only run the validator
        # if the value is not empty ie: (None, '', [], (), {})
        if value not in constants.EMPTY_VALUES:
            value = force_str(value)
            value_length = len(value)
            if not self.is_valid(value_length):
                self.fail(
                    'invalid',
                    min_length=self.min_length,
                    lenght=value_length
                )

    def is_valid(self, value_length):
        return value_length >= self.min_length


class EmailValidator(BaseValidator):
    """
    A email validator.
    """
    type_name = 'EmailValidator'
    type_label = 'email'
    default_error_messages = {
        'invalid': '{value} is an invalid email address.'
    }
    user_regex = re.compile(r"^[\w!#$%&'*+\-/=?^`{|}~.]+$")
    domain_regex = re.compile(r'''
        ^(?:[a-z0-9][a-z0-9\-]{,62}\.)+        # subdomain
        (?:[a-z]{2,63}|xn--[a-z0-9\-]{2,59})$  # top level domain
    ''', re.I | re.VERBOSE)
    domain_blacklist = []

    def __init__(self,
                 domain_blacklist=None,
                 *args,
                 **kwargs):
        """
        :param domain_blacklist: (optional) A list of domains which should be
            considered as invalid. Defaults to an empty list.
        """
        if domain_blacklist:
            self.domain_blacklist = domain_blacklist
        super(EmailValidator, self).__init__(*args, **kwargs)

    def __call__(self, value):
        # Only run the validator
        # if the value is not empty ie: (None, '', [], (), {})
        if value not in constants.EMPTY_VALUES:
            value = force_str(value)
            if not self.is_valid(value):
                self.fail('invalid', value=value)

    def is_valid(self, value):
        if not value or '@' not in value:
            return False

        user_part, domain_part = value.rsplit('@', 1)
        if domain_part in self.domain_blacklist:
            return False

        if not self.user_regex.match(user_part):
            return False

        try:
            idna_domain = [idna.ToASCII(p) for p in domain_part.split('.')]
            idna_domain = [p.decode('ascii') for p in idna_domain]
            idna_domain = '.'.join(idna_domain)
        except UnicodeError:
            # UnicodeError: label empty or too long
            # This exception might happen if we have an invalid domain
            # name part (for example test@.foo.bar.com)
            raise False

        if not self.domain_regex.match(domain_part):
            return False
        return True


class NumberValidator(BaseValidator):
    """
    A number validator. The default `num_type` is `float`
    """
    num_type = float
    type_name = 'NumberValidator'
    type_label = 'number'
    default_error_messages = {
        'invalid': ('Not a valid number.')
    }

    def __call__(self, value):
        # Only run the validator
        # if the value is not empty ie: (None, '', [], (), {})
        if value not in constants.EMPTY_VALUES and not self.is_valid(value):
            self.fail('invalid', value=value)

    def is_valid(self, value):
        try:
            self.num_type(str(value))
            return True
        except (ValueError, TypeError):
            return False


class IntegerValidator(NumberValidator):
    """
    A integer validator.
    """
    num_type = int
    type_name = 'IntegerValidator'
    type_label = 'integer'
    default_error_messages = {
        'invalid': ('Ensure the value {value} is of type integer.')
    }


class FloatValidator(NumberValidator):
    """
    A float validator.
    """
    num_type = float
    type_name = 'FloatValidator'
    type_label = 'float'
    default_error_messages = {
        'invalid': ('Ensure the value {value} is of type float.')
    }


class UUIDValidator(BaseValidator):
    """
    A UUID validator.
    """
    type_name = 'UUIDValidator'
    type_label = 'uuid'
    default_error_messages = {
        'invalid': ('Ensure the value {value} is of type uuid.')
    }

    def __call__(self, value):
        if not self.is_valid(value):
            self.fail('invalid', value=value)

    def is_valid(self, value):
        if isinstance(value, uuid.UUID):
            return True
        try:
            uuid.UUID(str(value))
            return True
        except (ValueError, TypeError):
            return False


class DateTimeOrDateValidator(BaseValidator):
    """
    A DateTime validator.
    """
    type_name = 'DateTimeValidator'
    type_label = 'date_time'
    default_error_messages = {
        'invalid': ('Ensure the DateTime value {value} is of format {format}.')
    }
    format = constants.DATETIME_FORMAT

    def __init__(self,
                 format=None,
                 *args,
                 **kwargs):
        """
        :param format: (optional) The format of the datetime.
            Defaults to ISO_8601.
        """
        self.format = format or self.format
        super(DateTimeOrDateValidator, self).__init__(*args, **kwargs)

    def __call__(self, value):
        if not self.is_valid(value):
            self.fail(
                'invalid',
                value=value,
                format=self.format
            )

    def is_valid(self, value):
        if isinstance(value, (datetime, date)):
            return True
        try:
            datetime.strptime(value, self.format)
            return True
        except (ValueError, TypeError):
            return False
