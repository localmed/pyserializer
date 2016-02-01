from nose.tools import *  # flake8: noqa
from mock import *  # flake8: noqa

from pyserializer.exceptions import ValidationError
from pyserializer import validators


class TestRequiredValidator(object):

    @raises(ValidationError)
    def test_required_validator_raises(self):
        value = None
        validator = validators.RequiredValidator()
        validator(value)

    def test_valid_required_validator(self):
        value = 'Some Value'
        validator = validators.RequiredValidator()
        assert_equal(validator(value), None)


class TestMaxValueValidator(object):

    @raises(ValidationError)
    def test_max_value_validator_raises(self):
        value = 100
        validator = validators.MaxValueValidator(max_value=100)
        validator(value)

    def test_valid_max_value_validator(self):
        value = 20
        validator = validators.MaxValueValidator(max_value=50)
        assert_equal(validator(value), None)

    @raises(ValidationError)
    def test_max_value_validator_with_decimals_raises(self):
        value = 20.22
        validator = validators.MaxValueValidator(max_value=20.21)
        validator(value)


class TestMinValueValidator(object):

    @raises(ValidationError)
    def test_min_value_validator_raises(self):
        value = 20
        validator = validators.MinValueValidator(min_value=50)
        validator(value)

    def test_valid_min_value_validator(self):
        value = 50
        validator = validators.MinValueValidator(min_value=50)
        assert_equal(validator(value), None)

    @raises(ValidationError)
    def test_min_value_validator_with_decimals_raises(self):
        value = 19.33
        validator = validators.MinValueValidator(min_value=20.21)
        validator(value)


class TestMaxLenghtValidator(object):

    @raises(ValidationError)
    def test_max_lenght_validator_raises(self):
        value = 'abcabc'
        validator = validators.MaxLengthValidator(max_lenght=5)
        validator(value)

    def test_valid_max_lenght_validator(self):
        value = 'abc'
        validator = validators.MaxLengthValidator(max_lenght=5)
        assert_equal(validator(value), None)


class TestMinLenghtValidator(object):

    @raises(ValidationError)
    def test_min_lenght_validator_raises(self):
        value = 'a'
        validator = validators.MinLengthValidator(min_lenght=5)
        validator(value)

    def test_valid_min_lenght_validator(self):
        value = 'abc'
        validator = validators.MinLengthValidator(min_lenght=3)
        assert_equal(validator(value), None)


class TestEmailValidator(object):

    @raises(ValidationError)
    def test_email_with_blacklist_domain_raises(self):
        value = 'unknown@example.org'
        validator = validators.EmailValidator(
            domain_blacklist=['example.org']
        )
        validator(value)

    @raises(ValidationError)
    def test_email_with_spaces_raises(self):
        value = 'unknown @example.org'
        validator = validators.EmailValidator()
        validator(value)

    @raises(ValidationError)
    def test_invalid_email_raises(self):
        value = 'foo.com'
        validator = validators.EmailValidator()
        validator(value)

    def test_valid_email_validator(self):
        value = 'bob@gmail.com'
        validator = validators.EmailValidator()
        assert_equal(validator(value), None)
