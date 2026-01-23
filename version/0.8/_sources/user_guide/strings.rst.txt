.. _strings:

==================
Unit string format
==================

PyAnsys Units supports specifying units as strings for many input parameters and
can also provide string representations of units. The basic form of a unit
string follows this convention:

.. code::

    <multiplier prefix>[unit]<^exponent>

where

- ``multiplier prefix`` is optional and must be one of the prefixes defined on
  package initialization such as ``k``, ``M`` or ``c``.
- ``unit`` must be one of the base or derived units as defined in the
  ``UnitRegistry``.
- ``exponent`` is optional and must be preceded by the caret ``^`` symbol followed
  by the numerical exponent.

More complex unit strings can be built up by concatenation of these basic strings
with spaces in between. Spaces between the substrings indicate that the units
are multiplied together. Some examples are as follows:

.. code:: python

    accel_mps = "m s^-2.0"
    density = "kg m^-3.0"
    proportional_const = "ft s^-2.5 psi^-1.0"

You can inspect the unit tests and documentation examples to see more usage of
unit strings.