.. _temperature:

======================================
Temperature and temperature difference
======================================

PyAnsys Units supports temperature units in kelvin (K), celsius (C), rankine (R)
and fahrenheit (F).

For each temperature unit, there is a corresponding temperature difference unit
which is prefixed with ``delta_``. To add two temperature-based quantities,
at least one must be a temperature difference. If one temperature is subtracted
from another, the result is a temperature difference.

.. code:: python

    from ansys.units import Quantity, UnitRegistry

    ureg = UnitRegistry()

    K = Quantity(value=280, units=ureg.K)
    K2 = Quantity(value=295, units=ureg.K)
    delta_K = Quantity(value=5, units=ureg.delta_K)

    K2_sb_K = K2 - K  # (15.0, "delta_K")
    K_ad_delta_K = K + delta_K  # (285.0, "K")
    K2_sb_delta_K = K2 - delta_K  # (290.0, "K")
    delta_K_ad_delta_K = delta_K + delta_K  # (10.0, "delta_K")
    delta_K_sb_delta_K = delta_K - delta_K  # (0.0, "delta_K")

Any temperature values below absolute zero are instantiated as temperature
difference. For arrays, the lowest value decides.

.. code:: python

    from ansys.units import Quantity, UnitRegistry

    ureg = UnitRegistry()

    K = Quantity(value=-2, units=ureg.K)  # (-2.0, "delta_K")
    C = Quantity(value=-300, units=ureg.C)  # (-300.0, "delta_C")
    F = Quantity(value=-500, units=ureg.F)  # (-500.0, "delta_F")
    R = Quantity(value=-2, units=ureg.R)  # (-2.0, "delta_R")
    C2 = Quantity(value=-2, units=ureg.C)  # (-2.0, "C"), above absolute zero

The lower limit comes from each unit's conversion offset rather than its name, so
it also applies to custom temperature units. You can query it directly:

.. code:: python

    from ansys.units import Unit

    Unit("C").min_absolute_value  # -273.15
    Unit("C").is_absolute_temperature  # True
    Unit("C").to_temperature_difference()  # Unit("delta_C")

Offset units
------------

The celsius (C) and fahrenheit (F) units are *offset* units: their zero point
differs from absolute zero, so scaling a value in these units has no physical
meaning. Kelvin (K), rankine (R), and all temperature difference units are
multiplicative.

Multiplying, dividing, or raising an absolute temperature in C or F to a power
raises a ``ProhibitedOffsetUnitOperation`` error. Convert to K or R, or use a
temperature difference, instead:

.. code:: python

    from ansys.units import Quantity

    t = Quantity(20, "C")

    t * 2  # raises ProhibitedOffsetUnitOperation
    t**2  # raises ProhibitedOffsetUnitOperation

    t.to("K") * 2  # Quantity (586.3, "K")
    Quantity(5, "delta_C") * 2  # Quantity (10.0, "delta_C")

    t + Quantity(5, "delta_C")  # Quantity (25.0, "C")
    t - Quantity(5, "C")  # Quantity (15.0, "delta_C")

``Unit("C").has_offset`` reports whether a unit is an offset unit.

Offset units inside compound units, such as ``W m^-1 C^-1``, are interpreted as
temperature differences. These compound units convert without an offset and
support all arithmetic. If unit arithmetic cancels such a compound unit down to a
single temperature term, the result is a temperature difference unit:

.. code:: python

    from ansys.units import Quantity, Unit

    conductivity = Quantity(2.0, "W m^-1 C^-1")
    conductivity * Quantity(3.0, "m")  # Quantity (6.0, "W C^-1")
    conductivity.to("W m^-1 K^-1")  # Quantity (2.0, "W m^-1 K^-1")

    Unit("C^2") ** 0.5  # Unit("delta_C")

Multiplier prefixes, such as ``kC`` or ``mF``, can't be combined with offset units
and raise a ``PrefixedOffsetUnit`` error.
