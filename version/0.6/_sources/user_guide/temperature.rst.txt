.. _temperature:

======================================
Temperature and temperature difference
======================================

PyAnsys Units supports temperature units in kelvin (K), celsius (C), rankine (R)
and fahrenheit (F).

For each temperature unit, there is a corresponding temperature difference unit
which is prefixed with ``delta_``. In order to add two temperature-based quantities,
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
difference.

.. code:: python

    from ansys.units import Quantity, UnitRegistry

    ureg = UnitRegistry()

    K = Quantity(value=-2, units=ureg.K)  # (-2, delta_K)
    C = Quantity(value=-2, units=ureg.C)  # (-275, delta_C)
    F = Quantity(value=-2, units=ureg.F)  # (-500, delta_F)
    R = Quantity(value=-2, units=ureg.R)  # (-2, delta_R)

