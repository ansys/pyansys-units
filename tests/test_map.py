import pytest

import ansys.units as ansunits
from ansys.units.map import UnknownMapItem


def test_quantity_map():
    qm1_map = {
        "Mass": 1,
        "Velocity": 2.5,
        "Current": 3,
        "Light": 1,
        "Epsilon Flux Coefficient": 2,
    }
    qm1 = ansunits.QuantityMap(quantity_map=qm1_map)
    assert qm1.units.name == "kg^3 m^-1.5 s^-6.5 A^3 cd"

    qm2_map = {
        "Temperature": 1,
        "Pressure": 1,
        "Volume": 1,
    }
    qm2 = ansunits.QuantityMap(quantity_map=qm2_map)
    assert qm2.units.name == "K Pa m^3"


def test_errors():
    qm_map = {"Bread": 2, "Chicken": 1, "Eggs": 7, "Milk": -4}
    with pytest.raises(UnknownMapItem) as e_info:
        qm = ansunits.QuantityMap(quantity_map=qm_map)


def test_error_messages():
    e1 = UnknownMapItem("Risk")
    assert str(e1) == "`Risk` is not a valid quantity map item."
