# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
.. _ref_unit_aliases:

Unit aliases
------------
PyAnsys Units supports unit aliases so you can use shorthand or
alternative names for units.  For example, ``deg`` for ``degree`` or
``meter`` for ``m``.

This example shows you how to:

- Use built-in aliases in unit and quantity creation.
- Use aliases inside compound unit strings.
- Register custom aliases programmatically.
- Perform conversions with aliased units.
"""

###############################################################################
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
from ansys.units import Quantity, Unit, UnitRegistry

###############################################################################
# Built-in aliases
# ~~~~~~~~~~~~~~~~
# Several common aliases are shipped out of the box. Use ``deg`` instead
# of ``degree``, ``rad`` instead of ``radian``, ``meter`` instead of ``m``,
# and so on.

angle = Unit("deg")
print(f"Unit('deg')  ->  name={angle.name!r}, sf={angle.si_scaling_factor}")

length = Unit("meter")
print(f"Unit('meter') ->  name={length.name!r}")

force = Unit("newton")
print(f"Unit('newton') ->  name={force.name!r}")

###############################################################################
# Aliases in quantities
# ~~~~~~~~~~~~~~~~~~~~~
# Aliases work seamlessly when creating ``Quantity`` objects.

q_angle = Quantity(90, "deg")
print(f"Quantity(90, 'deg')  = {q_angle}")

q_len = Quantity(5.0, "meter")
print(f"Quantity(5.0, 'meter') = {q_len}")

###############################################################################
# Aliases in compound units
# ~~~~~~~~~~~~~~~~~~~~~~~~~
# Aliases can be mixed with canonical names inside compound unit strings.

angular_velocity = Unit("deg sec^-1")
print(f"Unit('deg sec^-1') ->  name={angular_velocity.name!r}")

acceleration = Unit("meter sec^-2")
print(f"Unit('meter sec^-2') -> name={acceleration.name!r}")

###############################################################################
# Conversions with aliases
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Unit conversions work normally when aliases are used.

q_deg = Quantity(180, "deg")
q_rad = q_deg.to("radian")
print(f"180 deg = {q_rad.value:.6f} radian")

q_m = Quantity(1, "meter")
q_ft = q_m.to("ft")
print(f"1 meter = {q_ft.value:.6f} ft")

###############################################################################
# Register a custom alias
# ~~~~~~~~~~~~~~~~~~~~~~~
# You can register your own aliases at runtime via ``UnitRegistry``.

ureg = UnitRegistry()
ureg.register_alias("angular_deg", "degree")

custom = Unit("angular_deg")
print(f"Unit('angular_deg') -> name={custom.name!r}")

###############################################################################
# Alias equality
# ~~~~~~~~~~~~~~
# A unit created from an alias is fully equal to the canonical unit.

assert Unit("deg") == Unit("degree")
assert Unit("rad") == Unit("radian")
assert Unit("meter") == Unit("m")
print("All alias-based units equal their canonical counterparts.")
