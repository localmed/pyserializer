import six
import re
from encodings import idna
from decimal import Decimal
from collections import OrderedDict
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
        self.message = kwargs.pop(
            'message',
            self.default_error_messages['invalid']
        )
        self.error_dict = OrderedDict([
            ('type_name', kwargs.pop('type_name', self.type_name)),
            ('type_label', kwargs.pop('type_label', self.type_label)),
            ('message', self.message)
        ])

    def __call__(self, value):
        if not self.is_valid(value):
            raise ValidationError(
                self.default_error_messages['invalid']
            )

    def is_valid(self, value):
        raise NotImplementedError(
            '`is_valid` should be implemented by the child class.'
        )


class RequiredValidator(BaseValidator):
    """
    A required field validator.
    """
    type_name = 'RequiredValidator'
    type_label = 'required'
    default_error_messages = {
        'invalid': 'Value is required.'
    }

    def __call__(self,
                 value):
        if not self.is_valid(value):
            raise ValidationError(
                self.default_error_messages['invalid']
            )

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
        'invalid': 'Ensure this value is less than or equal to %s.'
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
        if not self.is_valid(value):
            raise ValidationError(
                self.default_error_messages['invalid'] % self.max_value
            )

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
        'invalid': 'Ensure this value is greater than or equal to %s.'
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
        if not self.is_valid(value):
            raise ValidationError(
                self.default_error_messages['invalid'] % self.min_value
            )

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
        'invalid': ('Ensure the value has atmost %s characters'
                    '(it has %s characters).')
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
        value = force_str(value)
        value_length = len(value)
        if not self.is_valid(value_length):
            message = self.default_error_messages['invalid'] \
                % (self.max_length, value_length)
            raise ValidationError(message)

    def is_valid(self, value_length):
        return value_length <= self.max_length


class MinLengthValidator(BaseValidator):
    """
    A min length validator.
    """
    type_name = 'MinLengthValidator'
    type_label = 'min_length'
    default_error_messages = {
        'invalid': ('Ensure the value has atlest %s characters'
                    '(it has %s characters).')
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
        value = force_str(value)
        value_length = len(value)
        if not self.is_valid(value_length):
            message = self.default_error_messages['invalid'] \
                % (self.min_length, value_length)
            raise ValidationError(message)

    def is_valid(self, value_length):
        return value_length >= self.min_length


class EmailValidator(BaseValidator):
    """
    A email validator.
    """
    type_name = 'EmailValidator'
    type_label = 'email'
    default_error_messages = {
        'invalid': '%s is an invalid email address.'
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
        value = force_str(value)
        if not self.is_valid(value):
            message = self.default_error_messages['invalid'] \
                % (value)
            raise ValidationError(message)

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
