# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import importlib.util
import math

from numpy.typing import NDArray
import pytest

from ansys.units import (
    BaseDimensions,
    Dimensions,
    Quantity,
    Unit,
    UnitRegistry,
    UnitSystem,
)
from ansys.units.common import Pa, kg, m
from ansys.units.quantity import (  # InvalidFloatUsage,
    ExcessiveParameters,
    IncompatibleDimensions,
    IncompatibleQuantities,
    IncompatibleValue,
    InsufficientArguments,
    NumPyRequired,
    RequiresUniqueDimensions,
    get_si_value,
)
from ansys.units.unit import IncorrectUnits, ProhibitedTemperatureOperation

DELTA = 1.0e-5


def test_preferred_units():
    Quantity.preferred_units(units=["J", "slug", "psi"])
    assert Quantity._chosen_units == [Unit("J"), Unit("slug"), Unit("psi")]

    with pytest.raises(RequiresUniqueDimensions):
        Quantity.preferred_units(units=["kg"])

    Quantity.preferred_units(units=["slug"], remove=True)
    Quantity.preferred_units(units=["kg"])
    Quantity.preferred_units(units=[kg * Pa])

    ten_pa = Quantity(10, units="Pa")
    assert ten_pa.value == pytest.approx(0.0014503773773020918, DELTA)
    assert ten_pa.units == Unit(units="psi")

    ten_slug = Quantity(10, units="slug")
    assert ten_slug.value == pytest.approx(145.93902937206367, DELTA)
    assert ten_slug.units == Unit(units="kg")

    assert (ten_slug * ten_pa).value == pytest.approx(1459.3902937206367, DELTA)
    assert (ten_slug * ten_pa).units == Unit(units="kg Pa")

    ten_N = Quantity(10, units="N")
    ten_m = Quantity(10, units="m")

    assert (ten_N * ten_m).value == pytest.approx(100, DELTA)
    assert (ten_N * ten_m).units == Unit(units="J")

    Quantity.preferred_units(units=["J", "kg", "psi", kg * Pa], remove=True)
    assert Quantity._chosen_units == []


def test_properties():
    dims = BaseDimensions
    v = Quantity(10.6, "m")
    assert v.value == 10.6
    assert v.units == Unit("m")
    assert get_si_value(v) == 10.6
    assert v.units.si_units == "m"
    assert not v.is_dimensionless
    assert v.dimensions == Dimensions({dims.LENGTH: 1.0})


def test_quantity_is_immutable():
    v = Quantity(1, "m")
    with pytest.raises(AttributeError):
        v.value = 20  # pyright: ignore[reportAttributeAccessIssue]  # fmt: skip
    with pytest.raises(AttributeError):
        v.units = "kg"  # pyright: ignore[reportAttributeAccessIssue]  # fmt: skip
    with pytest.raises(AttributeError):
        v.dimensions = Dimensions({})  # pyright: ignore[reportAttributeAccessIssue]  # fmt: skip
    assert v == Quantity(1, "m")


def test_conversion():
    us1 = UnitSystem(system="BT")
    q1 = Quantity(10, "kg ft s")

    q2 = q1.convert(us1)
    assert q2.value == 0.6852176585679174
    assert q2.units == Unit("slug ft s")

    us2 = UnitSystem(system="SI")
    q3 = Quantity(4, "slug cm s")

    q4 = q3.convert(us2)
    assert q4.value == 0.5837561174882547
    assert q4.units == Unit("kg m s")


def test_copy():
    meter = Quantity(1.0, "m")
    copy_meter = Quantity(copy_from=meter)

    assert meter == copy_meter

    two_meter = Quantity(2, copy_from=meter)

    assert two_meter == Quantity(2.0, "m")


def test_array():
    try:
        import numpy as np

        arr = np.array([7, 6, 5])
        meter = Quantity(arr, "m")

        assert np.array_equal(meter.value, arr)
        list_meter = Quantity([7, 6, 5], "m")

        assert np.array_equal(list_meter.value, arr)

    except ImportError:
        with pytest.raises(NumPyRequired):
            Quantity([7, 8, 9], "kg")


def _supporting_numpy():
    return importlib.util.find_spec("numpy") is not None


def test_array_compare():
    if not _supporting_numpy():
        return
    import numpy as np

    why_7s_scary: NDArray[np.floating] = np.array([7, 8, 9])
    assert Quantity(why_7s_scary, "kg") == Quantity(why_7s_scary, "kg")
    assert Quantity(why_7s_scary, "kg") != Quantity(np.array([1, 2, 3]), "kg")
    with pytest.raises(IncompatibleDimensions):
        Quantity(why_7s_scary, "kg") != Quantity(why_7s_scary, "m")
    with pytest.raises(IncompatibleDimensions):
        Quantity(why_7s_scary, "kg") == Quantity(why_7s_scary, "m")
    assert Quantity(why_7s_scary, "kg") != Quantity(why_7s_scary, "g")
    assert Quantity(why_7s_scary, "") == Quantity(why_7s_scary, "")
    assert Quantity(1, "kg") != Quantity([1, 2, 3], "kg")
    assert Quantity([1, 2, 3], "kg") != Quantity(1, "kg")


def test_array_to_si_value():
    if not _supporting_numpy():
        return
    si_value = get_si_value(Quantity([1, 2], "in"))
    assert si_value[0] == get_si_value(Quantity(1, "in"))
    assert si_value[1] == get_si_value(Quantity(2, "in"))


def test_array_to():
    if not _supporting_numpy():
        return
    import numpy as np

    to = Quantity(np.array([1, 2]), "in").to("m")
    assert to.value[0] == get_si_value(Quantity(1, "in"))
    assert to.value[1] == get_si_value(Quantity(2, "in"))


def test_array_index():
    if not _supporting_numpy():
        return
    q = Quantity([1, 2], "m")
    assert q[0] == Quantity(1, "m")
    assert q[1] == Quantity(2, "m")


def test_array_iteration():
    if not _supporting_numpy():
        return
    q = Quantity([1, 2], "m")
    qs = [x for x in q]
    assert qs[0] == Quantity(1, "m")
    assert qs[1] == Quantity(2, "m")
    i = iter(q)
    assert next(i) == Quantity(1, "m")
    assert next(i) == Quantity(2, "m")


def test_to():
    v = Quantity(1.0, "m")
    to = v.to("ft")
    assert to.value == pytest.approx(3.2808398, DELTA)
    assert to.units == Unit("ft")


def test_temperature_to():
    dims = BaseDimensions
    t1 = Quantity(273.15, "K")
    t1C = t1.to("C")
    assert t1C.dimensions == Dimensions({dims.TEMPERATURE: 1.0})
    assert t1C.value == 0.0
    assert t1C.units == Unit("C")


def test_complex_temperature_difference_to():
    t1 = Quantity(1.0, "K")
    t2 = Quantity(2.0, "K")
    m = Quantity(1.0, "kg")
    result = m * (t2 - t1)
    resultC2 = result.to("kg delta_C")
    assert resultC2.value == 1.0
    assert resultC2.units == Unit("kg delta_C")


def test_repr():
    v = Quantity(1.0, "m")
    assert v.__repr__() == 'Quantity(1.0, "m")'


def test_math():
    deg = Quantity(90, "degree")
    assert math.sin(deg) == 1.0

    rad = Quantity(math.pi / 2, "radian")
    assert math.sin(rad) == 1.0

    root = Quantity(100.0, "")
    assert math.sqrt(root) == 10.0


def test_subtraction():
    q1 = Quantity(10.0, "m s^-1")
    q2 = Quantity(5.0, "m s^-1")
    q3 = Quantity(5.0)
    q4 = q3 - 2  # pyright: ignore[reportOperatorIssue, reportUnknownVariableType]  # this won't raise but I don't think this is recommended  # fmt: skip

    assert get_si_value(q1 - q2) == 5.0
    assert get_si_value(q2 - q1) == -5.0
    assert q4.value == 3

    with pytest.raises(IncorrectUnits):
        assert q1 - q3

    ft = Quantity(1, "ft")
    m = Quantity(1, "m")
    mm = Quantity(1, "mm")

    assert m - ft == Quantity(0.6952, "m")
    assert ft - m == Quantity(-2.280839895013124, "ft")
    assert m - mm == Quantity(0.999, "m")
    assert mm - m == Quantity(-999, "mm")

    r = Quantity(10.0, "")
    r2 = Quantity(5.0, "")
    r3 = r - 2  # pyright: ignore[reportOperatorIssue, reportUnknownVariableType]  # this won't raise but I don't think this is recommended  # fmt: skip
    assert r3.value == 8
    assert r3.units == Unit("")

    r4 = r - r2
    assert r4.value == 5.0
    assert r4.units == Unit("")

    with pytest.raises(IncorrectUnits):
        m - 5  # pyright: ignore[reportOperatorIssue, reportUnusedExpression]  # fmt: skip


def test_reverse_subtraction():
    q1 = Quantity(5.0)
    q2 = 2 - q1  # pyright: ignore[reportOperatorIssue, reportUnknownVariableType]  # fmt: skip

    assert q2.value == -3

    r = Quantity(5.0, "")
    r2 = 10 - r  # pyright: ignore[reportOperatorIssue, reportUnknownVariableType]  # fmt: skip
    assert r2.value == 5
    assert r2.units == Unit("")

    m = Quantity(1, "m")
    with pytest.raises(IncorrectUnits):
        5 - m  # pyright: ignore[reportOperatorIssue, reportUnusedExpression]  # fmt: skip


def test_temp_subtraction():
    dims = BaseDimensions
    t1 = Quantity(1.0, "K")
    assert get_si_value(t1) == 1.0

    t2 = Quantity(2.0, "K")
    assert get_si_value(t2) == 2.0

    dt1 = t2 - t1
    assert get_si_value(dt1) == 1.0
    assert dt1.dimensions == Dimensions({dims.TEMPERATURE_DIFFERENCE: 1.0})

    t3 = Quantity(1.0, "C")
    assert get_si_value(t3) == 274.15

    t4 = Quantity(2.0, "C")
    assert get_si_value(t4) == 275.15

    dt2 = t4 - t3
    assert get_si_value(dt2) == 1.0
    assert dt2.dimensions == Dimensions({dims.TEMPERATURE_DIFFERENCE: 1.0})

    t5 = Quantity(10.0, "delta_F")
    t6 = t5 - t4
    assert t6 == Quantity(-25.600000000000023, "F")


def test_pow():
    q1 = Quantity(10.0, "m s^-1")
    q2 = Quantity(5.0, "ft")

    q1_sq = q1**2
    assert q1_sq.units == Unit("m^2 s^-2")
    assert q1_sq.value == 100
    q2_sq = q2**2
    assert q2_sq.units == Unit("ft^2")
    assert get_si_value(q2_sq) == pytest.approx(2.3225759999999993, DELTA)

    assert get_si_value(q1) ** 2 == 100.0
    assert get_si_value(q2) ** 2 == pytest.approx(2.3225759999999993, DELTA)


def test_mul():
    q1 = Quantity(10.0, "m s^-1")
    q2 = Quantity(5.0, "ft")
    u1 = Unit("kg")

    q3 = q1 * q2
    assert q3.units == Unit("m s^-1 ft")
    assert get_si_value(q3) == pytest.approx(15.239999999999998, DELTA)

    q4 = q1 * u1
    assert q4.units == Unit("kg m s^-1")
    assert q4.value == pytest.approx(10, DELTA)

    q5 = q2 * 3
    assert q5.units == Unit("ft")
    assert get_si_value(q5) == pytest.approx(4.571999999999999, DELTA)

    assert get_si_value(1.225 * kg / m**3 * [1, 2, 3] * m) == pytest.approx(
        [1.225, 2.45, 3.675],
        DELTA,
    )

    r1 = Quantity(10.0, "")
    r2 = Quantity(5.0, "")

    r3 = r1 * 3
    assert r3.value == 30.0
    assert r3.units == Unit("")

    r4 = r1 * r2
    assert r4.value == 50.0
    assert r4.units == Unit("")

    result = q1 * 2
    assert result.units == Unit("m s^-1")


def test_reverse_mul():
    q1 = Quantity(10.0, "m s^-1")
    u1 = Unit("kg")

    q3 = u1 * q1
    assert q3.units == Unit("m s^-1 kg")
    assert q3.value == pytest.approx(10, DELTA)

    r = Quantity(10.0, "")
    r2 = 3 * r
    assert r2.value == 30.0
    assert r2.units == Unit("")

    result = 2 * q1
    assert result.units == Unit("m s^-1")


def test_neg():
    q0 = Quantity(10.0, "m s^-1")
    q1 = -q0
    assert q1.value == -10.0
    assert q1.units == Unit("m s^-1")

    r = Quantity(10.0, "")
    r_neg = -r
    assert r_neg.value == -10.0
    assert r_neg.units == Unit("")


def test_ne():
    x = Quantity(10.5, "cm")
    y = Quantity(10.5, "m")
    z = Quantity(10.5, "g")
    r = Quantity(10.5, "")

    assert y != x
    assert x != y

    assert r != 0.5
    assert 0.5 != r


def test_eq():
    x = Quantity(10.5, "cm")
    y = Quantity(10.5, "m")
    r = Quantity(10.5, "")

    l = Quantity(10.5, "cm")
    m = Quantity(10.5, "kg")

    n = Quantity(10.5, "")

    assert x == l
    assert r == n
    assert r == 10.5

    with pytest.raises(IncompatibleQuantities):
        assert x == 0.5

    with pytest.raises(IncompatibleDimensions):
        assert m == y
        assert x == 0.5


def test_div():
    q1 = Quantity(10.0, "m s^-1")
    q2 = Quantity(5.0, "m s^-1")

    result = q1 / q2
    assert result.value == pytest.approx(2.0, DELTA)
    assert result.units == Unit("")

    q3 = Quantity(10.0, "m")
    q4 = Quantity(5.0, "s")
    result2 = q3 / q4
    assert result2.units == Unit("m s^-1")

    r1 = Quantity(20.0, "")
    r2 = Quantity(5.0, "")
    r3 = r1 / r2
    assert r3.value == 4.0
    assert r3.units == Unit("")

    r4 = r1 / 2
    assert r4.value == 10.0
    assert r4.units == Unit("")

    q5 = Quantity(10.0, "m")
    result3 = q5 / 2
    assert result3.value == 5.0
    assert result3.units == Unit("m")


def test_rdiv():
    q1 = Quantity(10.0, "m s^-1")

    q2 = 50 / q1
    assert q2.value == 5
    assert q2.units == Unit("m^-1 s")

    r = Quantity(5.0, "")
    r2 = 20 / r
    assert r2.value == 4.0
    assert r2.units == Unit("")

    m = Quantity(2.0, "m")
    result = 10 / m
    assert result.units == Unit("m^-1")


def test_dimensionless_div():
    length_1 = Quantity(50, "mm")
    length_2 = Quantity(40, "inch")
    result = length_1 / length_2
    assert result.value == 1.25
    assert result.units == Unit("mm inch^-1")

    r1 = Quantity(100.0, "")
    r2 = Quantity(25.0, "")
    result2 = r1 / r2
    assert result2.value == 4.0
    assert result2.units == Unit("")


def test_quantity_divided_by_unit():
    dims = BaseDimensions
    ur = UnitRegistry()
    mass = Quantity(10.0, ur.kg)
    mass_flow_rate = mass / ur.s
    assert mass_flow_rate.units == Unit("kg s^-1")
    assert mass_flow_rate.value == 10
    assert mass_flow_rate.dimensions == Dimensions({dims.MASS: 1.0, dims.TIME: -1.0})


def test_quantity_divided_by_number():
    ur = UnitRegistry()
    mass = Quantity(10.0, ur.kg)
    half_m = mass / 2
    assert half_m.units == Unit("kg")
    assert half_m.value == 5


def test_exponent():
    qt = Quantity(5.0, "m^0")
    qtm = qt**2

    assert qtm.value == 25.0
    assert qtm.dimensions == Dimensions()
    assert qtm.units == Unit("")


def test_addition():
    q1 = Quantity(5.0, "m^0")
    q3 = Quantity(52, "N")

    q2 = q1 + 5  # pyright: ignore[reportOperatorIssue, reportUnknownVariableType]  # this won't raise but I don't think this is recommended  # fmt: skip
    assert q2.units == Unit()
    assert q2.value == 10

    with pytest.raises(IncorrectUnits) as e_info:
        q1 - q3

    ft = Quantity(1, "ft")
    m = Quantity(1, "m")
    mm = Quantity(1, "mm")

    assert m + ft == Quantity(1.3048, "m")
    assert ft + m == Quantity(4.2808398950131235, "ft")
    assert m + mm == Quantity(1.001, "m")
    assert mm + m == Quantity(1001, "mm")

    r = Quantity(5.0, "")
    r2 = r + 5  # pyright: ignore[reportOperatorIssue, reportUnknownVariableType]  # this won't raise but I don't think this is recommended  # fmt: skip
    assert r2.units == Unit("")
    assert r2.value == 10

    q1 = Quantity(5.0, "m^0")

    assert (q1 + 5).value == 10  # pyright: ignore[reportOperatorIssue]  # fmt: skip

    assert q1 + [1, 2, 3] == Quantity([6, 7, 8])  # pyright: ignore[reportOperatorIssue]  # fmt: skip

    with pytest.raises(IncorrectUnits):
        m + 5  # pyright: ignore[reportOperatorIssue, reportUnusedExpression]  # fmt: skip


def test_reverse_addition():
    q1 = Quantity(5.0, "m^0")

    q2 = 5 + q1  # pyright: ignore[reportOperatorIssue, reportUnknownVariableType]  # fmt: skip
    assert q2.units == Unit()
    assert q2.value == 10

    assert (5 + q1).value == 10  # pyright: ignore[reportOperatorIssue]  # fmt: skip

    assert [1, 2, 3] + q1 == Quantity([6, 7, 8])  # pyright: ignore[reportOperatorIssue]  # fmt: skip

    r = Quantity(5.0, "")
    r2 = 5 + r  # pyright: ignore[reportOperatorIssue, reportUnknownVariableType]  # this won't raise but I don't think this is recommended  # fmt: skip
    assert r2.units == Unit("")
    assert r2.value == 10

    m = Quantity(1, "m")
    with pytest.raises(IncorrectUnits):
        5 + m  # pyright: ignore[reportOperatorIssue, reportUnusedExpression]  # fmt: skip


def test_ge():
    x = Quantity(10.5, "cm")
    y = Quantity(10.5, "m")
    z = Quantity(10.5, "g")
    r = Quantity(10.5, "")
    r2 = Quantity(7.8, "")

    assert y >= x
    assert 15.7 >= r
    assert r >= 7.8
    assert r >= r2
    assert r2 <= r

    with pytest.raises(IncompatibleDimensions) as e_info:
        assert x >= z

    with pytest.raises(IncompatibleQuantities) as e_info:
        assert x >= 5.0

    with pytest.raises(IncompatibleQuantities):
        5.0 >= x  # pyright: ignore[reportUnusedExpression, reportOperatorIssue]  # fmt: skip


def test_gt():
    x = Quantity(10.5, "cm")
    y = Quantity(10.5, "m")
    z = Quantity(10.5, "g")
    r = Quantity(10.5, "")
    r2 = Quantity(7.8, "")

    assert y > x
    assert 15.7 > r
    assert r > 7.8
    assert r > r2

    with pytest.raises(IncompatibleDimensions) as e_info:
        assert x > z

    with pytest.raises(IncompatibleQuantities) as e_info:
        assert x > 5.0

    with pytest.raises(IncompatibleQuantities):
        5.0 > x  # pyright: ignore[reportUnusedExpression, reportOperatorIssue]  # fmt: skip


def test_lt():
    x = Quantity(10.5, "cm")
    y = Quantity(10.5, "m")
    z = Quantity(10.5, "g")
    r = Quantity(10.5, "")
    r2 = Quantity(15.7, "")

    assert x < y
    assert r < 15.7
    assert 7.8 < r
    assert r < r2

    with pytest.raises(IncompatibleDimensions) as e_info:
        assert z < x

    with pytest.raises(IncompatibleQuantities) as e_info:
        assert x < 5.0

    with pytest.raises(IncompatibleQuantities):
        5.0 < x  # pyright: ignore[reportUnusedExpression, reportOperatorIssue]  # fmt: skip


def test_le():
    x = Quantity(10.5, "cm")
    y = Quantity(10.5, "m")
    z = Quantity(10.5, "g")
    r = Quantity(10.5, "")
    r2 = Quantity(15.7, "")

    assert x <= y
    assert r <= 15.7
    assert 7.8 <= r
    assert r <= r2

    with pytest.raises(IncompatibleDimensions) as e_info:
        assert z <= x

    with pytest.raises(IncompatibleQuantities) as e_info:
        assert x <= 5.0

    with pytest.raises(IncompatibleQuantities):
        5.0 <= x  # pyright: ignore[reportUnusedExpression, reportOperatorIssue]  # fmt: skip


def test_temp():
    k = Quantity(-40, "K")

    kc = k.to("delta_C")
    assert kc.value == pytest.approx(-40.0, DELTA)
    assert kc.units == Unit("delta_C")

    kc = k.to("delta_R")
    assert kc.value == pytest.approx(-72.0, DELTA)
    assert kc.units == Unit("delta_R")

    kc = k.to("delta_F")
    assert kc.value == pytest.approx(-72.0, DELTA)
    assert kc.units == Unit("delta_F")


def test_temp_addition():
    t1 = Quantity(150.0, "C")
    t2 = Quantity(50.0, "C")
    df = Quantity(50.0, "delta_F")
    k = Quantity(50.0, "K")

    td = t1 - t2
    assert td.units == Unit("delta_K")
    assert get_si_value(td) == 100.0

    t3 = df + k
    assert t3.value == pytest.approx(-319.6699999991, DELTA)
    assert t3.units == Unit("F")

    t4 = k + df
    assert t4.value == pytest.approx(77.7777777775, DELTA)
    assert t4.units == Unit("K")

    t5 = df + df
    assert t5 == Quantity(100, "delta_F")

    with pytest.raises(ProhibitedTemperatureOperation):
        t1 + t2


def test_quantity_from_dimensions():
    dims = BaseDimensions
    p = Quantity(
        10.5,
        dimensions=Dimensions({dims.MASS: 1.0, dims.LENGTH: -1.0, dims.TIME: -2.0}),
    )
    assert p.units == Unit("kg m^-1 s^-2")


def test_quantity_table():
    quantity_dict_from_settings_API = {
        "Mass": 1,
        "Velocity": 2.5,
        "Current": 3,
        "Light": 1,
        "HeatTransferCoefficient": 2,
    }

    api_test = Quantity(10.5, quantity_table=quantity_dict_from_settings_API)
    assert api_test.value == 10.5
    assert api_test.units == Unit("kg m^-1.5 s^-2.5 A^3 cd W^2 K^-2")


def testing_units_to_dimensions(monkeypatch):
    monkeypatch.setenv("PYANSYS_UNITS_ANGLE_AS_DIMENSION", "1")
    print(f"{'*' * 25} {testing_units_to_dimensions.__name__} {'*' * 25}")
    dims = BaseDimensions

    def dim_test(units, dim_dict):
        qt = Quantity(10, units)
        print(f"{units} : {qt.dimensions}")
        assert qt.dimensions == Dimensions(dim_dict)

    dim_test("m", {dims.LENGTH: 1.0})
    dim_test("m s^-1", {dims.LENGTH: 1.0, dims.TIME: -1.0})
    dim_test("kg m s^-2 m^-2", {dims.MASS: 1.0, dims.LENGTH: -1.0, dims.TIME: -2.0})
    dim_test("Pa", {dims.MASS: 1.0, dims.LENGTH: -1.0, dims.TIME: -2.0})
    dim_test("kPa", {dims.MASS: 1.0, dims.LENGTH: -1.0, dims.TIME: -2.0})
    dim_test("Pa^2", {dims.MASS: 2.0, dims.LENGTH: -2.0, dims.TIME: -4.0})
    dim_test("daPa", {dims.MASS: 1.0, dims.LENGTH: -1.0, dims.TIME: -2.0})
    dim_test("MPa", {dims.MASS: 1.0, dims.LENGTH: -1.0, dims.TIME: -2.0})
    dim_test("kPa^2", {dims.MASS: 2.0, dims.LENGTH: -2.0, dims.TIME: -4.0})
    dim_test("slug inch^-1 s^-1", {dims.MASS: 1.0, dims.LENGTH: -1.0, dims.TIME: -1.0})
    dim_test("radian", {dims.ANGLE: 1.0})
    dim_test(
        "ohm", {dims.MASS: 1.0, dims.LENGTH: 2.0, dims.TIME: -3.0, dims.CURRENT: -2.0}
    )
    dim_test("lb cm s^-2", {dims.MASS: 1.0, dims.LENGTH: 1.0, dims.TIME: -2.0})
    print("-" * 75)


def testing_multipliers():
    print(f"{'*' * 25} {testing_multipliers.__name__} {'*' * 25}")

    def from_to(from_str, to_str):
        qt = Quantity(1, from_str)
        to = qt.to(to_str)
        print(f"from {qt} -> to {to}")

    from_to("mm", "cm")
    from_to("m", "ft")
    from_to("dm^3", "m^3")
    from_to("m s^-1", "cm s^-1")
    from_to("N", "dyne")
    from_to("m^2", "inch^2")
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
    dims = BaseDimensions
    with pytest.raises(ExcessiveParameters):
        e1 = Quantity(
            value=10,
            units="farad",
            dimensions=Dimensions({dims.MASS: 1}),
            quantity_table={"Velocity": 3},
        )
    with pytest.raises(InsufficientArguments):
        e2 = Quantity()


def test_incompatible_dimensions_error():
    ur = UnitRegistry()
    with pytest.raises(IncompatibleDimensions):
        e1 = Quantity(7, ur.kg).to(ur.ft)


def test_error_messages():
    e1 = ExcessiveParameters()
    assert (
        str(e1)
        == "Quantity only accepts one of the following parameters: \
            (units) or (quantity_table) or (dimensions)."
    )

    e2 = IncompatibleDimensions(Unit("mm"), Unit("K"))
    assert str(e2) == "`mm` and `K` have incompatible dimensions."

    e3 = IncompatibleValue("radian")
    assert str(e3) == "`radian` is incompatible with the current quantity object."

    e4 = RequiresUniqueDimensions(Unit("mm"), Unit("m"))
    assert str(e4) == "For 'mm' to be added 'm' must be removed."


def test_value_as_string():
    with pytest.raises(TypeError):
        q = Quantity("string", "m")


def test_C_to_F():
    ureg = UnitRegistry()
    five_c = Quantity(value=5.0, units=ureg.C)
    converted = five_c.to(ureg.F)
    assert converted.value == 41.0
    assert converted.units._name == "F"


def _supporting_matplotlib():
    try:
        import matplotlib  # noqa: F401
    except ImportError:
        return False
    return True


def test_matplotlib_integration():
    if not _supporting_matplotlib():
        return
    import matplotlib.pyplot as plt

    arr_x = Quantity([1, 2, 3], Unit("m"))
    arr_y = Quantity([4, 5, 6], "kg")
    fig, ax = plt.subplots()
    ax.plot(arr_x, arr_y)
    assert ax.xaxis.get_units() == "m"
    assert ax.yaxis.get_units() == "kg"


def test_temperature_list():
    temp = Quantity(value=[1.0, 2.0, 3.0], units="C")
    assert temp.value.tolist() == [1.0, 2.0, 3.0]
    assert temp.units == Unit("C")
