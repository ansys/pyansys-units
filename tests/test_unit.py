import pytest

import ansys.units as ansunits
from ansys.units.unit import (
    InconsistentDimensions,
    IncorrectTemperatureUnits,
    IncorrectUnits,
    UnconfiguredUnit,
)


def test_base_units():
    dims = ansunits.BaseDimensions
    kg = ansunits.Unit("kg")
    assert kg.name == "kg"
    assert kg.dimensions == ansunits.Dimensions({dims.MASS: 1})
    assert kg.si_scaling_factor == 1
    assert kg.si_offset == 0


def test_derived_units():
    N = ansunits.Unit("N")
    assert N.name == "N"
    assert N.si_units == "kg m s^-2"
    assert N.si_scaling_factor == 1


def test_multiple_multipliers():
    ten_meter = ansunits.Unit("kcm")
    dam = ansunits.Unit("dam")

    assert ten_meter == dam


def test_unitless():
    u_1 = ansunits.Unit()
    u_2 = ansunits.Unit("m^0")

    assert u_1.name == ""
    assert u_1.dimensions == ansunits.Dimensions()

    assert u_2.name == ""
    assert u_2.dimensions == ansunits.Dimensions()


def test_copy():
    ureg = ansunits.UnitRegistry()
    kg = ansunits.Unit(copy_from=ureg.kg)
    ft = ansunits.Unit(copy_from=ureg.ft)
    slug = ansunits.Unit(copy_from=ureg.slug)
    assert kg == ureg.kg
    assert ft == ureg.ft
    assert slug == ureg.slug


def test_units_from_dimensions():
    dims = ansunits.BaseDimensions
    kg = ansunits.Unit(dimensions=ansunits.Dimensions({dims.MASS: 1}))
    assert kg.name == "kg"
    assert kg.dimensions == ansunits.Dimensions({dims.MASS: 1})
    assert kg.si_scaling_factor == 1
    assert kg.si_offset == 0
    slug_squared = ansunits.Unit(
        dimensions=ansunits.Dimensions({dims.MASS: 2}),
        system=ansunits.UnitSystem(system="BT"),
    )
    assert slug_squared.name == "slug^2"
    assert slug_squared.dimensions == ansunits.Dimensions({dims.MASS: 2})
    assert slug_squared.si_scaling_factor == 212.9820029406007
    assert slug_squared.si_offset == 0


def test_string_rep():
    C = ansunits.Unit("C")
    C_string = """_name: C
_dimensions: {'TEMPERATURE': 1.0}
_type: TEMPERATURE
_si_scaling_factor: 1.0
_si_offset: 273.15
_si_units: K
"""
    assert str(C) == C_string
    assert str(C) == repr(C)


def test_add():
    C = ansunits.Unit("C")
    delta_C = ansunits.Unit("delta_C")
    kg = ansunits.Unit("kg")
    temp_C = C + delta_C

    assert temp_C == ansunits.Unit("C")
    assert kg + kg == None

    with pytest.raises(IncorrectUnits):
        C + kg

    with pytest.raises(IncorrectTemperatureUnits):
        C + C


def test_unit_multiply_by_value():
    C = ansunits.Unit("C")
    seven_C = 7 * C

    assert seven_C.value == 7
    assert seven_C.units == ansunits.Unit("C")


def test_unit_multiply_by_quantity():
    q = ansunits.Quantity(7, "kg")
    C = ansunits.Unit("C")

    assert C.__mul__(q) == NotImplemented


def test_reverse_multiply():
    ur = ansunits.UnitRegistry()
    new_unit = ur.K * ur.kg * ur.J
    assert new_unit.name == "K kg J"


def test_sub():
    C = ansunits.Unit("C")
    kg = ansunits.Unit("kg")
    delta_C = C - C

    assert delta_C == ansunits.Unit("delta_C")
    assert kg - kg == None

    with pytest.raises(IncorrectUnits):
        C - kg


def test_unit_divide_by_quantity():
    q = ansunits.Quantity(7, "kg")
    C = ansunits.Unit("C")

    assert C.__truediv__(q) == NotImplemented


def test_unit_div():
    K = ansunits.Unit("K")
    kg = ansunits.Unit("kg")
    kg_K = kg / K
    assert kg_K.name == "kg K^-1"


def test_unit_pow():
    kg_K = ansunits.Unit("kg K")
    kg_K_sq = kg_K**2
    assert kg_K_sq.name == "kg^2 K^2"


def test_eq():
    kg = ansunits.Unit("kg")
    unitless = ansunits.Unit()
    assert kg == kg
    assert 7 == unitless


def test_ne():
    kg = ansunits.Unit("kg")
    assert 7 != kg


def test_excessive_parameters_not_allowed():
    dims = ansunits.BaseDimensions
    with pytest.raises(InconsistentDimensions):
        C = ansunits.Unit("kg", dimensions=ansunits.Dimensions({dims.LENGTH: 1}))


def test_incorrect_unit_with_multiplier():
    with pytest.raises(UnconfiguredUnit):
        ansunits.Unit("kbeans")


def test_copy_units_with_incompatable_dimensions():
    kg = ansunits.Unit("kg")
    with pytest.raises(InconsistentDimensions):
        ansunits.Unit(units="m", copy_from=kg)
