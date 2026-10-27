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
"""Tests for the NumPy ``__array_ufunc__`` and ``__array_function__`` protocols."""

from collections.abc import Callable
from typing import Any

import pytest

np = pytest.importorskip("numpy")

from ansys.units import Quantity, Unit  # noqa: E402
from ansys.units.quantity import (  # noqa: E402
    DimensionlessArgumentRequired,
    IncompatibleDimensions,
)
from ansys.units.unit import (  # noqa: E402
    IncorrectUnits,
    ProhibitedOffsetUnitOperation,
    ProhibitedTemperatureOperation,
)


def _same(q: Quantity, values: Any, units: str) -> bool:
    return q.units == Unit(units) and np.allclose(q.value, values)


# ---------------------------------------------------------------------------
# Trigonometric, exponential and logarithmic ufuncs
# ---------------------------------------------------------------------------


def test_trig_accepts_angle_units():
    angle = Quantity(np.array([0.0, 90.0, 180.0]), "degree")
    for func, expected in (
        (np.sin, [0.0, 1.0, 0.0]),
        (np.cos, [1.0, 0.0, -1.0]),
    ):
        result = func(angle)
        assert result.is_dimensionless
        assert np.allclose(result.value, expected, atol=1e-12)

    assert np.tan(Quantity(45.0, "degree")).value == pytest.approx(1.0)
    assert np.sin(Quantity(np.pi / 2, "radian")).value == pytest.approx(1.0)


def test_trig_rejects_dimensional_quantities():
    with pytest.raises(DimensionlessArgumentRequired, match="sin"):
        np.sin(Quantity(1.0, "m"))


def test_inverse_trig_returns_radians():
    result = np.arccos(Quantity(np.array([1.0, 0.0]), ""))
    assert _same(result, [0.0, np.pi / 2], "radian")
    assert np.arctan(1.0 * Unit("")).value == pytest.approx(np.pi / 4)

    with pytest.raises(DimensionlessArgumentRequired):
        np.arcsin(Quantity(1.0, "m"))


def test_arctan2_requires_matching_units():
    result = np.arctan2(Quantity(1.0, "m"), Quantity(100.0, "cm"))
    assert _same(result, np.pi / 4, "radian")
    with pytest.raises(IncompatibleDimensions):
        np.arctan2(Quantity(1.0, "m"), Quantity(1.0, "s"))


@pytest.mark.parametrize("func", [np.exp, np.log, np.log10, np.expm1, np.tanh])
def test_dimensionless_functions(func: Callable[..., Any]):
    q = Quantity(np.array([1.0, 2.0]), "")
    result = func(q)
    assert result.is_dimensionless
    assert np.allclose(result.value, func(q.value))

    with pytest.raises(DimensionlessArgumentRequired):
        func(Quantity(np.array([1.0, 2.0]), "kg"))


# ---------------------------------------------------------------------------
# Arithmetic ufuncs
# ---------------------------------------------------------------------------


def test_sqrt_square_cbrt_reciprocal_units():
    assert _same(np.sqrt(Quantity(9.0, "m^2")), 3.0, "m")
    assert _same(np.square(Quantity(3.0, "m s^-1")), 9.0, "m^2 s^-2")
    assert _same(np.cbrt(Quantity(8.0, "m^3")), 2.0, "m")
    assert _same(np.reciprocal(Quantity(4.0, "s")), 0.25, "s^-1")


def test_power_scalar_exponent():
    assert _same(np.power(Quantity(2.0, "m"), 3), 8.0, "m^3")
    assert _same(np.power(Quantity(np.array([1.0, 2.0]), "m"), 2.0), [1, 4], "m^2")
    with pytest.raises(ValueError, match="scalar exponent"):
        np.power(Quantity(2.0, "m"), np.array([1.0, 2.0]))
    # dimensionless base accepts array exponents
    assert np.allclose(
        np.power(Quantity(2.0, ""), np.array([1.0, 2.0])).value, [2.0, 4.0]
    )
    with pytest.raises(DimensionlessArgumentRequired):
        np.power(Quantity(2.0, "m"), Quantity(2.0, "s"))


def test_add_subtract_convert_units():
    a = Quantity(np.array([1.0, 2.0]), "m")
    b = Quantity(np.array([100.0, 100.0]), "cm")
    assert _same(np.add(a, b), [2.0, 3.0], "m")
    assert _same(np.subtract(a, b), [0.0, 1.0], "m")
    with pytest.raises(Exception):
        np.add(a, Quantity(np.array([1.0, 1.0]), "s"))


def test_multiply_divide_units():
    a = Quantity(np.array([1.0, 2.0]), "m")
    b = Quantity(np.array([2.0, 4.0]), "s")
    assert _same(np.multiply(a, b), [2.0, 8.0], "m s")
    assert _same(np.divide(a, b), [0.5, 0.5], "m s^-1")
    assert _same(np.multiply(a, 3.0), [3.0, 6.0], "m")
    assert _same(np.divide(1.0, b), [0.5, 0.25], "s^-1")


def test_ndarray_on_left_hand_side_keeps_units():
    q = Quantity(2.0, "m")
    result = np.array([1.0, 2.0]) * q
    assert isinstance(result, Quantity)
    assert _same(result, [2.0, 4.0], "m")
    assert _same(np.float64(3.0) * q, 6.0, "m")


def test_comparisons_convert_units():
    a = Quantity(np.array([1.0, 2.0]), "m")
    b = Quantity(np.array([150.0, 150.0]), "cm")
    assert np.array_equal(np.less(a, b), [True, False])
    assert np.array_equal(np.greater_equal(a, b), [False, True])
    with pytest.raises(IncompatibleDimensions):
        np.less(a, Quantity(1.0, "s"))


def test_unary_same_units_and_plain_results():
    q = Quantity(np.array([-1.5, 2.5, np.nan]), "m")
    absolute = np.absolute(q)
    assert absolute.units == Unit("m")
    assert np.allclose(absolute.value, [1.5, 2.5, np.nan], equal_nan=True)
    assert np.array_equal(np.isnan(q), [False, False, True])
    assert _same(np.floor(Quantity(np.array([1.5, -1.5]), "m")), [1.0, -2.0], "m")
    assert np.sign(Quantity(-2.0, "m")).value == -1.0


def test_maximum_minimum_convert_units():
    a = Quantity(np.array([1.0, 3.0]), "m")
    b = Quantity(np.array([200.0, 200.0]), "cm")
    assert _same(np.maximum(a, b), [2.0, 3.0], "m")
    assert _same(np.minimum(a, b), [1.0, 2.0], "m")


def test_unsupported_ufunc_raises_type_error():
    with pytest.raises(TypeError):
        np.logaddexp(Quantity(1.0, "m"), Quantity(1.0, "m"))


_UNSUPPORTED_OPERATIONS: list[Callable[[Any], Any]] = [
    lambda q: np.multiply.reduce(q),  # unsupported reduction
    lambda q: np.add.outer(q, q),  # unsupported ufunc method
    lambda q: np.add(q, q, where=np.array([True, False])),  # unsupported kwarg
    lambda q: np.spacing(q),  # unsupported unary ufunc
    lambda q: np.prod(q),  # unsupported array function
    lambda q: np.mean(q.value, out=q),  # quantity passed as ``out``
]


@pytest.mark.parametrize("operation", _UNSUPPORTED_OPERATIONS)
def test_unsupported_numpy_operations_raise_type_error(
    operation: Callable[[Any], Any],
):
    with pytest.raises(TypeError):
        operation(Quantity(np.array([1.0, 2.0]), "m"))


_PLAIN = np.array([1.0, 2.0])

_MISPLACED_QUANTITY_OPERATIONS: list[Callable[[Any], Any]] = [
    lambda q: np.percentile(_PLAIN, q),
    lambda q: np.diff(_PLAIN, prepend=q),
    lambda q: np.var(_PLAIN, mean=q),
    lambda q: np.atleast_1d(q, q),
    lambda q: np.clip(_PLAIN, q, q),
    lambda q: np.where(q),
    lambda q: np.where(q, _PLAIN, _PLAIN),
    lambda q: np.linspace(0.0, q),
]


@pytest.mark.parametrize("operation", _MISPLACED_QUANTITY_OPERATIONS)
def test_quantity_in_unsupported_argument_position_raises_type_error(
    operation: Callable[[Any], Any],
):
    # The quantity isn't in the position whose units define the result.
    with pytest.raises(TypeError):
        operation(Quantity(np.array([1.0, 0.0]), ""))


def test_quantity_divided_by_array():
    result = Quantity(np.array([2.0, 4.0]), "m") / np.array([2.0, 4.0])
    assert _same(result, [1.0, 1.0], "m")


def test_empty_results():
    assert np.diff(Quantity(np.array([1.0]), "m")).size == 0
    assert _same(np.sum(Quantity(np.array([]), "m")), 0.0, "m")
    empty_c = Quantity(np.array([]), "C")
    assert np.concatenate([empty_c, Quantity(np.array([1.0]), "C")]).value.tolist() == [
        1.0
    ]
    assert np.sqrt(Quantity(np.array([]), "m^2")).units == Unit("m")


def test_out_argument_is_unsupported():
    with pytest.raises(TypeError):
        np.sqrt(Quantity(4.0, "m^2"), out=np.empty(()))


# ---------------------------------------------------------------------------
# Reductions and array functions
# ---------------------------------------------------------------------------


def test_reductions_preserve_units():
    q = Quantity(np.array([1.0, 2.0, 3.0, 6.0]), "m")
    assert _same(np.sum(q), 12.0, "m")
    assert _same(np.mean(q), 3.0, "m")
    assert _same(np.median(q), 2.5, "m")
    assert _same(np.max(q), 6.0, "m")
    assert _same(np.min(q), 1.0, "m")
    assert _same(np.cumsum(q), [1.0, 3.0, 6.0, 12.0], "m")
    assert _same(np.ptp(q), 5.0, "m")
    assert _same(np.diff(q), [1.0, 1.0, 3.0], "m")
    assert _same(np.std(q), np.std(q.value), "m")
    assert _same(np.var(q), np.var(q.value), "m^2")
    assert np.argmax(q) == 3


def test_reduce_methods():
    q = Quantity(np.array([1.0, 2.0, 3.0]), "kg")
    assert _same(np.add.reduce(q), 6.0, "kg")
    assert _same(np.maximum.accumulate(q), [1.0, 2.0, 3.0], "kg")


def test_multidimensional_arrays():
    q = Quantity([[0.0, 1.0, 2.0], [3.0, 4.0, 5.0]], "m")
    assert q.value.shape == (2, 3)
    assert _same(np.sum(q, axis=0), [3.0, 5.0, 7.0], "m")
    assert _same(np.mean(q), 2.5, "m")
    assert _same(np.sqrt(Quantity(np.ones((2, 2)) * 4, "m^2")), np.full((2, 2), 2), "m")
    assert np.shape(q) == (2, 3)
    assert _same(np.transpose(q), q.value.T, "m")
    assert _same(np.reshape(q, (3, 2)), q.value.reshape(3, 2), "m")


def test_shape_properties_and_slicing():
    q = Quantity([[0.0, 1.0, 2.0], [3.0, 4.0, 5.0]], "m")
    assert (q.shape, q.ndim, q.size) == ((2, 3), 2, 6)
    assert Quantity(1.0, "m").shape == ()
    assert _same(q[0], [0.0, 1.0, 2.0], "m")
    assert _same(q[:, 1], [1.0, 4.0], "m")
    assert q[1, 2].value == 5.0


def test_concatenate_and_stack_convert_units():
    a = Quantity(np.array([1.0, 2.0]), "m")
    b = Quantity(np.array([300.0]), "cm")
    assert _same(np.concatenate([a, b]), [1.0, 2.0, 3.0], "m")
    assert _same(np.stack([a, a]), [[1.0, 2.0], [1.0, 2.0]], "m")
    assert _same(np.hstack([a, a]), [1.0, 2.0, 1.0, 2.0], "m")


def test_clip_converts_limits():
    q = Quantity(np.array([0.5, 1.5, 3.0]), "m")
    result = np.clip(q, Quantity(100.0, "cm"), Quantity(2.0, "m"))
    assert _same(result, [1.0, 1.5, 2.0], "m")


def test_where_and_comparison_functions():
    a = Quantity(np.array([1.0, 2.0]), "m")
    b = Quantity(np.array([300.0, 100.0]), "cm")
    cond = np.array([True, False])
    assert _same(np.where(cond, a, b), [1.0, 1.0], "m")
    result = np.where(cond, a, np.nan)
    assert result.value[0] == 1.0 and np.isnan(result.value[1])
    with pytest.raises(IncompatibleDimensions):
        np.where(cond, a, 5.0)
    assert np.allclose(a, Quantity(np.array([100.0, 200.0]), "cm"))
    assert np.array_equal(a, Quantity(np.array([100.0, 200.0]), "cm"))
    assert np.isclose(a, b).tolist() == [False, False]


def test_dot_and_norm():
    a = Quantity(np.array([3.0, 4.0]), "m")
    b = Quantity(np.array([1.0, 2.0]), "s")
    assert _same(np.dot(a, b), 11.0, "m s")
    assert _same(np.linalg.norm(a), 5.0, "m")


def test_linspace_converts_stop_units():
    result = np.linspace(Quantity(0.0, "m"), Quantity(200.0, "cm"), 3)
    assert _same(result, [0.0, 1.0, 2.0], "m")


def test_unsupported_function_raises_type_error():
    with pytest.raises(TypeError):
        np.prod(Quantity(np.array([1.0, 2.0]), "m"))


# ---------------------------------------------------------------------------
# Temperatures
# ---------------------------------------------------------------------------


def test_temperature_semantics_in_numpy_functions():
    t = Quantity(np.array([10.0, 20.0, 40.0]), "C")
    assert _same(np.mean(t), 70.0 / 3.0, "C")
    assert _same(np.max(t), 40.0, "C")
    assert _same(np.ptp(t), 30.0, "delta_C")
    assert _same(np.diff(t), [10.0, 20.0], "delta_C")
    assert _same(np.std(t), np.std(t.value), "delta_C")

    with pytest.raises(ProhibitedTemperatureOperation):
        np.sum(t)
    with pytest.raises(ProhibitedTemperatureOperation):
        np.add(t, t)
    with pytest.raises(ProhibitedOffsetUnitOperation):
        np.multiply(t, 2.0)
    with pytest.raises(ProhibitedOffsetUnitOperation):
        np.sqrt(t)


def test_temperature_subtract_and_compare():
    t1 = Quantity(np.array([20.0, 30.0]), "C")
    t2 = Quantity(np.array([293.15, 293.15]), "K")
    assert _same(np.subtract(t1, t2), [0.0, 10.0], "delta_C")
    assert np.array_equal(np.greater(t1, t2), [False, True])


def test_ratio_scale_temperatures_support_arithmetic():
    k = Quantity(np.array([100.0, 200.0]), "K")
    assert _same(np.multiply(k, 2.0), [200.0, 400.0], "K")
    assert _same(np.sqrt(Quantity(np.array([4.0, 9.0]), "K^2")), [2.0, 3.0], "K")


def test_offset_units_rejected_by_multiplicative_numpy_functions():
    c = Quantity(np.array([10.0, 20.0]), "C")
    m = Quantity(np.array([1.0, 2.0]), "m")
    for operation in (
        lambda: np.divide(1.0, c),
        lambda: np.divide(m, c),
        lambda: np.multiply(3.0, c),
        lambda: np.float64(2.0) * Quantity(1.0, "C"),
        lambda: np.hypot(c, c),
        lambda: np.dot(c, m),
        lambda: np.linalg.norm(c),
        lambda: np.square(c),
        lambda: np.power(c, 2),
    ):
        with pytest.raises(ProhibitedOffsetUnitOperation):
            operation()

    with pytest.raises(ProhibitedOffsetUnitOperation, match="'/'"):
        np.divide(1.0, c)


def test_absolute_temperatures_cannot_be_accumulated():
    c = Quantity(np.array([10.0, 20.0]), "C")
    for operation in (
        lambda: np.add.reduce(c),
        lambda: np.add.accumulate(c),
        lambda: np.nansum(c),
        lambda: np.cumsum(c),
    ):
        with pytest.raises(ProhibitedTemperatureOperation):
            operation()
    assert _same(np.sum(Quantity(np.array([1.0, 2.0]), "delta_C")), 3.0, "delta_C")
    assert _same(np.var(c), np.var(c.value), "delta_C^2")


# ---------------------------------------------------------------------------
# Mixed operands, keyword arguments and less common paths
# ---------------------------------------------------------------------------


def test_plain_arrays_combine_with_quantities():
    assert _same(np.array([2.0, 4.0]) / Quantity(2.0, "s"), [1.0, 2.0], "s^-1")
    assert _same(np.array([2.0, 4.0]) + Quantity(2.0, ""), [4.0, 6.0], "")
    assert np.array_equal(np.array([2.0, 4.0]) < Quantity(3.0, ""), [True, False])
    with pytest.raises(IncorrectUnits):
        _ = np.array([2.0, 4.0]) + Quantity(2.0, "m")
    with pytest.raises(IncompatibleDimensions):
        np.equal(Quantity(np.array([1.0]), "m"), 1.0)


def test_matmul_and_atleast_1d():
    a = Quantity(np.array([3.0, 4.0]), "m")
    assert _same(np.matmul(a, a), 25.0, "m^2")
    assert _same(np.atleast_1d(Quantity(2.0, "m")), [2.0], "m")


def test_matmul_operator():
    matrix = Quantity([[1.0, 2.0], [3.0, 4.0]], "m")
    vector = Quantity([1.0, 1.0], "N")
    assert _same(matrix @ vector, [3.0, 7.0], "m N")
    assert _same(matrix @ matrix, [[7.0, 10.0], [15.0, 22.0]], "m^2")
    assert _same(vector @ vector, 2.0, "N^2")

    # Plain operands are dimensionless, on either side.
    assert _same(matrix @ [1.0, 2.0], [5.0, 11.0], "m")
    assert _same([1.0, 2.0] @ matrix, [7.0, 10.0], "m")
    assert _same(matrix @ np.array([1.0, 2.0]), [5.0, 11.0], "m")
    assert _same(np.array([1.0, 2.0]) @ matrix, [7.0, 10.0], "m")

    # Same result as np.matmul.
    assert _same(matrix @ vector, np.matmul(matrix, vector).value, "m N")


def test_matmul_operator_errors():
    vector = Quantity([1.0, 2.0], "m")
    with pytest.raises(ProhibitedOffsetUnitOperation):
        _ = Quantity([1.0, 2.0], "C") @ vector
    with pytest.raises(ProhibitedOffsetUnitOperation):
        _ = vector @ Quantity([1.0, 2.0], "F")
    with pytest.raises(ProhibitedOffsetUnitOperation):
        _ = [1.0, 2.0] @ Quantity([1.0, 2.0], "C")
    with pytest.raises(ValueError):
        _ = vector @ Quantity([1.0, 2.0, 3.0], "m")  # shape mismatch
    with pytest.raises(ValueError):
        _ = Quantity(2.0, "m") @ vector  # scalar operand
    for other in ("ab", 2.0, Unit("m"), object()):
        with pytest.raises(TypeError):
            _ = vector @ other
    with pytest.raises(TypeError):
        _ = "ab" @ vector


def test_value_preserving_functions():
    q = Quantity(np.array([3.0, 1.0, np.nan, 2.0]), "s")
    assert _same(np.nanmean(q), 2.0, "s")
    assert _same(np.nanmax(q), 3.0, "s")
    finite = Quantity(np.array([3.0, 1.0, 2.0]), "s")
    assert _same(np.sort(finite), [1.0, 2.0, 3.0], "s")
    assert _same(np.percentile(finite, 50), 2.0, "s")
    assert _same(np.round(Quantity(np.array([1.234]), "s"), 1), [1.2], "s")
    assert np.argsort(finite).tolist() == [1, 2, 0]


def test_keyword_arguments():
    m = Quantity(np.array([3.0, 4.0]), "m")
    assert _same(np.clip(m, min=Quantity(350.0, "cm"), max=None), [3.5, 4.0], "m")
    assert _same(
        np.linspace(start=Quantity(0.0, "m"), stop=Quantity(100.0, "cm"), num=3),
        [0.0, 0.5, 1.0],
        "m",
    )
    assert np.isclose(m, Quantity(np.array([300.1, 400.0]), "cm"), rtol=1e-3).all()
    with pytest.raises(TypeError):
        np.mean(m, out=np.empty(()))


def test_where_with_placeholder_first_and_mismatched_dimensions():
    m = Quantity(np.array([3.0, 4.0]), "m")
    result = np.where(np.array([True, False]), np.nan, m)
    assert np.isnan(result.value[0]) and result.value[1] == 4.0
    assert result.units == Unit("m")
    with pytest.raises(IncompatibleDimensions):
        np.where(np.array([True, False]), m, Quantity(np.array([1.0, 1.0]), "s"))


def test_arctan2_with_plain_number_requires_dimensionless():
    assert _same(np.arctan2(Quantity(1.0, ""), 1.0), np.pi / 4, "radian")
    with pytest.raises(IncompatibleDimensions):
        np.arctan2(Quantity(1.0, "m"), 1.0)


def test_concatenate_rejects_mismatched_dimensions():
    with pytest.raises(IncompatibleDimensions):
        np.concatenate([Quantity(np.array([1.0]), "m"), np.array([1.0])])


def test_temperature_comparisons_across_scales():
    c = Quantity(np.array([0.0, 100.0]), "C")
    f = Quantity(np.array([32.0, 32.0]), "F")
    assert np.array_equal(np.equal(c, f), [True, False])
    assert _same(np.maximum(c, f), [0.0, 100.0], "C")
