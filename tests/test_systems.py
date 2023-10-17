import pytest

import ansys.units as ansunits


def test_pre_defined_unit_system():
    ur = ansunits.UnitRegistry()
    us = ansunits.UnitSystem(unit_sys="SI")
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


def test_eq():
    us1 = ansunits.UnitSystem(unit_sys="BT")
    us2 = ansunits.UnitSystem()
    assert (us1 == us2) == False


def test_copy():
    us = ansunits.UnitSystem(unit_sys="BT")
    us1 = ansunits.UnitSystem(copy_from=us)
    assert us1 == us


def test_update():
    dims = ansunits.BaseDimensions
    ur = ansunits.UnitRegistry()
    us = ansunits.UnitSystem(unit_sys="SI")
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


def test_single_set():
    ur = ansunits.UnitRegistry()
    us = ansunits.UnitSystem(unit_sys="SI")
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
        },
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
    dims = ansunits.BaseDimensions
    ur = ansunits.UnitRegistry()
    us1 = ansunits.UnitSystem(unit_sys="BT")
    q1 = ansunits.Quantity(10, "kg ft s")

    q2 = us1.convert(q1)
    assert q2.value == 0.6852176585679174
    assert q2.units == "slug ft s"

    us2 = ansunits.UnitSystem(unit_sys="SI")
    q3 = ansunits.Quantity(4, "slug cm s")

    q4 = us2.convert(q3)
    assert q4.value == 0.5837561174882547
    assert q4.units == "kg m s"


def test_not_base_unit_init():
    with pytest.raises(ansunits.UnitSystemError):
        dims = ansunits.BaseDimensions
        ur = ansunits.UnitRegistry()
        us1 = ansunits.UnitSystem(
            base_units={
                dims.MASS: ur.slug,
                dims.LENGTH: ur.N,
                dims.TIME: ur.s,
                dims.TEMPERATURE: ur.R,
                dims.TEMPERATURE_DIFFERENCE: ur.delta_R,
                dims.ANGLE: ur.radian,
                dims.CHEMICAL_AMOUNT: ur.slugmol,
                dims.LIGHT: ur.cd,
                dims.CURRENT: ur.A,
                dims.SOLID_ANGLE: ur.sr,
            },
        )


def test_not_base_unit_update():
    with pytest.raises(ansunits.UnitSystemError):
        dims = ansunits.BaseDimensions
        ur = ansunits.UnitRegistry()
        us = ansunits.UnitSystem(unit_sys="SI")
        base_units = {dims.MASS: ur.N}
        us.update(base_units=base_units)


def test_INVALID_UNIT_SYS():
    with pytest.raises(ansunits.UnitSystemError):
        us2 = ansunits.UnitSystem(unit_sys="Standard")


def test_error_messages():
    e1 = ansunits.UnitSystemError.BASE_UNITS_LENGTH(11)
    expected_str = "The `base_units` argument must contain 10 unique units, currently there are 11."
    assert str(e1) == expected_str

    e2 = ansunits.UnitSystemError.NOT_BASE_UNIT(ansunits.Unit("kg s^-1"))
    expected_str = (
        "`kg s^-1` is not a base unit. To use `kg s^-1`, add it to the "
        "`base_units` table within the cfg.yaml file."
    )
    assert str(e2) == expected_str

    e3 = ansunits.UnitSystemError.INVALID_UNIT_SYS("ham sandwich")
    assert str(e3) == "`ham sandwich` is not a supported unit system."
