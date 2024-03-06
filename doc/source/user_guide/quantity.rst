.. _quantity:

===================
Defining a quantity
===================

Import ``Quantity`` from the ``ansys.units`` package and instantiate a
``Quantity`` object, providing a numerical value and a unit string:

.. code:: python

    from ansys.units import Quantity

    meter = Quantity(value=1, units="m")

You can also provide a ``Unit`` object (rather than a unit string) as a
construction argument. Alternatively, you can instantiate a ``Quantity``
object by multiplying a ``Unit`` object by a value:

.. code:: python

    from ansys.units import Quantity, UnitRegistry

    ureg = UnitRegistry()

    meter = Quantity(value=1, units=ureg.m)
    meter = 1 * ureg.m

With ``NumPy`` installed, you can instantiate a ``Quantity`` using either
a list of floats or a ``NumPy`` array:

.. code:: python

    from ansys.units import Quantity
    import numpy as np

    length_array_quantity = Quantity(value=[1.0, 6.0, 7.0], units="m")
    length_array_quantity[1]  # Quantity (6.0, "m")
    time = Quantity(value=2, units="s")
    speed = length_array_quantity / time
    speed  # Quantity ([0.5 3. 3.5], "m s^-1")

All ``Quantity`` objects work intuitively with arithmetic operators:

.. code:: python


    from ansys.units import Quantity

    meter = Quantity(value=1, units="m")

    m_ml = meter * 2  # (2.0, "m")
    m_dv = meter / 2  # (0.5, "m")
    m_sq = meter**2  # (1.0, "m^2")

Additions and subtractions involving ``Quantity`` objects retain the units
of the first operand:

.. code:: python


    from ansys.units import Quantity

    meter = Quantity(value=1, units="m")
    foot = Quantity(value=1, units="ft")

    meter + foot  # Quantity (1.3048, "m")
    foot + meter  # Quantity (4.2808398950131235, "ft")

This formula defines the conversion of ``Quantity`` objects between different units:

.. math::

    value_{\text{new}} = \frac{value_{\text{si}}}{f_{\text{new}}} - c_{\text{new}}

where :math:`f_{new}` is a scaling factor and :math:`c_{new}` is an offset to convert
from SI units to the requested units.

To define a new unit system or create custom quantities, you can manually update the
``cfg.yaml`` file with your desired settings. Once saved, these changes are reflected
the next time the ``ansys.units`` package is initialized.
