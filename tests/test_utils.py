import ansys.units as ansunits
from ansys.units.utils import (
    _has_multiplier,
    _si_map,
    condense,
    filter_unit_term,
    get_type,
    si_data,
)


def test_tables():
    assert isinstance(ansunits._api_quantity_map, dict)
    assert isinstance(ansunits._fundamental_units, dict)
    assert isinstance(ansunits._derived_units, dict)
    assert isinstance(ansunits._multipliers, dict)
    assert isinstance(ansunits._unit_systems, dict)


def test_has_multiplier():
    assert _has_multiplier("km")
    assert _has_multiplier("ms")
    assert _has_multiplier("dam")

    assert not _has_multiplier("kg")
    assert not _has_multiplier("cm")
    assert not _has_multiplier("m")


def test_si_map():
    assert _si_map("g") == "kg"
    assert _si_map("lbm") == "kg"
    assert _si_map("ft") == "m"
    assert _si_map("slugmol") == "mol"
    assert _si_map("degree") == "radian"


def test_filter_unit_term():
    assert filter_unit_term("cm^-2") == ("", "cm", -2)
    assert filter_unit_term("m") == ("", "m", 1)
    assert filter_unit_term("K^4") == ("", "K", 4)
    assert filter_unit_term("dam") == ("da", "m", 1)
    assert filter_unit_term("mm") == ("m", "m", 1)


def test_si_data():
    u1, m1, o1 = si_data(units="g")
    assert u1 == "kg"
    assert m1 == 0.001
    assert o1 == 0

    u2, m2, o2 = si_data(units="lb")
    assert u2 == "kg"
    assert m2 == 0.45359237
    assert o2 == 0

    u3, m3, o3 = si_data(units="ft^2")
    assert u3 == "m^2"
    assert m3 == 0.09290303999999998
    assert o3 == 0

    u4, m4, o4 = si_data(units="F")
    assert u4 == "K"
    assert m4 == 0.55555555555
    assert o4 == 459.67

    u5, m5, o5 = si_data(units="farad")
    assert u5 == "kg^-1 m^-2 s^4 A^2"
    assert m5 == 1
    assert o5 == 0


def test_condense():
    assert condense("m m m m") == "m^4"
    assert condense("kg ft^3 kg^-2") == "kg^-1 ft^3"
    assert condense("s^2 s^-2") == ""


def test_get_type():
    assert get_type(units="kg") == "MASS"
    assert get_type(units="m") == "LENGTH"
    assert get_type(units="s") == "TIME"
    assert get_type(units="K") == "TEMPERATURE"
    assert get_type(units="delta_K") == "TEMPERATURE_DIFFERENCE"
    assert get_type(units="radian") == "ANGLE"
    assert get_type(units="mol") == "CHEMICAL_AMOUNT"
    assert get_type(units="cd") == "LIGHT"
    assert get_type(units="A") == "CURRENT"
    assert get_type(units="sr") == "SOLID_ANGLE"
    assert get_type(units="") == "No Type"
    assert get_type(units="farad") == "Derived"
    assert get_type(units="N m s") == "Composite"
    assert get_type(units="C^2") == "Composite"
