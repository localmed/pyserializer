=====================
Custom Error Messages
=====================
A quick example on how to set custom error messages on fields.


Custom Error Messages on Fields
===============================
Validation error messages for fields can be configured by passing in ``error_messages`` argument to the Field's constructor::

    from pyserializer import fields

    class UserDeserializer(Serializer):
        dob = fields.DateField(
            error_messages={'invalid': 'Please provide a valid date of birth for user.'}
        )
