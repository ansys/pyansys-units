.. _quantity:

===================
Defining a quantity
===================

To initialize a physical quantity, import the ``ansunits`` library and create a
new ``Quantity`` object:

.. code:: python

    import ansys.units as ansunits

    meter = ansunits.Quantity(value=1, units="m")

A ``Quantity`` object can also be created with a ``Unit`` object directly or
through multiplication

.. code:: python

    import ansys.units as ansunits

    ureg = ansunits.UnitRegistry()

    meter = ansunits.Quantity(value=1, units=ureg.m)
    meter = 1 * ureg.m

With ``NumPy`` installed, a ``Quantity`` can be created using either a list of floats or a NumPy array.

.. code:: python

    import ansys.units as ansunits
    import numpy as np

    meter = ansunits.Quantity(value=[1.0, 6.0, 7.0], units="m")

    values = np.array([1.0, 6.0, 7.0])
    meter = ansunits.Quantity(value=values, units="m")

    meter[1]  # Quantity (6.0, "m")

    second = ansunits.Quantity(value=2, units="s")
    speed = meter / second
    speed  # Quantity ([0.5 3.  3.5], "m s^-1")

All ``Quantity`` objects work intuitively with arithmetic operators. Simply
insert them within an equation to perform mathematical operations.

.. code:: python


    import ansys.units as ansunits

    meter = ansunits.Quantity(value=1, units="m")

    m_ad = meter + 2  # 3
    m_sb = meter - 2  # -1
    m_ml = meter * 2  # 2
    m_dv = meter / 2  # 0.5
    m_sq = meter**2  # 1

Additions and subtraction between two ``Quantity`` objects retains the units
of the first quantity.

.. code:: python


    import ansys.units as ansunits

    meter = ansunits.Quantity(value=1, units="m")
    foot = ansunits.Quantity(value=1, units="ft")

    meter + foot  # Quantity (1.3048, "m")
    foot + meter  # Quantity (4.2808398950131235, "ft")

``Quantity`` objects work intuitively with unit conversion. The arithmetic operation
behind conversions is:

.. math::

    value_{\text{new}} = \frac{value_{\text{si}}}{f_{\text{new}}} - c_{\text{new}}


Where :math:`f_{new}` is a scaling factor and :math:`c_{new}` is an offset to convert
from SI units to the requested units.

To define a new unit system or create custom quantities, manually update the
``cfg.yaml`` file with your desired data. Once saved, these changes are reflected
throughout PyAnsys Units.