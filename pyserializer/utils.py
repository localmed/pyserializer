import inspect
import six
import collections


__all__ = [
    'is_simple_callable',
    'is_iterable',
    'force_str',
    'get_object_by_source',
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


def get_object_by_source(obj, source):
    """
    Tries to get the object by source.
    Similar to Python's `getattr(obj, source)`, but takes a dot separaed
    string for source to get source from nested obj, instead of a single
    source field. Also, supports getting source form obj where obj is a
    dict type.

    Example:
        >>> obj = get_object_by_source(
            object, source='user.username')
    """
    if isinstance(obj, collections.Mapping):
        if '.' in source:
            for source in source.split('.'):
                obj = obj.get(source)
        else:
            obj = obj.get(source)
    else:
        if '.' in source:
            for source in source.split('.'):
                obj = getattr(obj, source)
        else:
            obj = getattr(obj, source)
    return obj
