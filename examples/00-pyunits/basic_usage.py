""".. _ref_basic_usage:

PyUnits Basics
--------------
PyUnits provides a pythonic interface for units, unit systems, and unit conversions.
Its features enable seamless setup and usage of physical quantities.

**Getting Started**

The following examples cover:

- Creating quantities (unit strings, dimensions, quantity map)
- Accessing different quantity properties
- Performing arithmetic operations
- Performing unit conversions
- Creating unit systems (custom, pre-defined)
- Applying unit systems to quantities
"""

# sphinx_gallery_thumbnail_path = '_static/basic_usage.png'

###############################################################################
# Basic Usage
# -----------
#
# Units Setup
# ~~~~~~~~~~~
# Importing the pyunits library

import ansys.units as q

###############################################################################
# Creating Quantities
# ~~~~~~~~~~~~~~~~~~~
# Quantities can be instantiated with 1 of 3 methods:
#   1. Unit String : str
#   2. Dimensions : list
#   3. Quantity Map : dict

# Unit Strings

volume = q.Quantity(value=1, units="m^3")

acceleration = q.Quantity(value=3, units="m s^-2")

torque = q.Quantity(value=5, units="N m")

# Dimensions

vol_dims = [0, 3]
volume = q.Quantity(value=1, dimensions=vol_dims)

acc_dims = [0, 1, -2]
acceleration = q.Quantity(value=3, dimensions=acc_dims)

tor_dims = [1, 2, -2]
torque = q.Quantity(value=5, dimensions=tor_dims)

# Quantity Map

vol_map = {"Volume": 1}
volume = q.Quantity(value=1, quantity_map=vol_map)

acc_map = {"Acceleration": 1}
acceleration = q.Quantity(value=3, quantity_map=acc_map)

tor_map = {"Torque": 1}
torque = q.Quantity(value=5, quantity_map=tor_map)

###############################################################################
# Quantity properties
# ~~~~~~~~~~~~~~~~~~~
# Quantity objects have a total of 7 properties:
#   1. value : float | int
#   2. units : str
#   3. si_value : float | int
#   4. si_units : str
#   5. dimensions : list
#   6. is_dimensionless : bool
#   7. type : str

cap_map = {"Capacitance": 1}
capacitance = q.Quantity(value=50, quantity_map=cap_map)

capacitance.value  # >>> 50.0
capacitance.units  # >>> "farad"
capacitance.si_value  # >>> 50.0
capacitance.si_units  # >>> "kg^-1 m^-2 s^4 A^2"
capacitance.dimensions  # >>> [-1.0, -2.0, 4.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0]
capacitance.is_dimensionless  # >>> False
capacitance.type  # >>> "Derived"

###############################################################################
# Arithmetic operations
# ~~~~~~~~~~~~~~~~~~~~~
# Quantity objects support all mathematical operations.

import math

q1 = q.Quantity(10.0, "m s^-1")
q2 = q.Quantity(5.0, "m s^-1")

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

math.sin(q.Quantity(90, "degree"))  # >>> 1.0
math.cos(q.Quantity(math.pi, "radian"))  # >>> -1.0

###############################################################################
# Unit conversions
# ~~~~~~~~~~~~~~~~
# Conversions can be performed between Quantities with compatible units.

slug = q.Quantity(value=5, units="slug")
kg = slug.to("kg")

kg.value  # >>> 72.96951468603184
kg.units  # >>> "kg"

m = q.Quantity(value=25, units="m")
cm = m.to("cm")

cm.value  # >>> 2500
cm.units  # >>> "cm"

dvis = q.Quantity(1.0, "lb ft^-1 s^-1")
pas = dvis.to("Pa s")

pas.value  # >>> 1.4881639435695542
pas.units  # >>> "Pa s"

###############################################################################
# Unit systems
# ~~~~~~~~~~~~
# Unit Systems can be instantiated with 1 of 2 methods:
#   1. Custom Units
#   2. Pre-defined Unit System

# Custom Units

sys_units = ["kg", "m", "s", "K", "radian", "mol", "cd", "A", "sr"]
sys = q.UnitSystem(name="sys", base_units=sys_units)

sys.name  # >>> "sys"
sys.base_units  # >>> ["kg", "m", "s", "K", "radian", "mol", "cd", "A", "sr"]

# Pre-defined Unit Systems

cgs = q.UnitSystem(unit_sys="CGS")

cgs.name  # >>> "cgs"
cgs.base_units  # >>> ['g', 'cm', 's', 'K', 'radian', 'mol', 'cd', 'A', 'sr']

###############################################################################
# Unit systems and Quantities
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Unit Systems can be created independently and applied to desired Quantities.

si = q.UnitSystem(unit_sys="SI")
fps = q.Quantity(value=11.2, units="ft s^-1")

mps = si.convert(fps)

mps.value  # >>> 3.4137599999999995
mps.units  # >>> "m s^-1"
