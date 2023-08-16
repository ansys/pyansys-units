import pytest

import ansys.units as q


def test_pre_defined_unit_system():
    us = q.UnitSystem(unit_sys="SI")
    assert us.name == "SI"
    assert us.base_units == ["kg", "m", "s", "K", "radian", "mol", "cd", "A", "sr"]


def test_custom_unit_system():
    us = q.UnitSystem(
        name="sys",
        base_units=["slug", "ft", "s", "R", "radian", "slugmol", "cd", "A", "sr"],
    )
    assert us.name == "sys"
    assert us.base_units == [
        "slug",
        "ft",
        "s",
        "R",
        "radian",
        "slugmol",
        "cd",
        "A",
        "sr",
    ]


def test_conversion():
    us1 = q.UnitSystem(unit_sys="BT")
    q1 = q.Quantity(10, "kg ft s")

    q2 = us1.convert(q1)
    assert q2.value == 0.6852176585679174
    assert q2.units == "slug ft s"

    us2 = q.UnitSystem(
        name="sys", base_units=["kg", "m", "s", "K", "radian", "mol", "cd", "A", "sr"]
    )
    q3 = q.Quantity(4, "slug cm s")

    q4 = us2.convert(q3)
    assert q4.value == 0.5837561174882547
    assert q4.units == "kg m s"


def test_errors():
    with pytest.raises(q.UnitSystemError) as e_info:
        us1 = q.UnitSystem(
            name="sys",
            base_units=["slug", "ft", "s", "R", "radian", "slugmol", "cd", "A", "sr"],
            unit_sys="BT",
        )

    with pytest.raises(q.UnitSystemError) as e_info:
        us2 = q.UnitSystem(
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

    with pytest.raises(q.UnitSystemError) as e_info:
        us3 = q.UnitSystem(
            name="sys",
            base_units=["slug", "ft", "eon", "R", "radian", "slugmol", "cd", "A", "sr"],
        )

    with pytest.raises(q.UnitSystemError) as e_info:
        us4 = q.UnitSystem(
            name="sys",
            base_units=["m", "ft", "s", "R", "radian", "slugmol", "cd", "A", "sr"],
        )

    with pytest.raises(q.UnitSystemError) as e_info:
        us5 = q.UnitSystem(unit_sys="Standard")


def test_error_messages():
    e1 = q.UnitSystemError.EXCESSIVE_PARAMETERS()
    expected_str = "UnitSystem only accepts 1 of the following parameters: " \
                   "(name, base_units) or (unit_sys)."
    assert str(e1) == expected_str

    e2 = q.UnitSystemError.BASE_UNITS_LENGTH(10)
    expected_str = "The `base_units` argument must contain 9 units, currently there are 10."
    assert str(e2) == expected_str

    e3 = q.UnitSystemError.UNIT_UNDEFINED("pizza")
    expected_str = "`pizza` is an undefined unit. To use `pizza` add it to the " \
                   "`fundamental_units` table within cfg.yaml."
    assert str(e3) == expected_str

    e4 = q.UnitSystemError.UNIT_ORDER("Mass", 1, "Light", 7)
    expected_str = "Expected unit of type: `Mass` (order: 1), received unit of type: " \
                   "`Light` (order: 7)."
    assert str(e4) ==  expected_str

    e5 = q.UnitSystemError.INVALID_UNIT_SYS("ham sandwich")
    assert str(e5) == "`ham sandwich` is not a supported unit system."
