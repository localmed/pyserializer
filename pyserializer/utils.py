import inspect
import six


__all__ = [
    'is_simple_callable',
    'is_iterable',
    'force_str',
]


def is_simple_callable(obj):
    '''
    True if the object is a callable and takes no arguments, else False.
    '''
    function = inspect.isfunction(obj)
    method = inspect.ismethod(obj)
    if not (function or method):
        return False
    args, varargs, keywords, defaults = inspect.getargspec(obj)
    len_args = len(args) if function else len(args) - 1
    len_defaults = len(defaults) if defaults else 0
    return len_args <= len_defaults


def is_iterable(obj):
    '''
    True if an object is iterable, else False
    '''
    return hasattr(obj, '__iter__')


def force_str(value, encoding='utf-8'):
    """
    Forces the value to a str instance, decoding if necessary.
    """
    if six.PY3:
        if isinstance(value, bytes):
            return str(value, encoding)
    return value
