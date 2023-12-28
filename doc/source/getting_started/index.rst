.. _getting_started:

===============
Getting started
===============

PyAnsys Units provides a Pythonic interface for units, unit systems, and unit
conversions. Once imported the package is initialized with units and unit
systems for you to use, and is fully customizable if something you need is not
present.

Basic usage
-----------
PyAnsys Units supports defining quantities and their units in a intuitive way.
Start by importing the ``ansys.units`` package:

.. code:: python

   from ansys.units import Quantity, UnitRegistry, BaseDimensions, Dimensions

You can instantiate quantities with one of four methods:

.. code:: python

   # Using supported unit strings

   volume = Quantity(value=1, units="m^3")

   volume.value  # 1.0
   volume.units.name  # "m^3"

   # Using Unit instances

   ureg = UnitRegistry()

   mass = Quantity(value=1, units=ureg.kg)

   volume.value  # 1.0
   volume.units.name  # "kg"

   # Using base dimensions

   dims = BaseDimensions
   dimensions = Dimensions({dims.LENGTH: 1, dims.TIME: -2})

   acceleration = Quantity(value=3, dimensions=dimensions)

   acceleration.value  # 3.0
   acceleration.units.name  # "m s^-2"

   # Using the quantity table

   torque = Quantity(5, quantity_table={"Torque": 1})

   torque.value  # 5.0
   torque.units.name  # "N m"
   torque.units.si_units  # "kg m^2 s^-2"

You can instantiate unit systems with one of two methods:

.. code:: python

   # Use a pre-defined unit system

   si = UnitSystem(system="SI")

   si.base_units  # ['kg', 'm', 's', 'K', 'delta_K', 'radian', 'mol', 'cd', 'A', 'sr']

   # Custom unit systems are defined by passing selected base units. Any unit
   # type that is not given defaults to SI.

   dims = BaseDimensions

   sys = UnitSystem(
       base_units={
           dims.MASS: ureg.slug,
           dims.LENGTH: ureg.ft,
           dims.TEMPERATURE: ureg.R,
           dims.TEMPERATURE_DIFFERENCE: ureg.delta_R,
           dims.CHEMICAL_AMOUNT: ureg.slugmol,
       }
   )

   sys.base_units  # ['slug', 'ft', 's', 'R', 'delta_R', 'radian', 'slugmol', 'cd', 'A', 'sr']

Examples
--------

Perform arithmetic operations:

.. code:: python

   from ansys.units import Quantity

   deg = Quantity(90, "degree")
   math.sin(deg)  # 1.0

   v1 = Quantity(10.0, "m s^-1")
   v2 = Quantity(5.0, "m s^-1")

   v3 = v1 - v2
   v3.value  # 5.0

   vpow = v1**2
   vpow.value  # 100.0
   vpow.units  # "m^2 s^-2"

Directly convert values to another set of units:

.. code:: python

   from ansys.units import Quantity

   flbs = Quantity(1, "lb ft^-1 s^-1")
   flbs.value  # 1

   pas = flbs.to("Pa s")
   pas.value  # 1.4881639435695542
   pas.units.name  # 'Pa s'

Use a custom unit system to perform conversions:

.. code:: python

   from ansys.units import Quantity, BaseDimensions, UnitSystem

   dims = BaseDimensions

   sys = UnitSystem(
       base_units={
           dims.MASS: ureg.slug,
           dims.LENGTH: ureg.ft,
           dims.TEMPERATURE: ureg.R,
           dims.TEMPERATURE_DIFFERENCE: ureg.delta_R,
           dims.CHEMICAL_AMOUNT: ureg.slugmol,
       }
   )

   v = Quantity(10, "kg m s^2")
   v2 = v.convert(sys)

   v2.value  # 2.2480894309971045
   v2.units.name  # 'slug ft s^2'

.. toctree::
   :hidden:
   :maxdepth: 2

   installation
   faq
