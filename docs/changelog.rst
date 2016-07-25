=========
Changelog
=========

Changes in v0.5.0
=================
- Add ability to set ``allow_blank_source`` on serializer class. If this is set to ``True`` the serializer class will not throw error if source is not available.

Changes in v0.4.1
=================
- Fix bug where nested serialization where caching data.

Changes in v0.4.0
=================
- Add support for ``MethodField``

Changes in v0.3.1
=================
- Fixes bug with defining source with dot syntax

Changes in v0.3.0
=================
- Add support for ``FloatField``
- Add support for ``DecimalField``
- Add support for ``DictField``
- Add support for ``UrlField``
- Add support for ``BooleanField``
- Add support for ``RawField``


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
