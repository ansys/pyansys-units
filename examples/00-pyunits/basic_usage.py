"""
.. _ref_basic_usage:

PyAnsys Units basics
--------------------
PyAnsys Units provides a Pythonic interface for units, unit systems, and unit conversions.
Its features enable seamless setup and usage of physical quantities.

This example shows you how to perform these tasks:

- Create quantities (unit strings, dimensions, and quantity maps).
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

import ansys.units as ansunits

###############################################################################
# Create quantities
# ~~~~~~~~~~~~~~~~~
# You can instantiate quantities using one of three methods:
# - Unit strings : str, Unit
# - Dimensions : Dimensions
# - Quantity maps : dict

# Unit strings

volume = ansunits.Quantity(value=1, units="m^3")

acceleration = ansunits.Quantity(value=3, units="m s^-2")

torque = ansunits.Quantity(value=5, units="N m")

# Dimensions

dims = ansunits.BaseDimensions

vol_dims = ansunits.Dimensions({dims.LENGTH: 3})
volume = ansunits.Quantity(value=1, dimensions=vol_dims)

acc_dims = ansunits.Dimensions({dims.LENGTH: 1, dims.TIME: -2})
acceleration = ansunits.Quantity(value=3, dimensions=acc_dims)

tor_dims = ansunits.Dimensions({dims.MASS: 1, dims.LENGTH: 2, dims.TIME: -2})
torque = ansunits.Quantity(value=5, dimensions=tor_dims)

# Quantity map

vol_map = {"Volume": 1}
volume = ansunits.Quantity(value=1, quantity_map=vol_map)

acc_map = {"Acceleration": 1}
acceleration = ansunits.Quantity(value=3, quantity_map=acc_map)

tor_map = {"Torque": 1}
torque = ansunits.Quantity(value=5, quantity_map=tor_map)

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


cap_map = {"Capacitance": 1}
capacitance = ansunits.Quantity(value=50, quantity_map=cap_map)

capacitance.value  # >>> 50.0
capacitance.units  # >>> "kg^-1 m^-2 s^4 A^2"
capacitance.si_value  # >>> 50.0
capacitance.si_units  # >>> "kg^-1 m^-2 s^4 A^2"
capacitance.dimensions  # >>> {'MASS': -1.0, 'LENGTH': -2.0, 'TIME': 4.0, 'CURRENT': 2.0}
capacitance.is_dimensionless  # >>> False

###############################################################################
# Perform arithmetic operations
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# You can perform all mathematical operations on a quantity.

import math

q1 = ansunits.Quantity(10.0, "m s^-1")
q2 = ansunits.Quantity(5.0, "m s^-1")

# Subtraction

q3 = q2 - q1
q3.value  # >>> 5.0
q3.units  # >>> "m s^-1"

# Addition

q4 = q2 + q1
q4.value  # >>> 15.0
q4.units  # >>> "m s^-1"

# Division

q5 = q2 / q1
q5.value  # >>> 2.0
q5.units  # >>> None

# Multiplication

q6 = q2 * q1
q6.value  # >>> 50.0
q6.units  # >>> "m^2 s^-2"

# Negation

q7 = -q2
q7.value  # >>> -5.0
q7.units  # >>> "m s^-1"

# Exponents

q8 = q1**2
q8.value  # >>> 100.0
q8.units  # >>> "m^2 s^-2"

# Roots

math.sqrt(q2)  # >>> 2.2360679775

# Trigonometry

math.sin(ansunits.Quantity(90, "degree"))  # >>> 1.0
math.cos(ansunits.Quantity(math.pi, "radian"))  # >>> -1.0

###############################################################################
# Perform conversions
# ~~~~~~~~~~~~~~~~~~~
# You can perform conversions on quantities with compatible units.

slug = ansunits.Quantity(value=5, units="slug")
kg = slug.to("kg")

kg.value  # >>> 72.96951468603184
kg.units  # >>> "kg"

m = ansunits.Quantity(value=25, units="m")
cm = m.to("cm")

cm.value  # >>> 2500
cm.units  # >>> "cm"

dvis = ansunits.Quantity(1.0, "lb ft^-1 s^-1")
pas = dvis.to("Pa s")

pas.value  # >>> 1.4881639435695542
pas.units  # >>> "Pa s"

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

dims = ansunits.BaseDimensions
sys_units = {dims.MASS: "slug", dims.LENGTH: "ft"}
sys = ansunits.UnitSystem(base_units=sys_units, unit_sys="SI")

sys.base_units  # >>> ["slug", "ft", "s", "K", "delta_K", "radian", "mol", "cd", "A", "sr"]

# Predefined unit systems

cgs = ansunits.UnitSystem(unit_sys="CGS")

cgs.base_units  # >>> ['g', 'cm', 's', 'K', "delta_K", 'radian', 'mol', 'cd', 'A', 'sr']

# Copy from a preexisting unit system

cgs2 = ansunits.UnitSystem(copy_from=cgs)

cgs2.base_units  # >>> ['g', 'cm', 's', 'K', "delta_K", 'radian', 'mol', 'cd', 'A', 'sr']

# Combinations of these

sys_units = {dims.MASS: "slug", dims.LENGTH: "ft", dims.ANGLE: "degree"}
cgs_modified = ansunits.UnitSystem(base_units=sys_units, copy_from=cgs)

cgs_modified.base_units  # >>> ['slug', 'ft', 's', 'K', "delta_K", 'degree', 'mol', 'cd', 'A', 'sr']


###############################################################################
# Create a unit system independently
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# You can create a unit system independently and apply it to quantities.

si = ansunits.UnitSystem()
fps = ansunits.Quantity(value=11.2, units="ft s^-1")

mps = si.convert(fps)

mps.value  # >>> 3.4137599999999995
mps.units  # >>> "m s^-1"
