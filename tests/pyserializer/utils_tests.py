from nose.tools import *
from mock import *

from pyserializer.utils import *


class TestUtil(object):

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
