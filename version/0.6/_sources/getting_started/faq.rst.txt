.. _frequently:

==========================
Frequently asked questions
==========================

What is PyAnsys Units?
""""""""""""""""""""""
PyAnsys units is a Python package that allows you to introduce the concept of
physical quantities into your Python environment. You can define your own units,
unit systems and quantities and work with them in a natural way using arithmetic
operations and conversions.

What unit systems are provided by default?
""""""""""""""""""""""""""""""""""""""""""
PyAnsys Units provides the following unit systems by default:

- `International System of Units <https://en.wikipedia.org/wiki/International_System_of_Units>`_ (SI)
- `Centimetre gram second <https://en.wikipedia.org/wiki/Centimetre–gram–second_system_of_units>`_ (CGS)
- British Technical (BT)

British technical units define the mass units as the ``slug``, length units as
``ft`` and time units of ``s``, which leads to pound-force, ``lbf``, being the
force units. You can introduce your own unit systems either dynamically at run
time or by providing a custom configuration file.

PyAnsys Units defines a unit system as a `unique selection` of base units. For
instance, the SI unit system is a unique choice of units for the default base
units.

How is PyAnsys Units different from pint?
"""""""""""""""""""""""""""""""""""""""""

In contrast to pint, the ``UnitRegistry`` is only a container of the configured
``Unit`` objects. The registry does not contain additional information. Notably
the ``UnitSystem`` is a standalone class. When creating a ``Unit`` using
``Dimensions`` it requires a unit system parameter to be passed in for non-SI
units.

Equivalent units are also handled differently. Any two ``Unit`` objects that
have the same dimensions, SI offset, and SI scaling factor are evaluated as
equal.

PyAnsys Units treats all angles as dimensional units. With this behavior the
conversion from rad/s to Hz is not allowed.