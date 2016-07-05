__all__ = [
    'ValidationError',
    'MethodMissingError',
]


class ValidationError(Exception):
    pass


class MethodMissingError(Exception):
    pass
