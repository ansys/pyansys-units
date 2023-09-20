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


def test_string_rep():
    C = ansunits.Unit("C")
    C_string = """_name: C
_dimensions: [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
_type: Temperature
_factor: 1
_offset: 273.15
"""
    assert C.__str__() == C_string


def test_unit_multiply_by_value():
    C = ansunits.Unit("C")
    seven_C = 7 * C
    assert seven_C.value == 7
    assert seven_C.units == "C"


def test_reverse_multiply():
    ur = ansunits.UnitRegistry()
    new_unit = ur.K * ur.kg * ur.J
    assert new_unit.name == "kg^2 m^2 s^-2 K"
