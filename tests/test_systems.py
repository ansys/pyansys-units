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

import os

os.environ["PYANSYS_UNITS_ANGLE_AS_DIMENSION"] = "1"

import pytest

from ansys.units import BaseDimensions, UnitRegistry, UnitSystem
from ansys.units.systems import IncorrectUnitType, InvalidUnitSystem, NotBaseUnit


def test_pre_defined_unit_system():
    us = UnitSystem(system="SI")
    assert us.MASS == "kg"
    assert us.LENGTH == "m"
    assert us.TIME == "s"
    assert us.TEMPERATURE == "K"
    assert us.TEMPERATURE_DIFFERENCE == "delta_K"
    assert us.ANGLE == "radian"
    assert us.CHEMICAL_AMOUNT == "mol"
    assert us.LIGHT == "cd"
    assert us.CURRENT == "A"
    assert us.SOLID_ANGLE == "sr"


def test_repr():
    us = UnitSystem()
    us_dict = """MASS: kg
LENGTH: m
TIME: s
TEMPERATURE: K
TEMPERATURE_DIFFERENCE: delta_K
CHEMICAL_AMOUNT: mol
LIGHT: cd
CURRENT: A
ANGLE: radian
SOLID_ANGLE: sr
"""

    assert repr(us) == str(us_dict)


def test_copy():
    us = UnitSystem(system="BT")
    us1 = UnitSystem(copy_from=us)
    assert us1 == us


def test_update():
    ureg = UnitRegistry()
    dims = BaseDimensions
    us = UnitSystem(system="SI")
    base_units = {
        dims.MASS: ureg.slug,
        dims.LENGTH: ureg.ft,
        dims.TIME: "s",
        dims.TEMPERATURE: "R",
        dims.TEMPERATURE_DIFFERENCE: "delta_R",
        dims.ANGLE: "degree",
        dims.CHEMICAL_AMOUNT: ureg.slugmol,
        dims.LIGHT: "cd",
        dims.CURRENT: "A",
        dims.SOLID_ANGLE: "sr",
    }
    us.update(base_units=base_units)
    assert us.MASS.name == "slug"
    assert us.LENGTH.name == "ft"
    assert us.TIME == "s"
    assert us.TEMPERATURE == "R"
    assert us.TEMPERATURE_DIFFERENCE == "delta_R"
    assert us.ANGLE == "degree"
    assert us.CHEMICAL_AMOUNT.name == "slugmol"
    assert us.LIGHT == "cd"
    assert us.CURRENT == "A"
    assert us.SOLID_ANGLE == "sr"


def test_eq():
    us1 = UnitSystem(system="BT")
    us2 = UnitSystem()
    us3 = UnitSystem(system="SI")
    assert (us1 == us2) == False
    assert us2 == us3


def test_set_type():
    ureg = UnitRegistry()
    us = UnitSystem(system="SI")
    us.MASS = ureg.slug
    us.LENGTH = "ft"
    us.TEMPERATURE = "R"
    us.TEMPERATURE_DIFFERENCE = ureg.delta_R
    us.ANGLE = "degree"
    us.CHEMICAL_AMOUNT = "slugmol"
    assert us.MASS.name == "slug"
    assert us.LENGTH == "ft"
    assert us.TEMPERATURE == "R"
    assert us.TEMPERATURE_DIFFERENCE.name == "delta_R"
    assert us.ANGLE == "degree"
    assert us.CHEMICAL_AMOUNT == "slugmol"


def test_custom_unit_system():
    dims = BaseDimensions
    us = UnitSystem(
        base_units={
            dims.MASS: "slug",
            dims.LENGTH: "ft",
            dims.TIME: "s",
            dims.TEMPERATURE: "R",
            dims.TEMPERATURE_DIFFERENCE: "delta_R",
            dims.ANGLE: "radian",
            dims.CHEMICAL_AMOUNT: "slugmol",
            dims.LIGHT: "cd",
            dims.CURRENT: "A",
            dims.SOLID_ANGLE: "sr",
        }
    )
    assert us.MASS == "slug"
    assert us.LENGTH == "ft"
    assert us.TIME == "s"
    assert us.TEMPERATURE == "R"
    assert us.TEMPERATURE_DIFFERENCE == "delta_R"
    assert us.ANGLE == "radian"
    assert us.CHEMICAL_AMOUNT == "slugmol"
    assert us.LIGHT == "cd"
    assert us.CURRENT == "A"
    assert us.SOLID_ANGLE == "sr"


def test_not_base_unit_init():
    dims = BaseDimensions

    with pytest.raises(NotBaseUnit):
        us1 = UnitSystem(base_units={dims.LENGTH: "N"})


def test_not_base_unit_update():
    dims = BaseDimensions
    us = UnitSystem(system="SI")
    base_units = {dims.MASS: "N"}

    with pytest.raises(NotBaseUnit):
        us.update(base_units=base_units)


def test_invalid_unit_sys():
    with pytest.raises(InvalidUnitSystem):
        us2 = UnitSystem(system="Standard")


def test_wrong_unit_type():
    us = UnitSystem()

    with pytest.raises(IncorrectUnitType):
        us.TIME = "m"
    with pytest.raises(IncorrectUnitType):
        us.LIGHT = "sr"
    with pytest.raises(IncorrectUnitType):
        us.CURRENT = "ft"
    with pytest.raises(IncorrectUnitType):
        us.SOLID_ANGLE = "radian"


def test_error_messages():
    e1 = NotBaseUnit("kg s^-1")
    expected_str = (
        "`kg s^-1` is not a base unit. To use `kg s^-1`, add it to the "
        "`base_units` table within the cfg.yaml file."
    )
    assert str(e1) == expected_str

    e2 = InvalidUnitSystem("ham sandwich")
    assert str(e2) == "`ham sandwich` is not a supported unit system."

    e3 = IncorrectUnitType(unit="ft", unit_type=BaseDimensions.MASS)
    assert str(e3) == "The unit `ft` is incompatible with unit system type: `MASS`"
