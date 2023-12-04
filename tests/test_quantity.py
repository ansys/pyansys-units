import math

import pytest

import ansys.units as ansunits
from ansys.units.quantity import (  # InvalidFloatUsage,
    ExcessiveParameters,
    IncompatibleDimensions,
    IncompatibleQuantities,
    IncompatibleValue,
    InsufficientArguments,
    NumpyRequired,
)
from ansys.units.unit import IncorrectUnits

DELTA = 1.0e-5


def test_properties():
    dims = ansunits.BaseDimensions
    v = ansunits.Quantity(10.6, "m")
    assert v.value == 10.6
    assert v.units == ansunits.Unit("m")
    assert v.si_value == 10.6
    assert v.si_units == "m"
    assert v.is_dimensionless == False
    assert v.dimensions == ansunits.Dimensions({dims.LENGTH: 1.0})


def test_value_setter():
    v = ansunits.Quantity(1, "m")
    v.value = 20
    assert v.value == 20
    assert v.units == ansunits.Unit("m")


def test_copy():
    meter = ansunits.Quantity(1.0, "m")
    copy_meter = ansunits.Quantity(copy_from=meter)

    assert meter == copy_meter

    two_meter = ansunits.Quantity(2, copy_from=meter)

    assert two_meter == ansunits.Quantity(2.0, "m")


def test_array():
    try:
        import numpy as np

        arr = np.array([7, 6, 5])
        meter = ansunits.Quantity(arr, "m")

        assert np.array_equal(meter.value, arr)
        list_meter = ansunits.Quantity([7, 6, 5], "m")

        assert np.array_equal(list_meter.value, arr)

    except ImportError:
        with pytest.raises(NumpyRequired):
            e1 = ansunits.Quantity(7, "kg").__array__()

        with pytest.raises(NumpyRequired):
            e2 = ansunits.Quantity([7, 8, 9], "kg")


def test_to():
    v = ansunits.Quantity(1.0, "m")
    to = v.to("ft")
    assert to.value == pytest.approx(3.2808398, DELTA)
    assert to.units == ansunits.Unit("ft")


def test_temperature_to():
    dims = ansunits.BaseDimensions
    t1 = ansunits.Quantity(273.15, "K")
    t1C = t1.to("C")
    assert t1C.dimensions == ansunits.Dimensions({dims.TEMPERATURE: 1.0})
    assert t1C.value == 0.0
    assert t1C.units == ansunits.Unit("C")


def test_complex_temperature_difference_to():
    t1 = ansunits.Quantity(1.0, "K")
    t2 = ansunits.Quantity(2.0, "K")
    m = ansunits.Quantity(1.0, "kg")
    result = m * (t2 - t1)
    resultC2 = result.to("kg delta_C")
    assert resultC2.value == 1.0
    assert resultC2.units == ansunits.Unit("kg delta_C")


def test_repr():
    v = ansunits.Quantity(1.0, "m")
    assert v.__repr__() == 'Quantity (1.0, "m")'


def test_math():
    deg = ansunits.Quantity(90, "degree")
    assert math.sin(deg) == 1.0

    rad = ansunits.Quantity(math.pi / 2, "radian")
    assert math.sin(rad) == 1.0

    root = ansunits.Quantity(100.0, "")
    assert math.sqrt(root) == 10.0


def test_subtraction():
    q1 = ansunits.Quantity(10.0, "m s^-1")
    q2 = ansunits.Quantity(5.0, "m s^-1")
    q3 = ansunits.Quantity(5.0)
    q4 = q3 - 2

    assert (q1 - q2).si_value == 5.0
    assert (q2 - q1).si_value == -5.0
    assert q4.value == 3

    with pytest.raises(IncorrectUnits) as e_info:
        assert q1 - q3


def test_reverse_subtraction():
    q1 = ansunits.Quantity(5.0)
    q2 = 2 - q1

    assert q2.value == 3


def test_temp_subtraction():
    dims = ansunits.BaseDimensions
    t1 = ansunits.Quantity(1.0, "K")
    assert t1.si_value == 1.0

    t2 = ansunits.Quantity(2.0, "K")
    assert t2.si_value == 2.0

    dt1 = t2 - t1
    assert dt1.si_value == 1.0
    assert dt1.dimensions == ansunits.Dimensions({dims.TEMPERATURE_DIFFERENCE: 1.0})

    t3 = ansunits.Quantity(1.0, "C")
    assert t3.si_value == 274.15

    t4 = ansunits.Quantity(2.0, "C")
    assert t4.si_value == 275.15

    dt2 = t4 - t3
    assert dt2.si_value == 1.0
    assert dt2.dimensions == ansunits.Dimensions({dims.TEMPERATURE_DIFFERENCE: 1.0})


def test_pow():
    q1 = ansunits.Quantity(10.0, "m s^-1")
    q2 = ansunits.Quantity(5.0, "ft")

    q1_sq = q1**2
    assert q1_sq.units == ansunits.Unit("m^2 s^-2")
    assert q1_sq.value == 100
    q2_sq = q2**2
    assert q2_sq.units == ansunits.Unit("m^2")
    assert q2_sq.si_value == pytest.approx(2.3225759999999993, DELTA)

    assert q1.si_value**2 == 100.0
    assert q2.si_value**2 == pytest.approx(2.3225759999999993, DELTA)


def test_mul():
    q1 = ansunits.Quantity(10.0, "m s^-1")
    q2 = ansunits.Quantity(5.0, "ft")
    u1 = ansunits.Unit("kg")

    q3 = q1 * q2
    assert q3.units == ansunits.Unit("m^2 s^-1")
    assert q3.si_value == pytest.approx(15.239999999999998, DELTA)

    q4 = q1 * u1
    assert q4.units == ansunits.Unit("kg m s^-1")
    assert q4.value == pytest.approx(10, DELTA)

    q5 = q2 * 3
    assert q5.units == ansunits.Unit("m")
    assert q5.si_value == pytest.approx(4.571999999999999, DELTA)


def test_reverse_mul():
    q1 = ansunits.Quantity(10.0, "m s^-1")
    u1 = ansunits.Unit("kg")

    q3 = u1 * q1
    assert q3.units == ansunits.Unit("m s^-1 kg")
    assert q3.value == pytest.approx(10, DELTA)


def test_neg():
    q0 = ansunits.Quantity(10.0, "m s^-1")
    q1 = -q0
    assert q1.value == -10.0


def test_ne():
    x = ansunits.Quantity(10.5, "cm")
    y = ansunits.Quantity(10.5, "m")
    z = ansunits.Quantity(10.5, "g")
    r = ansunits.Quantity(10.5, "")

    assert y != x
    assert x != y

    assert r != 0.5
    assert 0.5 != r


def test_eq():
    x = ansunits.Quantity(10.5, "cm")
    y = ansunits.Quantity(10.5, "m")
    r = ansunits.Quantity(10.5, "")

    l = ansunits.Quantity(10.5, "cm")
    m = ansunits.Quantity(10.5, "kg")

    n = ansunits.Quantity(10.5, "")

    assert x == l
    assert r == n
    assert r == 10.5

    with pytest.raises(IncompatibleQuantities):
        assert x == 0.5

    with pytest.raises(IncompatibleDimensions):
        assert m == y
        assert x == 0.5


def test_rdiv():
    q1 = ansunits.Quantity(10.0, "m s^-1")

    q2 = 50 / q1
    assert q2.value == 5
    assert q2.units == ansunits.Unit("m^-1 s")


def test_quantity_divided_by_unit():
    dims = ansunits.BaseDimensions
    ur = ansunits.UnitRegistry()
    mass = ansunits.Quantity(10.0, ur.kg)
    mass_flow_rate = mass / ur.s
    assert mass_flow_rate.units == ansunits.Unit("kg s^-1")
    assert mass_flow_rate.value == 10
    assert mass_flow_rate.dimensions == ansunits.Dimensions(
        {dims.MASS: 1.0, dims.TIME: -1.0}
    )


def test_quantity_divided_by_number():
    ur = ansunits.UnitRegistry()
    mass = ansunits.Quantity(10.0, ur.kg)
    half_m = mass / 2
    assert half_m.units == ansunits.Unit("kg")
    assert half_m.value == 5


def test_exponent():
    qt = ansunits.Quantity(5.0, "m^0")
    qtm = qt**2

    assert qtm.value == 25.0
    assert qtm.dimensions == ansunits.Dimensions()
    assert qtm.units == ansunits.Unit("")


def test_addition():
    q1 = ansunits.Quantity(5.0, "m^0")
    q3 = ansunits.Quantity(52, "N")

    q2 = q1 + 5
    assert q2.units.name == ""
    assert q2.value == 10

    with pytest.raises(IncorrectUnits) as e_info:
        assert q1 - q3


def test_reverse_addition():
    q1 = ansunits.Quantity(5.0, "m^0")

    q2 = 5 + q1
    assert q2.units.name == ""
    assert q2.value == 10


def test_ge():
    x = ansunits.Quantity(10.5, "cm")
    y = ansunits.Quantity(10.5, "m")
    z = ansunits.Quantity(10.5, "g")
    r = ansunits.Quantity(10.5, "")

    assert y >= x
    assert 15.7 >= r
    assert r >= 7.8

    with pytest.raises(IncompatibleDimensions) as e_info:
        assert x >= z

    with pytest.raises(IncompatibleQuantities) as e_info:
        assert x >= 5.0


def test_gt():
    x = ansunits.Quantity(10.5, "cm")
    y = ansunits.Quantity(10.5, "m")
    z = ansunits.Quantity(10.5, "g")
    r = ansunits.Quantity(10.5, "")

    assert y > x
    assert 15.7 > r
    assert r > 7.8

    with pytest.raises(IncompatibleDimensions) as e_info:
        assert x > z

    with pytest.raises(IncompatibleQuantities) as e_info:
        assert x > 5.0


def test_lt():
    x = ansunits.Quantity(10.5, "cm")
    y = ansunits.Quantity(10.5, "m")
    z = ansunits.Quantity(10.5, "g")
    r = ansunits.Quantity(10.5, "")

    assert x < y
    assert r < 15.7
    assert 7.8 < r

    with pytest.raises(IncompatibleDimensions) as e_info:
        assert z < x

    with pytest.raises(IncompatibleQuantities) as e_info:
        assert x < 5.0


def test_le():
    x = ansunits.Quantity(10.5, "cm")
    y = ansunits.Quantity(10.5, "m")
    z = ansunits.Quantity(10.5, "g")
    r = ansunits.Quantity(10.5, "")

    assert x <= y
    assert r <= 15.7
    assert 7.8 <= r

    with pytest.raises(IncompatibleDimensions) as e_info:
        assert z <= x

    with pytest.raises(IncompatibleQuantities) as e_info:
        assert x <= 5.0


def test_temp():
    k = ansunits.Quantity(-40, "K")

    kc = k.to("delta_C")
    assert kc.value == pytest.approx(-40.0, DELTA)
    assert kc.units == ansunits.Unit("delta_C")

    kc = k.to("delta_R")
    assert kc.value == pytest.approx(-72.0, DELTA)
    assert kc.units == ansunits.Unit("delta_R")

    kc = k.to("delta_F")
    assert kc.value == pytest.approx(-72.0, DELTA)
    assert kc.units == ansunits.Unit("delta_F")


def test_temp_addition():
    t1 = ansunits.Quantity(150.0, "C")
    t2 = ansunits.Quantity(50.0, "C")

    td = t1 - t2
    assert td.units == ansunits.Unit("delta_K")
    assert td.si_value == 100.0

    kd = ansunits.Quantity(50.0, "delta_C")
    k = ansunits.Quantity(50.0, "K")

    t = k + kd
    assert t.si_value == 100.0
    assert t.units == ansunits.Unit("K")


def test_quantity_from_dimensions():
    dims = ansunits.BaseDimensions
    p = ansunits.Quantity(
        10.5,
        dimensions=ansunits.Dimensions(
            {dims.MASS: 1.0, dims.LENGTH: -1.0, dims.TIME: -2.0}
        ),
    )
    assert p.units == ansunits.Unit("kg m^-1 s^-2")


def test_quantity_map():
    quantity_map_from_settings_API = {
        "Mass": 1,
        "Velocity": 2.5,
        "Current": 3,
        "Light": 1,
        "Epsilon Flux Coefficient": 2,
    }

    api_test = ansunits.Quantity(10.5, quantity_map=quantity_map_from_settings_API)
    assert api_test.value == 10.5
    assert api_test.units == ansunits.Unit("kg^3 m^-1.5 s^-6.5 A^3 cd")


def testing_units_to_dimensions():
    print(f"{'*' * 25} {testing_units_to_dimensions.__name__} {'*' * 25}")
    dims = ansunits.BaseDimensions

    def dim_test(units, dim_dict):
        qt = ansunits.Quantity(10, units)
        print(f"{units} : {qt.dimensions}")
        assert qt.dimensions == ansunits.Dimensions(dim_dict)

    dim_test("m", {dims.LENGTH: 1.0})
    dim_test("m s^-1", {dims.LENGTH: 1.0, dims.TIME: -1.0})
    dim_test("kg m s^-2 m^-2", {dims.MASS: 1.0, dims.LENGTH: -1.0, dims.TIME: -2.0})
    dim_test("Pa", {dims.MASS: 1.0, dims.LENGTH: -1.0, dims.TIME: -2.0})
    dim_test("kPa", {dims.MASS: 1.0, dims.LENGTH: -1.0, dims.TIME: -2.0})
    dim_test("Pa^2", {dims.MASS: 2.0, dims.LENGTH: -2.0, dims.TIME: -4.0})
    dim_test("daPa", {dims.MASS: 1.0, dims.LENGTH: -1.0, dims.TIME: -2.0})
    dim_test("MPa", {dims.MASS: 1.0, dims.LENGTH: -1.0, dims.TIME: -2.0})
    dim_test("kPa^2", {dims.MASS: 2.0, dims.LENGTH: -2.0, dims.TIME: -4.0})
    dim_test("slug in^-1 s^-1", {dims.MASS: 1.0, dims.LENGTH: -1.0, dims.TIME: -1.0})
    dim_test("radian", {dims.ANGLE: 1.0})
    dim_test(
        "ohm", {dims.MASS: 1.0, dims.LENGTH: 2.0, dims.TIME: -3.0, dims.CURRENT: -2.0}
    )
    dim_test("lb cm s^-2", {dims.MASS: 1.0, dims.LENGTH: 1.0, dims.TIME: -2.0})
    print("-" * 75)


def testing_multipliers():
    print(f"{'*' * 25} {testing_multipliers.__name__} {'*' * 25}")

    def from_to(from_str, to_str):
        qt = ansunits.Quantity(1, from_str)
        to = qt.to(to_str)
        print(f"from {qt} -> to {to}")

    from_to("mm", "cm")
    from_to("m", "ft")
    from_to("dm^3", "m^3")
    from_to("m s^-1", "cm s^-1")
    from_to("N", "dyne")
    from_to("m^2", "in^2")
    from_to("degree s^-1", "radian s^-1")
    from_to("radian s^-1", "degree s^-1")
    from_to("Pa", "lb m s^-2 ft^-2")
    from_to("lb m s^-2 ft^-2", "Pa")

    from_to("J kg^-1 K^-1", "J kg^-1 C^-1")
    from_to("J kg^-1 K^-1", "J kg^-1 R^-1")
    from_to("J kg^-1 K^-1", "J kg^-1 F^-1")

    from_to("K", "C")
    from_to("K", "R")
    from_to("K", "F")

    print("-" * 75)


def test_excessive_parameters_error():
    dims = ansunits.BaseDimensions
    with pytest.raises(ExcessiveParameters):
        e1 = ansunits.Quantity(
            value=10,
            units="farad",
            dimensions=ansunits.Dimensions({dims.MASS: 1}),
            quantity_map={"Velocity": 3},
        )
    with pytest.raises(InsufficientArguments):
        e2 = ansunits.Quantity()


def test_incompatible_dimensions_error():
    ur = ansunits.UnitRegistry()
    with pytest.raises(IncompatibleDimensions):
        e1 = ansunits.Quantity(7, ur.kg).to(ur.ft)


def test_error_messages():
    e1 = ExcessiveParameters()
    assert (
        str(e1)
        == "Quantity only accepts one of the following parameters: \
            (units) or (quantity_map) or (dimensions)."
    )

    e2 = IncompatibleDimensions(ansunits.Unit("mm"), ansunits.Unit("K"))
    assert str(e2) == "`mm` and `K` have incompatible dimensions."

    e3 = IncompatibleValue("radian")
    assert str(e3) == "`radian` is incompatible with the current quantity object."
