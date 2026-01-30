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

import pytest

from ansys.units import (
    BaseDimensions,
    Dimensions,
    Quantity,
    Unit,
    UnitRegistry,
    UnitSystem,
)
from ansys.units.quantity import get_si_value
from ansys.units.unit import (
    InconsistentDimensions,
    IncorrectUnits,
    ProhibitedTemperatureOperation,
    UnconfiguredUnit,
    UnknownTableItem,
)


def test_base_units():
    dims = BaseDimensions
    kg = Unit("kg")
    assert kg.name == "kg"
    assert kg.dimensions == Dimensions({dims.MASS: 1})
    assert kg.si_scaling_factor == 1
    assert kg.si_offset == 0


def test_equal_dimensions_not_equal_units():
    l = Unit("l")
    kl = Unit("kl")
    m_cubed = Unit("m^3")

    assert m_cubed == kl
    assert l != m_cubed


def test_derived_units():
    N = Unit("N")
    assert N.name == "N"
    assert N.si_units == "kg m s^-2"
    assert N.si_scaling_factor == 1


def test_multiple_multipliers():
    ten_meter = Unit("kcm")
    dam = Unit("dam")

    assert ten_meter == dam


def test_unitless():
    u_1 = Unit()
    u_2 = Unit("m^0")

    assert u_1.name == ""
    assert u_1.dimensions == Dimensions()

    assert u_2.name == ""
    assert u_2.dimensions == Dimensions()


def test_copy():
    ureg = UnitRegistry()
    kg = Unit(copy_from=ureg.kg)
    ft = Unit(copy_from=ureg.ft)
    slug = Unit(copy_from=ureg.slug)
    assert kg == ureg.kg
    assert ft == ureg.ft
    assert slug == ureg.slug


def test_compatibility():
    ureg = UnitRegistry()
    length_units = {"cm", "in", "m", "inch"}
    force_units = {"dyne", "lbf", "pdl"}
    temperature_difference_units = {"delta_C", "delta_R", "delta_F"}

    assert ureg.ft.compatible_units() == length_units
    assert ureg.N.compatible_units() == force_units
    assert ureg.delta_K.compatible_units() == temperature_difference_units


def test_units_from_dimensions():
    dims = BaseDimensions
    kg = Unit(dimensions=Dimensions({dims.MASS: 1}))
    assert kg.name == "kg"
    assert kg.dimensions == Dimensions({dims.MASS: 1})
    assert kg.si_scaling_factor == 1
    assert kg.si_offset == 0
    slug_squared = Unit(
        dimensions=Dimensions({dims.MASS: 2}),
        system=UnitSystem(system="BT"),
    )
    assert slug_squared.name == "slug^2"
    assert slug_squared.dimensions == Dimensions({dims.MASS: 2})
    assert slug_squared.si_scaling_factor == 212.9820029406007
    assert slug_squared.si_offset == 0


def test_string_rep():
    C = Unit("C")
    C_string = """_name: C
_dimensions: {'TEMPERATURE': 1.0}
_type: TEMPERATURE
_si_scaling_factor: 1.0
_si_offset: 273.15
_si_units: K
"""
    assert C._to_string() == C_string


def test_add():
    C = Unit("C")
    delta_C = Unit("delta_C")
    kg = Unit("kg")
    temp_C, delta_temp = C + delta_C

    assert delta_temp == Unit("delta_C")
    assert temp_C == Unit("C")
    assert kg + kg is None

    with pytest.raises(ProhibitedTemperatureOperation):
        C + C

    with pytest.raises(IncorrectUnits):
        C + kg


def test_quantity_table():
    qm1 = Unit(
        table={
            "Mass": 1,
            "Velocity": 2.5,
            "Current": 3,
            "Light": 1,
            "HeatTransferCoefficient": 2,
        }
    )
    assert qm1.name == "kg m^-1.5 s^-2.5 A^3 cd W^2 K^-2"


def test_unit_multiply_by_quantity():
    q = Quantity(7, "kg")
    C = Unit("C")

    assert C.__mul__(q) == NotImplemented


def test_reverse_multiply():
    ur = UnitRegistry()
    new_unit = ur.K * ur.kg * ur.J
    assert new_unit.name == "K kg J"


def test_rmul():
    assert 7 * Unit("kg") == Quantity(7, "kg")


def test_sub():
    C = Unit("C")
    kg = Unit("kg")
    delta_C, C = C - C

    assert C == Unit("C")
    assert delta_C == Unit("delta_C")
    assert kg - kg is None

    with pytest.raises(IncorrectUnits):
        C - kg


def test_unit_divide_by_quantity():
    q = Quantity(7, "kg")
    C = Unit("C")

    assert C.__truediv__(q) is NotImplemented  # type: ignore


def test_unit_div():
    K = Unit("K")
    kg = Unit("kg")
    kg_K = kg / K
    assert kg_K.name == "kg K^-1"


def test_rtruediv():
    K = Unit("K")
    kg = Unit("kg")
    kg_K = kg / K
    assert kg_K.name == "kg K^-1"

    assert 1 / K == Quantity(1, "K^-1")


def test_unit_pow():
    kg_K = Unit("kg K")
    kg_K_sq = kg_K**2
    assert kg_K_sq.name == "kg^2 K^2"


def test_eq():
    kg = Unit("kg")
    unitless = Unit()
    assert kg == kg
    assert 7 == unitless


def test_ne():
    kg = Unit("kg")
    assert 7 != kg


def test_excessive_parameters_not_allowed():
    dims = BaseDimensions
    with pytest.raises(InconsistentDimensions):
        Unit("kg", dimensions=Dimensions({dims.LENGTH: 1}))


def test_incorrect_unit_with_multiplier():
    with pytest.raises(UnconfiguredUnit):
        Unit("kbeans")


def test_copy_units_with_incompatable_dimensions():
    kg = Unit("kg")
    with pytest.raises(InconsistentDimensions):
        Unit(units="m", copy_from=kg)


def test_unconfigured_units():
    with pytest.raises(UnconfiguredUnit):
        Quantity(value=1, units="k")

        Quantity(value=1, units="kg m^2 k")


def test_errors():
    with pytest.raises(UnknownTableItem):
        Unit(
            table={
                "Bread": 2,
                "Chicken": 1,
                "Eggs": 7,
                "Milk": -4,
            }  # pyright: ignore[reportArgumentType]
        )


def test_error_messages():
    e1 = UnknownTableItem("Risk")
    assert str(e1) == "`Risk` is not a valid quantity table item."


def test_tonne_feet_unit():
    foot = Quantity(value=1, units="ft")
    assert get_si_value(foot) == 0.30479999999999996

    tonne = Quantity(value=1, units="tonne")
    assert get_si_value(tonne) == 1000.0

    femto_tonne = Quantity(value=1, units="ftonne")
    assert get_si_value(femto_tonne) == 1e-12
