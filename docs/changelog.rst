=========
Changelog
=========

Changes in v0.2.1
=================
- Fix Field errors are not caught during the validation and stored in error object, but are raised when accessing the object
- Updated documentation for Create Custom Validators
- Updated documentation for Create Custom Fields


Changes in v0.2.0
=================
- Hooked in the field validators with the serializer
- Added ``is_valid()`` method on the ``Serializer`` class
- Added ``errors`` property on the ``Serializer`` class
- Added documentations for the above
