from nose.tools import *  # flake8: noqa
from mock import *  # flake8: noqa

from pyserializer.utils import *  # flake8: noqa


class TestUtil:

    def test_is_simple_callable_with_function(self):
        def foo():
            pass
        output = is_simple_callable(foo)
        assert_true(output)

    def test_is_simple_callable_with_function_and_args(self):
        def foo(name):
            pass
        output = is_simple_callable(foo)
        assert_false(output)

    def test_is_simple_callable_with_method(self):
        class Foo(object):
            def __init__(self, *args, **kwargs):
                pass
        output = is_simple_callable(Foo())
        assert_false(output)

    def test_is_iterable_true(self):
        output = is_iterable([])
        assert_true(output)

    def test_is_terable_false(self):
        output = is_iterable(1)
        assert_false(output)

    def test_force_str(self):
        output = force_str(b'some_value')
        assert_equal(output, 'some_value')

    def test_force_str_with_str(self):
        output = force_str('some_value')
        assert_equal(output, 'some_value')

    def test_get_object_by_source(self):
        user = Mock(name='user', username='foo.bar.com')
        output = get_object_by_source(
            user,
            source='username'
        )
        assert_equal(output, 'foo.bar.com')

    def test_get_object_by_source_with_dot_syntax(self):
        user = Mock(name='user', username='foo.bar.com')
        comment = Mock(name='comment', user=user)
        output = get_object_by_source(
            comment,
            source='user.username'
        )
        assert_equal(output, 'foo.bar.com')
