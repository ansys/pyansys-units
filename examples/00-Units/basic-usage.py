""".._ref_basic_usage:

Getting Started
---------------
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
- Setting up custom units
"""

# sphyinx_gallery_thumbnail_path = ''

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
# Accessing different quantity properties
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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

capacitance.value
# >>> 50.0

capacitance.units
# >>> "farad"

capacitance.si_value
# >>> 50.0

capacitance.si_units
# >>> "kg^-1 m^-2 s^4 A^2"

capacitance.dimensions
# >>> [-1.0, -2.0, 4.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0]

capacitance.is_dimensionless
# >>> False

capacitance.type
# >>> "Derived"

###############################################################################
# Performing arithmetic operations
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Quantity objects support all types of mathematical operation.


###############################################################################
# Performing unit conversions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
#

###############################################################################
# Creating unit systems
# ~~~~~~~~~~~~~~~~~~~~~
#

###############################################################################
# Applying unit systems to quantities
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

###############################################################################
# Setting up custom units
# ~~~~~~~~~~~~~~~~~~~~~~~
#
