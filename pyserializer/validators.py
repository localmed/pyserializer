import six
import re
from encodings import idna
from decimal import Decimal

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
    'validate_email',
]


class BaseValidator(object):
    default_error_messages = {
        'invalid': 'Not valid.'
    }

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
    default_error_messages = {
        'invalid': 'Value is ruquired.'
    }

    def __call__(self, value):
        if not self.is_valid(value):
            raise ValidationError(
                self.default_error_messages['invalid']
            )

    def is_valid(self, value):
        if value in constants.EMPTY_VALUES:
            return False
        return True


class MaxValueValidator(BaseValidator):
    default_error_messages = {
        'invalid': 'Ensure this value is less than or equal to %s.'
    }

    def __init__(self, max_value):
        self.max_value = max_value

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
    default_error_messages = {
        'invalid': 'Ensure this value is greater than or equal to %s.'
    }

    def __init__(self, min_value):
        self.min_value = min_value

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
    default_error_messages = {
        'invalid': 'Ensure the value has atmost %s characters (it has %s characters).'
    }

    def __init__(self, max_lenght):
        self.max_lenght = max_lenght

    def __call__(self, value):
        value = force_str(value)
        value_lenght = len(value)
        if not self.is_valid(value_lenght):
            message = self.default_error_messages['invalid'] \
                % (self.max_lenght, value_lenght)
            raise ValidationError(message)

    def is_valid(self, value_lenght):
        return value_lenght <= self.max_lenght


class MinLengthValidator(BaseValidator):
    default_error_messages = {
        'invalid': 'Ensure the value has atlest %s characters (it has %s characters).'
    }

    def __init__(self, min_lenght):
        self.min_lenght = min_lenght

    def __call__(self, value):
        value = force_str(value)
        value_lenght = len(value)
        if not self.is_valid(value_lenght):
            message = self.default_error_messages['invalid'] \
                % (self.min_lenght, value_lenght)
            raise ValidationError(message)

    def is_valid(self, value_lenght):
        return value_lenght >= self.min_lenght


class EmailValidator(BaseValidator):

    default_error_messages = {
        'invalid': 'Not the value %s is a valid email address.'
    }
    user_regex = re.compile(r"^[\w!#$%&'*+\-/=?^`{|}~.]+$")
    domain_regex = re.compile(r'''
        ^(?:[a-z0-9][a-z0-9\-]{,62}\.)+        # subdomain
        (?:[a-z]{2,63}|xn--[a-z0-9\-]{2,59})$  # top level domain
    ''', re.I | re.VERBOSE)
    domain_blacklist = []

    def __init__(self, domain_blacklist=None):
        if domain_blacklist:
            self.domain_blacklist = domain_blacklist

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

validate_email = EmailValidator()
