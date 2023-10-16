import pytest

import ansys.units as ansunits


def test_pre_defined_unit_system():
    us = ansunits.UnitSystem(unit_sys="SI")
    assert us.name == "SI"
    assert us.base_units == [
        "kg",
        "m",
        "s",
        "K",
        "delta_K",
        "radian",
        "mol",
        "cd",
        "A",
        "sr",
    ]


def test_custom_unit_system():
    ur = ansunits.UnitRegistry()
    us = ansunits.UnitSystem(
        name="sys",
        base_units=[
            ur.slug,
            ur.ft,
            ur.s,
            ur.R,
            ur.delta_R,
            ur.radian,
            ur.slugmol,
            ur.cd,
            ur.A,
            ur.sr,
        ],
    )
    assert us.name == "sys"
    assert us.base_units == [
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
    ]


def test_conversion():
    us1 = ansunits.UnitSystem(unit_sys="BT")
    q1 = ansunits.Quantity(10, "kg ft s")

    q2 = us1.convert(q1)
    assert q2.value == 0.6852176585679174
    assert q2.units == "slug ft s"

    us2 = ansunits.UnitSystem(
        name="sys",
        base_units=["kg", "m", "s", "K", "delta_K", "radian", "mol", "cd", "A", "sr"],
    )
    q3 = ansunits.Quantity(4, "slug cm s")

    q4 = us2.convert(q3)
    assert q4.value == 0.5837561174882547
    assert q4.units == "kg m s"


def test_errors():
    with pytest.raises(ansunits.UnitSystemError) as e_info:
        us1 = ansunits.UnitSystem(
            name="sys",
            base_units=["slug", "ft", "s", "R", "radian", "slugmol", "cd", "A", "sr"],
            unit_sys="BT",
        )

    with pytest.raises(ansunits.UnitSystemError) as e_info:
        us2 = ansunits.UnitSystem(
            name="sys",
            base_units=[
                "slug",
                "ft",
                "s",
                "R",
                "radian",
                "slugmol",
                "cd",
                "A",
                "sr",
                "cd",
                "A",
                "sr",
            ],
        )

    with pytest.raises(ansunits.UnitSystemError) as e_info:
        us3 = ansunits.UnitSystem(
            name="sys",
            base_units=[
                "slug",
                "ft",
                "N",
                "R",
                "delta_R",
                "radian",
                "slugmol",
                "cd",
                "A",
                "sr",
            ],
        )

    with pytest.raises(ansunits.UnitSystemError) as e_info:
        us4 = ansunits.UnitSystem(
            name="sys",
            base_units=[
                "slug",
                "slug",
                "s",
                "R",
                "delta_R",
                "radian",
                "slugmol",
                "cd",
                "A",
                "sr",
            ],
        )

    with pytest.raises(ansunits.UnitSystemError) as e_info:
        us5 = ansunits.UnitSystem(
            name="sys",
            base_units=["m", "ft", "s", "R", "radian", "slugmol", "cd", "A", "sr"],
        )

    with pytest.raises(ansunits.UnitSystemError) as e_info:
        us6 = ansunits.UnitSystem(unit_sys="Standard")

    with pytest.raises(ansunits.UnitSystemError) as e_info:
        us7 = ansunits.UnitSystem(
            name="us6",
            base_units=[
                "kg s^-1",
                "ft",
                "s",
                "R",
                "radian",
                "slugmol",
                "cd",
                "A",
                "sr",
            ],
        )

    with pytest.raises(ansunits.UnitSystemError) as e_info:
        us6 = ansunits.UnitSystem(
            name="us6",
            base_units=[
                "kg s^-1",
                "ft",
                "s",
                "R",
                "radian",
                "slugmol",
                "cd",
                "A",
                "sr",
            ],
        )


def test_error_messages():
    e1 = ansunits.UnitSystemError.EXCESSIVE_PARAMETERS()
    expected_str = (
        "UnitSystem only accepts one of the following parameters: "
        "(name, base_units) or (unit_sys)."
    )
    assert str(e1) == expected_str

    e2 = ansunits.UnitSystemError.BASE_UNITS_LENGTH(11)
    expected_str = "The `base_units` argument must contain 10 unique units, currently there are 11."
    assert str(e2) == expected_str

    e3 = ansunits.UnitSystemError.NOT_BASE_UNIT(ansunits.Unit("kg s^-1"))
    expected_str = (
        "`kg s^-1` is not a base unit. To use `kg s^-1`, add it to the "
        "`base_units` table within the cfg.yaml file."
    )
    assert str(e3) == expected_str

    e4 = ansunits.UnitSystemError.INVALID_UNIT_SYS("ham sandwich")
    assert str(e4) == "`ham sandwich` is not a supported unit system."


def test_si_properties():
    us = ansunits.UnitSystem()
    assert us.MASS.name == "kg"
    assert us.ANGLE.name == "radian"
    assert us.CHEMICAL_AMOUNT.name == "mol"
    assert us.LENGTH.name == "m"
    assert us.CURRENT.name == "A"
    assert us.SOLID_ANGLE.name == "sr"
    assert us.TEMPERATURE.name == "K"
    assert us.TEMPERATURE_DIFFERENCE.name == "delta_K"
    assert us.LIGHT.name == "cd"
    assert us.TIME.name == "s"
