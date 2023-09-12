import ansys.units as ansunits


def test_default_units():
    ur = ansunits.UnitRegistry()
    kg = ur.kg
    assert kg.name == "kg"
    assert kg.type == "Mass"
    assert kg.factor == 1
    assert kg.offset == 0
    N = ur.N
    assert N.name == "N"
    assert N.type == "Derived"
    assert N.composition == "kg m s^-2"
    assert N.factor == 1
