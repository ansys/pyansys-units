# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
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

import pytest


@pytest.mark.developer_only
def test_pint_raises_exception_for_multiplying_relative_temperature():
    from pint import UnitRegistry
    from pint.errors import OffsetUnitCalculusError

    ur = UnitRegistry()
    with pytest.raises(OffsetUnitCalculusError):
        # this is ambiguous - relative value!
        tc = 150.0 * ur.degC
    # this is well-defined
    tk = 50.0 * ur.kelvin


@pytest.mark.developer_only
def test_pint_distinguishes_temperature_from_difference():
    from pint import Quantity, UnitRegistry
    from util import assert_wrongly

    ur = UnitRegistry()
    t1 = 150.0 * ur.kelvin
    t2 = 100.0 * ur.kelvin
    td1 = t1 - t2
    assert_wrongly(
        td1 == 50.0 * ur.kelvin, "test_pint_distinguishes_temperature_from_difference"
    )
    t1 = Quantity(1.0, ur.degC)
    t2 = Quantity(2.0, ur.degC)
    t3 = t2 - t1
    assert t3 == 1.0 * ur.delta_degree_Celsius


def test_ansunits_distinguishes_temperature_from_difference():
    from ansys.units import BaseDimensions, Dimensions, Quantity

    dims = BaseDimensions
    t1 = Quantity(150.0, "C")
    assert t1.dimensions == Dimensions({dims.TEMPERATURE: 1})
    t2 = Quantity(100.0, "C")
    assert t2.dimensions == Dimensions({dims.TEMPERATURE: 1})
    td1 = t1 - t2
    assert td1.dimensions == Dimensions({dims.TEMPERATURE_DIFFERENCE: 1})
    t3 = Quantity(1.0, "K")
    t4 = Quantity(2.0, "K")
    td2 = t4 - t3
    assert td2.dimensions == Dimensions({dims.TEMPERATURE_DIFFERENCE: 1})


# These next tests are completely debatable.
# If we start applying this, what can we do for compound units involving temperature?
# It gets too complicated.
# However, -1 K is *only* meaningful as a difference rather than an absolute value
# OTOH if you start asserting that -1 K has to be a temperature difference, you
# can run into a bunch of other issues.
def test_ansunits_automatically_creates_temperature_difference_from_negative_absolute_value():
    from ansys.units import BaseDimensions, Dimensions, Quantity, Unit

    dims = BaseDimensions

    t = Quantity(-1.0, "K")
    assert t.dimensions == Dimensions({dims.TEMPERATURE_DIFFERENCE: 1})
    assert t.units == Unit("delta_K")
    assert t.value == -1.0


# shortened from test_ansunits_automatically_creates_temperature_
# difference_from_negative_absolute_value_based_on_relative_value
# to test_ansunits_temperature_difference_from_negative_absolute_value_to_relative_value
def test_ansunits_temperature_difference_from_negative_absolute_value_to_relative_value():
    from ansys.units import BaseDimensions, Dimensions, Quantity, Unit

    dims = BaseDimensions

    t = Quantity(-274.0, "C")
    assert t.dimensions == Dimensions({dims.TEMPERATURE_DIFFERENCE: 1})
    assert t.units == Unit("delta_C")
    assert t.value == -274.0


def test_ansunits_converts_temperature_correctly():
    from ansys.units.quantity import Quantity, get_si_value

    tC = Quantity(1.0, "K").to("C")
    assert tC.value == -272.15
    assert get_si_value(tC) == 1


# This one is not debatable. This is a pure bug in ansunits code.
# We will need to do some extra work such that when type is a difference
# then the offset is zero in conversions.
def test_ansunits_converts_temperature_difference_correctly():
    from ansys.units import Quantity, Unit, get_si_value

    dK = Quantity(1.0, "K") - Quantity(2.0, "K")
    assert dK.value == -1.0
    assert dK.units == Unit("delta_K")

    tC = dK.to("delta_C")
    assert tC.value == -1.0
    assert tC.units == Unit("delta_C")
    assert get_si_value(tC) == -1.0

    dK = Quantity(2.0, "K") - Quantity(1.0, "K")
    assert dK.value == 1.0
    assert dK.units == Unit("delta_K")

    tC = dK.to("delta_C")
    assert tC.value == 1.0
    assert tC.units == Unit("delta_C")
    assert get_si_value(tC) == 1.0
