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

import re

import pytest

from ansys.units import (
    BaseDimensions,
    Dimensions,
    Quantity,
    Unit,
    UnitRegistry,
    UnitSystem,
)
from ansys.units._constants import _base_units
from ansys.units.quantity import get_si_value
from ansys.units.unit import (
    InconsistentDimensions,
    IncorrectUnits,
    PrefixedOffsetUnit,
    ProhibitedOffsetUnitOperation,
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

    inch = Unit("in")
    assert inch.name == "in"
    assert inch.dimensions == Dimensions({dims.LENGTH: 1})
    assert inch.si_scaling_factor == 0.0254
    assert inch.si_offset == 0

    minute = Unit("min")
    assert minute.name == "min"
    assert minute.dimensions == Dimensions({dims.TIME: 1})
    assert minute.si_scaling_factor == 60
    assert minute.si_offset == 0


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

    bar = Unit("bar")
    assert bar.name == "bar"
    assert bar.si_units == "kg m^-1 s^-2"
    assert bar.dimensions == Dimensions(
        {BaseDimensions.MASS: 1, BaseDimensions.LENGTH: -1, BaseDimensions.TIME: -2}
    )
    assert bar.si_scaling_factor == 100000
    assert bar.si_offset == 0


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


@pytest.mark.parametrize(
    "name, minimum, delta",
    [
        ("K", 0.0, "delta_K"),
        ("R", 0.0, "delta_R"),
        ("C", -273.15, "delta_C"),
        ("F", -459.67, "delta_F"),
    ],
)
def test_absolute_temperature_metadata(name: str, minimum: float, delta: str):
    unit = Unit(name)
    assert unit.is_absolute_temperature
    assert unit.min_absolute_value == minimum
    assert unit.to_temperature_difference().name == delta


def test_non_absolute_temperature_metadata():
    for name in ("m", "delta_C", "K s^-1"):
        unit = Unit(name)
        assert not unit.is_absolute_temperature
        assert unit.min_absolute_value is None
    with pytest.raises(ValueError):
        Unit("delta_C").to_temperature_difference()


def test_to_temperature_difference_falls_back_to_matching_scaling_factor(
    monkeypatch: pytest.MonkeyPatch,
):
    # A temperature unit without a ``delta_<name>`` counterpart resolves to a
    # configured difference unit with the same scaling factor.
    monkeypatch.setitem(
        _base_units,
        "testtemp",
        {"type": "TEMPERATURE", "si_scaling_factor": 1, "si_offset": 10.0},
    )
    unit = Unit("testtemp")
    assert unit.min_absolute_value == -10.0
    delta = unit.to_temperature_difference()
    assert delta.dimensions == Dimensions({BaseDimensions.TEMPERATURE_DIFFERENCE: 1})
    assert delta.si_scaling_factor == 1

    q = Quantity(-20.0, "testtemp")
    assert q.units == delta


def test_to_temperature_difference_without_counterpart(
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setitem(
        _base_units,
        "testtemp",
        {"type": "TEMPERATURE", "si_scaling_factor": 0.8, "si_offset": 1.0},
    )
    with pytest.raises(ValueError, match="No temperature difference unit"):
        Unit("testtemp").to_temperature_difference()


@pytest.mark.parametrize(
    "name, expected",
    [
        ("C", True),
        ("F", True),
        ("K", False),
        ("R", False),
        ("kelvin", False),
        ("delta_C", False),
        ("delta_F", False),
        ("m s^-1", False),
        ("", False),
        # Offset units in compound units are temperature differences.
        ("C^2", False),
        ("kg C", False),
        ("W m^-1 C^-1", False),
    ],
)
def test_has_offset(name: str, expected: bool):
    assert Unit(name).has_offset is expected


def test_compound_units_with_offset_terms_are_multiplicative():
    conductivity = Quantity(2.0, "W m^-1 C^-1")
    assert (conductivity * 2).value == 4.0
    assert (conductivity * Quantity(3.0, "m")).units == Unit("W C^-1")
    assert conductivity.to("W m^-1 K^-1").value == 2.0
    assert Quantity(9.0, "F^-1").to("R^-1").value == pytest.approx(9.0)


def test_arithmetic_never_produces_an_absolute_offset_unit():
    # Cancelling down to a bare offset unit yields the temperature difference.
    assert (Unit("C^2") ** 0.5).name == "delta_C"
    assert (Unit("C m") / Unit("m")).name == "delta_C"
    assert (Unit("F m^-1") * Unit("m")).name == "delta_F"
    assert (Quantity(4.0, "C^2") ** 0.5).units == Unit("delta_C")


@pytest.mark.parametrize("name", ["kC", "mF", "kg kC", "uC^-1"])
def test_prefixed_offset_units_are_rejected(name: str):
    with pytest.raises(PrefixedOffsetUnit, match="multiplier prefix"):
        Unit(name)
    with pytest.raises(PrefixedOffsetUnit):
        Quantity(1.0, name)


def test_prefixed_difference_and_ratio_units_are_allowed():
    assert Unit("kK").si_scaling_factor == 1000
    assert Unit("mdelta_C").si_scaling_factor == pytest.approx(0.001)


def test_offset_unit_arithmetic_is_prohibited():
    C, m = Unit("C"), Unit("m")
    for operation, op in (
        (lambda: C * m, "*"),
        (lambda: m * C, "*"),
        (lambda: C / m, "/"),
        (lambda: m / C, "/"),
        (lambda: C**2, "**"),
        (lambda: Unit("F") ** -1, "**"),
    ):
        with pytest.raises(ProhibitedOffsetUnitOperation, match=re.escape(f"'{op}'")):
            operation()

    # Constructing a quantity from a value and an offset unit is still allowed.
    assert 5 * C == Quantity(5, "C")


def test_ratio_scale_and_difference_units_allow_arithmetic():
    assert Unit("K") * Unit("m") == Unit("K m")
    assert Unit("R") / Unit("s") == Unit("R s^-1")
    assert Unit("K") ** 2 == Unit("K^2")
    assert Unit("delta_C") / Unit("m") == Unit("delta_C m^-1")


def test_prohibited_offset_unit_operation_error():
    error = ProhibitedOffsetUnitOperation(Unit("C"), "*")
    assert isinstance(error, TypeError)
    assert "'C'" in str(error) and "'*'" in str(error)


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


def test_units_from_dimensions_with_preferred_units():
    dims = BaseDimensions
    mm_tonne_second = UnitSystem(
        base_units={
            dims.MASS: "tonne",
            dims.LENGTH: "mm",
            dims.TIME: "s",
        }
    )
    pressure_dims = Dimensions({dims.MASS: 1, dims.LENGTH: -1, dims.TIME: -2})

    expanded = Unit(dimensions=pressure_dims, system=mm_tonne_second)
    assert expanded.name == "tonne mm^-1 s^-2"

    simplified = Unit(
        dimensions=pressure_dims,
        system=mm_tonne_second,
        preferred_units=["MPa"],
    )
    assert simplified.name == "MPa"


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
    assert [1, 2, 3] * Unit("m") == Quantity([1, 2, 3], "m")
    assert [1, 2, 3] * Unit("m") * (Quantity(4, "Hz")) == Quantity([4, 8, 12], "m s^-1")


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

    assert C.__truediv__(q) is NotImplemented


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


def test_unit_repr():
    assert repr(Unit("kg m^-3")) == "Unit('kg m^-3')"


def test_unsupported_reflected_operands():
    with pytest.raises(TypeError):
        object() * Unit("m")
    with pytest.raises(TypeError):
        object() / Unit("m")


def test_dimensionless_unit_arithmetic_names():
    assert (Unit("") / Unit("")).name == ""
    assert (Unit("m") / Unit("")).name == "m"
    assert (Unit("") ** 2).name == ""
    assert (6 / Quantity(2.0, "")).units.name == ""


def test_dim_to_units_defaults_to_si():
    from ansys.units.unit import _dim_to_units

    dims = Dimensions({BaseDimensions.LENGTH: 1, BaseDimensions.TIME: -1})
    assert _dim_to_units(system=None, dimensions=dims) == "m s^-1"
