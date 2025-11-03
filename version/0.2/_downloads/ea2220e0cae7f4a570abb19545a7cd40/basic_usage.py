"""
.. _ref_basic_usage:

PyAnsys Units basics
--------------------
PyAnsys Units provides a Pythonic interface for units, unit systems, and unit conversions.
Its features enable seamless setup and usage of physical quantities.

This example shows you how to perform these tasks:

- Create quantities (unit strings, dimensions, and quantity tables).
- Access different quantity properties.
- Perform arithmetic operations.
- Perform unit conversions.
- Create unit systems (custom and predefined).
- Apply unit systems to quantities.
"""

# sphinx_gallery_thumbnail_path = '_static/basic_usage.png'

###############################################################################
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Import the ``ansys.units`` package.

from ansys.units import BaseDimensions, Dimensions, Quantity, UnitSystem
from ansys.units.quantity import get_si_value

###############################################################################
# Create quantities
# ~~~~~~~~~~~~~~~~~
# You can instantiate quantities using one of three methods:
# - Unit strings : str, Unit
# - Dimensions : Dimensions
# - Quantity table : dict

# Unit strings

volume = Quantity(value=1, units="m^3")

acceleration = Quantity(value=3, units="m s^-2")

torque = Quantity(value=5, units="N m")

# Dimensions

dims = BaseDimensions

vol_dims = Dimensions({dims.LENGTH: 3})
volume = Quantity(value=1, dimensions=vol_dims)

acc_dims = Dimensions({dims.LENGTH: 1, dims.TIME: -2})
acceleration = Quantity(value=3, dimensions=acc_dims)

tor_dims = Dimensions({dims.MASS: 1, dims.LENGTH: 2, dims.TIME: -2})
torque = Quantity(value=5, dimensions=tor_dims)

# Quantity table

vol_dict = {"Volume": 1}
volume = Quantity(value=1, quantity_table=vol_dict)

acc_dict = {"Acceleration": 1}
acceleration = Quantity(value=3, quantity_table=acc_dict)

tor_dict = {"Torque": 1}
torque = Quantity(value=5, quantity_table=tor_dict)

###############################################################################
# Specify quantity properties
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# For a quantity, you specify seven properties:

# 1. value : float | int
# 2. units : str
# 3. si_value : float | int
# 4. si_units : str
# 5. dimensions : dict
# 6. is_dimensionless : bool


cap_dict = {"Capacitance": 1}
capacitance = Quantity(value=50, quantity_table=cap_dict)

capacitance.value  # >>> 50.0
capacitance.units.name  # >>> "farad"
capacitance.units.si_units  # >>> "kg^-1 m^-2 s^4 A^2"
capacitance.dimensions  # >>> {'MASS': -1.0, 'LENGTH': -2.0, 'TIME': 4.0, 'CURRENT': 2.0}
capacitance.is_dimensionless  # >>> False
get_si_value(capacitance)  # >>> 50.0

###############################################################################
# Perform arithmetic operations
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# You can perform all mathematical operations on a quantity.

import math

q1 = Quantity(10.0, "m s^-1")
q2 = Quantity(5.0, "m s^-1")

# Subtraction

q3 = q2 - q1
q3.value  # >>> 5.0
q3.units.name  # >>> "m s^-1"

# Addition

q4 = q2 + q1
q4.value  # >>> 15.0
q4.units.name  # >>> "m s^-1"

# Division

q5 = q2 / q1
q5.value  # >>> 2.0
q5.units.name  # >>> None

# Multiplication

q6 = q2 * q1
q6.value  # >>> 50.0
q6.units.name  # >>> "m^2 s^-2"

# Negation

q7 = -q2
q7.value  # >>> -5.0
q7.units.name  # >>> "m s^-1"

# Exponents

q8 = q1**2
q8.value  # >>> 100.0
q8.units.name  # >>> "m^2 s^-2"

# Roots

q9 = Quantity(5.0, "")

math.sqrt(q9)  # >>> 2.2360679775

# Trigonometry

math.sin(Quantity(90, "degree"))  # >>> 1.0
math.cos(Quantity(math.pi, "radian"))  # >>> -1.0

###############################################################################
# Perform conversions
# ~~~~~~~~~~~~~~~~~~~
# To check the compatible units use the 'compatible_units' method.

slug = Quantity(value=5, units="slug")
slug.compatible_units()  # >>> {'lbm', 'g', 'lb', 'kg'}

# You can perform conversions on quantities with compatible units.

kg = slug.to("kg")

kg.value  # >>> 72.96951468603184
kg.units.name  # >>> "kg"

m = Quantity(value=25, units="m")
cm = m.to("cm")

cm.value  # >>> 2500
cm.units.name  # >>> "cm"

dvis = Quantity(1.0, "lb ft^-1 s^-1")
pas = dvis.to("Pa s")

pas.value  # >>> 1.4881639435695542
pas.units.name  # >>> "Pa s"

###############################################################################
# Instantiate unit systems
# ~~~~~~~~~~~~~~~~~~~~~~~~
# You can instantiate unit systems using a few methods:
#
# - Custom units
# - Predefined unit systems
# - Copy from a preexisting unit system
# - Combinations of these

# Custom units

dims = BaseDimensions
sys_units = {dims.MASS: "slug", dims.LENGTH: "ft"}
sys = UnitSystem(base_units=sys_units, system="SI")
sys
"""
MASS: slug
LENGTH: ft
TIME: s
TEMPERATURE: K
TEMPERATURE_DIFFERENCE: delta_K
ANGLE: radian
CHEMICAL_AMOUNT: mol
LIGHT: cd
CURRENT: A
SOLID_ANGLE: sr
"""

# Predefined unit systems

cgs = UnitSystem(system="CGS")
cgs
"""
MASS: g
LENGTH: cm
TIME: s
TEMPERATURE: K
TEMPERATURE_DIFFERENCE: delta_K
ANGLE: radian
CHEMICAL_AMOUNT: mol
LIGHT: cd
CURRENT: A
SOLID_ANGLE: sr
"""


# Copy from a preexisting unit system

cgs_copy = UnitSystem(copy_from=cgs)
cgs_copy
"""
MASS: g
LENGTH: cm
TIME: s
TEMPERATURE: K
TEMPERATURE_DIFFERENCE: delta_K
ANGLE: radian
CHEMICAL_AMOUNT: mol
LIGHT: cd
CURRENT: A
SOLID_ANGLE: sr
"""


# Combinations of these

sys_units = {dims.MASS: "slug", dims.LENGTH: "ft", dims.ANGLE: "degree"}
cgs_modified = UnitSystem(base_units=sys_units, copy_from=cgs)
cgs_modified
"""
MASS: slug
LENGTH: ft
TIME: s
TEMPERATURE: K
TEMPERATURE_DIFFERENCE: delta_K
ANGLE: degree
CHEMICAL_AMOUNT: mol
LIGHT: cd
CURRENT: A
SOLID_ANGLE: sr
"""


###############################################################################
# Create a unit system independently
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# You can create a unit system independently and apply it to quantities.

si = UnitSystem()
feet_per_second = Quantity(value=11.2, units="ft s^-1")

meters_per_second = feet_per_second.convert(si)

meters_per_second.value  # >>> 3.4137599999999995
meters_per_second.units  # >>> "m s^-1"


###############################################################################
# Using preferred units
# ~~~~~~~~~~~~~~~~~~~~~
# Specify a list of units that quantities will automatically convert to.

Quantity.preferred_units(units=["J"])

torque = Quantity(1, quantity_table={"Torque": 1})
torque  # >>> Quantity (1.0, "J")

ten_N = Quantity(10, units="N")
ten_m = Quantity(10, units="m")

joules = ten_N * ten_m
joules  # >>> Quantity (100.0, "J")
