import ansys.units as pyunits


def test_fundamental_units():
    kg = pyunits.Unit("kg")
    assert kg.name == "kg"
    assert kg.type == "Mass"
    assert kg.factor == 1
    assert kg.offset == 0


def test_derived_units():
    N = pyunits.Unit("N")
    assert N.name == "N"
    assert N.composition == "kg m s^-2"
    assert N.factor == 1


def test_string_rep():
    C = pyunits.Unit("C")
    C_string = """name: C
type: Temperature
factor: 1
offset: 273.15
dimensions: [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
"""
    assert C.__str__() == C_string
