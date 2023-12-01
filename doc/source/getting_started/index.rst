.. _getting_started:

===============
Getting started
===============

PyAnsys Units provides a Pythonic interface for units, unit systems, and unit
conversions. On import the package is preconfigured with units and unit systems
for you to use, and is fully customizable if something you need is not present.

The package supports defining quantities and their units in a intuitive way

.. code::

   >>> from ansys.units import Quantity
   >>> foot = Quantity(value=1, units="ft")
   >>> second = Quantity(value=1, units="s")
   >>> speed = foot/second
   >>> speed
   Quantity (1.0, "ft s^-1")

and you can do the same thing with all the units provided by ``UnitRegistry``

.. code::

   >>> from ansys.units import UnitRegistry, Quantity
   >>> ur = UnitRegistry()
   >>> foot = Quantity(value=1, units=ur.ft)
   >>> second = Quantity(value=1, units=ur.s)
   >>> speed = foot/second
   >>> speed
   Quantity (1.0, "ft s^-1")

including unit conversions

.. code::

   >>> speedms = speed.to("m s^-1")
   >>> speedms
   Quantity (0.30479999999999996, "m s^-1")
   >>> speedms = speed.to(ur.m / ur.s)
   >>> speedms
   Quantity (0.30479999999999996, "m s^-1")

Finally, numpy arrays and lists can also be used with ``Quantity``

.. code::

   >>> import numpy as np
   >>> from ansys.units import UnitRegistry, Quantity
   >>> values = np.array([1.0, 6.0, 7.0])
   >>> lengths = Quantity(value=values, units=ur.m)
   >>> time = Quantity(value=2, units=ur.s)
   >>> speed = lengths/time
   >>> speed
   Quantity ([0.5 3.  3.5], "m s^-1")

.. toctree::
   :hidden:
   :maxdepth: 2

   installation
   faq
