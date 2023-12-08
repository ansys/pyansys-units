import pytest

import ansys.units as ansunits
from ansys.units.systems import IncorrectUnitType, InvalidUnitSystem, NotBaseUnit


def test_pre_defined_unit_system():
    ur = ansunits.UnitRegistry()
    us = ansunits.UnitSystem(system="SI")
    assert us.MASS == ur.kg
    assert us.LENGTH == ur.m
    assert us.TIME == ur.s
    assert us.TEMPERATURE == ur.K
    assert us.TEMPERATURE_DIFFERENCE == ur.delta_K
    assert us.ANGLE == ur.radian
    assert us.CHEMICAL_AMOUNT == ur.mol
    assert us.LIGHT == ur.cd
    assert us.CURRENT == ur.A
    assert us.SOLID_ANGLE == ur.sr


def test_repr():
    us = ansunits.UnitSystem()
    us_dict = {
        "MASS": "kg",
        "LENGTH": "m",
        "TIME": "s",
        "TEMPERATURE": "K",
        "TEMPERATURE_DIFFERENCE": "delta_K",
        "ANGLE": "radian",
        "CHEMICAL_AMOUNT": "mol",
        "LIGHT": "cd",
        "CURRENT": "A",
        "SOLID_ANGLE": "sr",
    }
    assert repr(us) == str(us_dict)


def test_copy():
    us = ansunits.UnitSystem(system="BT")
    us1 = ansunits.UnitSystem(copy_from=us)
    assert us1 == us


def test_update():
    dims = ansunits.BaseDimensions
    ur = ansunits.UnitRegistry()
    us = ansunits.UnitSystem(system="SI")
    base_units = {
        dims.MASS: "slug",
        dims.LENGTH: ur.ft,
        dims.TIME: ur.s,
        dims.TEMPERATURE: ur.R,
        dims.TEMPERATURE_DIFFERENCE: ur.delta_R,
        dims.ANGLE: ur.degree,
        dims.CHEMICAL_AMOUNT: ur.slugmol,
        dims.LIGHT: ur.cd,
        dims.CURRENT: ur.A,
        dims.SOLID_ANGLE: ur.sr,
    }
    us.update(base_units=base_units)
    assert us.MASS == ur.slug
    assert us.LENGTH == ur.ft
    assert us.TIME == ur.s
    assert us.TEMPERATURE == ur.R
    assert us.TEMPERATURE_DIFFERENCE == ur.delta_R
    assert us.ANGLE == ur.degree
    assert us.CHEMICAL_AMOUNT == ur.slugmol
    assert us.LIGHT == ur.cd
    assert us.CURRENT == ur.A
    assert us.SOLID_ANGLE == ur.sr


def test_eq():
    us1 = ansunits.UnitSystem(system="BT")
    us2 = ansunits.UnitSystem()
    us3 = ansunits.UnitSystem(system="SI")
    assert (us1 == us2) == False
    assert us2 == us3


def test_set_type():
    ur = ansunits.UnitRegistry()
    us = ansunits.UnitSystem(system="SI")
    us.MASS = ur.slug
    us.LENGTH = ur.ft
    us.TEMPERATURE = ur.R
    us.TEMPERATURE_DIFFERENCE = ur.delta_R
    us.ANGLE = ur.degree
    us.CHEMICAL_AMOUNT = ur.slugmol
    assert us.MASS == ur.slug
    assert us.LENGTH == ur.ft
    assert us.TEMPERATURE == ur.R
    assert us.TEMPERATURE_DIFFERENCE == ur.delta_R
    assert us.ANGLE == ur.degree
    assert us.CHEMICAL_AMOUNT == ur.slugmol


def test_custom_unit_system():
    dims = ansunits.BaseDimensions
    ur = ansunits.UnitRegistry()
    us = ansunits.UnitSystem(
        base_units={
            dims.MASS: ur.slug,
            dims.LENGTH: ur.ft,
            dims.TIME: ur.s,
            dims.TEMPERATURE: ur.R,
            dims.TEMPERATURE_DIFFERENCE: ur.delta_R,
            dims.ANGLE: ur.radian,
            dims.CHEMICAL_AMOUNT: ur.slugmol,
            dims.LIGHT: ur.cd,
            dims.CURRENT: ur.A,
            dims.SOLID_ANGLE: ur.sr,
        }
    )
    assert us.MASS == ur.slug
    assert us.LENGTH == ur.ft
    assert us.TIME == ur.s
    assert us.TEMPERATURE == ur.R
    assert us.TEMPERATURE_DIFFERENCE == ur.delta_R
    assert us.ANGLE == ur.radian
    assert us.CHEMICAL_AMOUNT == ur.slugmol
    assert us.LIGHT == ur.cd
    assert us.CURRENT == ur.A
    assert us.SOLID_ANGLE == ur.sr


def test_conversion():
    us1 = ansunits.UnitSystem(system="BT")
    q1 = ansunits.Quantity(10, "kg ft s")

    q2 = us1.convert(q1)
    assert q2.value == 0.6852176585679174
    assert q2.units == ansunits.Unit("slug ft s")

    us2 = ansunits.UnitSystem(system="SI")
    q3 = ansunits.Quantity(4, "slug cm s")

    q4 = us2.convert(q3)
    assert q4.value == 0.5837561174882547
    assert q4.units == ansunits.Unit("kg m s")


def test_not_base_unit_init():
    dims = ansunits.BaseDimensions
    ur = ansunits.UnitRegistry()

    with pytest.raises(NotBaseUnit):
        us1 = ansunits.UnitSystem(base_units={dims.LENGTH: ur.N})


def test_not_base_unit_update():
    dims = ansunits.BaseDimensions
    ur = ansunits.UnitRegistry()
    us = ansunits.UnitSystem(system="SI")
    base_units = {dims.MASS: ur.N}

    with pytest.raises(NotBaseUnit):
        us.update(base_units=base_units)


def test_invalid_unit_sys():
    with pytest.raises(InvalidUnitSystem):
        us2 = ansunits.UnitSystem(system="Standard")


def test_wrong_unit_type():
    ur = ansunits.UnitRegistry()
    us = ansunits.UnitSystem()

    with pytest.raises(IncorrectUnitType):
        us.TIME = ur.m
    with pytest.raises(IncorrectUnitType):
        us.LIGHT = ur.sr
    with pytest.raises(IncorrectUnitType):
        us.CURRENT = ur.ft
    with pytest.raises(IncorrectUnitType):
        us.SOLID_ANGLE = ur.radian


def test_error_messages():
    e1 = NotBaseUnit(ansunits.Unit("kg s^-1"))
    expected_str = (
        "`kg s^-1` is not a base unit. To use `kg s^-1`, add it to the "
        "`base_units` table within the cfg.yaml file."
    )
    assert str(e1) == expected_str

    e2 = InvalidUnitSystem("ham sandwich")
    assert str(e2) == "`ham sandwich` is not a supported unit system."

    e3 = IncorrectUnitType(
        unit=ansunits.Unit("ft"), unit_type=ansunits.BaseDimensions.MASS
    )
    assert str(e3) == "The unit `ft` is incompatible with unit system type: `MASS`"
