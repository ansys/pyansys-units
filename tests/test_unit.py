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
    assert C.__str__() == "name: C\ntype: Temperature\nfactor: 1\noffset: 273.15\n"
