# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
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

import ansys.units as pyunits


def test_degree_addition():
    degree = pyunits.Quantity(1.0, "degree")
    assert not degree.dimensions
    assert degree.is_dimensionless
    assert degree + 1 == pyunits.Quantity(58.29577951308232, "degree")


def test_radian_addition():
    radian = pyunits.Quantity(1.0, "radian")
    assert not radian.dimensions
    assert radian.is_dimensionless
    assert radian + 1 == pyunits.Quantity(2.0, "radian")
    assert (radian + 1).to("degree") == pyunits.Quantity(114.59155902616465, "degree")


def test_unit_system_repr():
    us = pyunits.UnitSystem()
    us_dict = """MASS: kg
LENGTH: m
TIME: s
TEMPERATURE: K
TEMPERATURE_DIFFERENCE: delta_K
CHEMICAL_AMOUNT: mol
LIGHT: cd
CURRENT: A
"""

    assert repr(us) == str(us_dict)
