import pytest

import ansys.units as ansunits


def test_fundamental_units():
    kg = ansunits.Unit("kg")
    assert kg.name == "kg"
    assert kg.type == "Mass"
    assert kg._factor == 1
    assert kg._offset == 0


def test_derived_units():
    N = ansunits.Unit("N")
    assert N.name == "N"
    assert N._composition == "kg m s^-2"
    assert N._factor == 1


def test_unitless():
    unit = ansunits.Unit()
    assert unit.name == ""

    assert unit.dimensions.dimensions == {}


def test_string_rep():
    C = ansunits.Unit("C")
    C_string = """_name: C
_dimensions: {'temperature': 1.0}
_type: Temperature
_factor: 1
_offset: 273.15
"""
    assert str(C) == C_string


def test_unit_multiply_by_value():
    C = ansunits.Unit("C")
    seven_C = 7 * C
    assert seven_C.value == 7
    assert seven_C.units == "C"


def test_reverse_multiply():
    ur = ansunits.UnitRegistry()
    new_unit = ur.K * ur.kg * ur.J
    assert new_unit.name == "K kg^2 m^2 s^-2"


def test_unit_div():
    K = ansunits.Unit("K")
    kg = ansunits.Unit("kg")
    kg_K = kg / K
    assert kg_K.name == "kg K^-1"


def test_unit_pow():
    kg_K = ansunits.Unit("kg K")
    kg_K_sq = kg_K**2
    assert kg_K_sq.name == "kg^2 K^2"


def test_unit_sys_list():
    dim1 = ansunits.BaseDimensions.mass
    slug = ansunits.Unit(
        dimensions=ansunits.Dimensions({dim1: 1}),
        unit_sys=ansunits.UnitSystem(
            name="sys",
            base_units=[
                "slug",
                "ft",
                "s",
                "R",
                "delta_R",
                "radian",
                "slugmol",
                "cd",
                "A",
                "sr",
            ],
        ),
    )
    assert slug.name == "slug"
    assert slug.dimensions.dimensions == {0: 1}


def test_excessive_parameters():
    with pytest.raises(ansunits.UnitError):
        C = ansunits.Unit("kg", dimensions=[1])
