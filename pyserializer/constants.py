# Default datetime input and output formats


ISO_8601 = 'iso-8601'

DATETIME_FORMAT = ISO_8601

DATE_FORMAT = ISO_8601

EMPTY_VALUES = (None, '', [], (), {})

MISSING_ERROR_MESSAGE = (
    'ValidationError raised by `{class_name}`, but error key `{key}` does '
    'not exist in the `error_messages` dict.'
)
