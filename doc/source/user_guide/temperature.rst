.. _temperature:

==================================
Temperature and temperature change
==================================

PyAnsys Units supports temperature units in Kelvin (K), Celsius (C), Rankine (R)
and Fahrenheit (F). For each temperature unit there is a change of temperature
unit which is prefixed with ``delta_``.

Conversion is handled naturally through arithmetic operations:

.. code:: python

    import ansys.units as ansunits

    ureg = ansunits.UnitRegistry()

    K = ansunits.Quantity(value=2, units=ureg.K)
    K2 = ansunits.Quantity(value=5, units=ureg.K)
    delta_K = ansunits.Quantity(value=7, units=ureg.delta_K)

    K_ad_K2 = K + K2  # (9, K)
    K2_sb_K = K2 - K  # (5, delta_K)
    K_ad_delta_K = K + delta_K  # (7, K)
    K2_sb_delta_K = K2 - delta_K  # (2, K)
    delta_K_ad_delta_K = delta_K + delta_K  # (10, delta_K)
    delta_K_sb_delta_K = delta_K - delta_K  # (0, delta_K)

Negative absolute values for any temperature are instantiated as a change in
temperature.

.. code:: python

    import ansys.units as ansunits

    ureg = ansunits.UnitRegistry()

    K = ansunits.Quantity(value=-2, units=ureg.K)  # (-2, delta_K)
    C = ansunits.Quantity(value=-2, units=ureg.C)  # (-275, delta_C)
    F = ansunits.Quantity(value=-2, units=ureg.F)  # (-500, delta_F)
    R = ansunits.Quantity(value=-2, units=ureg.R)  # (-2, delta_R)
