import pytest

import ansys.units as pyunits


def test_tables():
    assert isinstance(pyunits._api_quantity_map, dict)
    assert isinstance(pyunits._fundamental_units, dict)
    assert isinstance(pyunits._derived_units, dict)
    assert isinstance(pyunits._multipliers, dict)
    assert isinstance(pyunits._unit_systems, dict)
    assert isinstance(pyunits._dimension_order, dict)


def test_has_multiplier():
    ut = pyunits.Units()

    assert ut._has_multiplier("km")
    assert ut._has_multiplier("ms")
    assert ut._has_multiplier("dam")

    assert not ut._has_multiplier("kg")
    assert not ut._has_multiplier("cm")
    assert not ut._has_multiplier("m")


def test_si_map():
    ut = pyunits.Units()

    assert ut._si_map("g") == "kg"
    assert ut._si_map("lbm") == "kg"
    assert ut._si_map("ft") == "m"
    assert ut._si_map("slugmol") == "mol"
    assert ut._si_map("degree") == "radian"


def test_filter_unit_term():
    ut = pyunits.Units()

    assert ut.filter_unit_term("cm^-2") == ("", "cm", -2)
    assert ut.filter_unit_term("m") == ("", "m", 1)
    assert ut.filter_unit_term("K^4") == ("", "K", 4)
    assert ut.filter_unit_term("dam") == ("da", "m", 1)
    assert ut.filter_unit_term("mm") == ("m", "m", 1)


def test_si_data():
    ut = pyunits.Units()

    u1, m1, o1 = ut.si_data(units="g")
    assert u1 == "kg"
    assert m1 == 0.001
    assert o1 == 0

    u2, m2, o2 = ut.si_data(units="lb")
    assert u2 == "kg"
    assert m2 == 0.45359237
    assert o2 == 0

    u3, m3, o3 = ut.si_data(units="ft^2")
    assert u3 == "m^2"
    assert m3 == 0.09290303999999998
    assert o3 == 0

    u4, m4, o4 = ut.si_data(units="F")
    assert u4 == "K"
    assert m4 == 0.55555555555
    assert o4 == 459.67

    u5, m5, o5 = ut.si_data(units="farad")
    assert u5 == "kg^-1 m^-2 s^4 A^2"
    assert m5 == 1
    assert o5 == 0


def test_condense():
    ut = pyunits.Units()

    assert ut.condense("m m m m") == "m^4"
    assert ut.condense("kg ft^3 kg^-2") == "kg^-1 ft^3"
    assert ut.condense("s^2 s^-2") == ""


def test_get_type():
    ut = pyunits.Units()

    assert ut.get_type(units="kg") == "Mass"
    assert ut.get_type(units="m") == "Length"
    assert ut.get_type(units="s") == "Time"
    assert ut.get_type(units="K") == "Temperature"
    assert ut.get_type(units="delta_K") == "Temperature Difference"
    assert ut.get_type(units="radian") == "Angle"
    assert ut.get_type(units="mol") == "Chemical Amount"
    assert ut.get_type(units="cd") == "Light"
    assert ut.get_type(units="A") == "Current"
    assert ut.get_type(units="sr") == "Solid Angle"
    assert ut.get_type(units="") == "No Type"
    assert ut.get_type(units="farad") == "Derived"
    assert ut.get_type(units="N m s") == "Composite"
    assert ut.get_type(units="C^2") == "Temperature Difference"


def test_unit_as_attribute():
    ut = pyunits.Units()

    assert ut.kg == "kg"
    assert ut.psi == "psi"
    assert ut.A == "A"

    with pytest.raises(pyunits.QuantityError) as e_info:
        ut.xyz
