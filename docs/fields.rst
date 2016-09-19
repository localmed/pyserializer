======
Fields
======
Each field in a Serializer/Deserializer class is responsible for validating and cleaning the data. You can add additional validators to the field class to further enhanse the field validation.

.. note:: The serializer fields are defined in ``fields.py``. You can import them using ``from pyserializer import fields``, and refer to the fields as ``fields.<FieldName>``.


Currently supported serializer fields
=====================================
CharField:
----------
A text representation. Signature: ``CharField(source=None, label=None, help_text=None, validators=None)``

:attr:`source` (Default: None)
    The source name for the field. You can use dot syntax to specify nested source. Eg: ``version.name``.

:attr:`label` (Default: None)
    The label for the field.

:attr:`help_text` (Default: None)
    The readable help text for the field.

:attr:`validators` (Default: None)
    List of validators that should be ran when deserializing the field.

    .. note:: The validators are defined in ``validators.py``. You can import them using ``from pyserializer import validators``, and refer to the fields as ``validators.<ValidatorName>``.

    Some commonly used validators with ``CharField`` are:

    * ``RequiredValidator``: Signature: ``RequiredValidator()``. Raise a ``ValidationError`` if the field value is not supplied during deserialization.

    * ``MaxLengthValidator``: Signature: ``MaxLengthValidator(max_length)``. Raise a ``ValidationError`` if the field value exceeds the max lenght character limit during deserialization.

        :attr:`max_length`
            The maximum lenght in integer.

    * ``MinLengthValidator``: Signature: ``MinLengthValidator(min_length)``. Raise a ``ValidationError`` if the field value does not have atlest min lenght characters during deserialization.

        :attr:`min_length`
            The minimum lenght in integer.


DateField:
----------
A date representation. The default format is ``%Y-%m-%d``. Validates the input to match the specified format. Signature: ``DateField(source=None, label=None, help_text=None, validators=None, format='%Y-%m-%d')``

:attr:`format` (Default: '%Y-%m-%d')
    A string representing the input or output format.


DateTimeField:
--------------
A datetime representation. The default format is ``'iso-8601'``. Validates the input to match the specified format. Signature: ``DateTimeField(source=None, label=None, help_text=None, validators=None, format='iso-8601')``

:attr:`format` (Default: 'iso-8601')
    A string representing the input or output format.


UUIDField:
----------
A field that ensures the input is a valid UUID string. Signature: ``UUIDField(source=None, label=None, help_text=None, validators=None)``

.. _number-field:

NumberField:
------------
An float representation. Signature: ``NumberField(source=None, label=None, help_text=None, validators=None)``

:attr:`validators` (Default: None)
    List of validators that should be ran when deserializing the field.
    Some commonly used validators with ``NumberField`` are:

    * ``RequiredValidator``: Signature: ``RequiredValidator()``. Raise a ``ValidationError`` if the field value is not supplied during deserialization.

    * ``MaxValueValidator``: Signature: ``MaxValueValidator(max_value)``. Raise a ``ValidationError`` if the field value exceeds the max value during deserialization.

        :attr:`max_value`
            The maximum value in integer.

    * ``MinValueValidator``: Signature: ``MinValueValidator(min_value)``. Raise a ``ValidationError`` if the field value is less than the min value during deserialization.

        :attr:`min_value`
            The minimum value in integer.


IntegerField:
-------------
An integer representation. Signature: ``IntegerField(source=None, label=None, help_text=None, validators=None)``

:attr:`validators` (Default: None)
    List of validators that should be ran when deserializing the field.
    Some commonly used validators with ``IntegerField`` are are inline with ``NumberField`` validators. See :ref:`number-field`.


FloatField:
-----------
An integer representation. Signature: ``FloatField(source=None, label=None, help_text=None, validators=None)``

:attr:`validators` (Default: None)
    List of validators that should be ran when deserializing the field.
    Some commonly used validators with ``IntegerField`` are are inline with ``NumberField`` validators. See :ref:`number-field`.


DictField:
----------
An python dictionary representation. Signature: ``DictField(source=None, label=None, help_text=None, validators=None)``


BooleanField:
-------------
An boolean representation. Signature: ``BooleanField(source=None, label=None, help_text=None, validators=None)``


RawField:
---------
A field that does not perform any valudation. Signature: ``RawField(source=None, label=None, help_text=None, validators=None)``


UrlField:
---------
A field that validates the input against a URL matching pattern. Signature: ``UrlField(source=None, label=None, help_text=None, validators=None)``


EmailField:
-----------
A field that validates the input to be a valid e-mail address. Signature: ``EmailField(source=None, label=None, help_text=None, validators=None)``


MethodField:
------------
This that gets its value by calling a method on the serializer class it is attached to. It can be used to add any sort of data to the serialized representation of your object. Signature: ``MethodField(method_name=None, source=None, label=None, help_text=None, validators=None)``

:attr:`method_name` (Default: None)
    The name of the serialize method defined in serializer.

See :doc:`apireference` for complete documentation on the fields.
