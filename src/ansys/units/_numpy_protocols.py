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
"""
NumPy ``__array_ufunc__`` and ``__array_function__`` support for ``Quantity``.

This module is only imported by ``Quantity`` when NumPy calls one of its
protocol methods, so NumPy remains an optional dependency.

Each handler either returns a result, raises an error when the units make the
operation invalid, or returns ``NotImplemented`` for unsupported functions
(NumPy then raises a ``TypeError``).
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

import numpy as np

from ansys.units.base_dimensions import BaseDimensions
from ansys.units.dimensions import Dimensions
from ansys.units.quantity import (
    DimensionlessArgumentRequired,
    IncompatibleDimensions,
    Quantity,
    get_si_value,
)
from ansys.units.unit import (
    ProhibitedOffsetUnitOperation,
    ProhibitedTemperatureOperation,
    Unit,
)

_DIMENSIONLESS = Dimensions()
_ANGLE = Dimensions({BaseDimensions.ANGLE: 1})


def _funcs(*names: str) -> frozenset[Any]:
    """Collect the NumPy functions that exist in the installed NumPy version."""
    return frozenset(
        func for func in (getattr(np, name, None) for name in names) if func
    )


# ---------------------------------------------------------------------------
# Value and unit helpers
# ---------------------------------------------------------------------------


def _plain(value: Any) -> Any:
    """Return a float for scalars and an ndarray otherwise."""
    array = np.asarray(value)
    if array.ndim == 0:
        item = array.item()
        if isinstance(item, (int, float)):
            return float(item)
    return array


def _as_quantity(value: Any) -> Quantity:
    return value if isinstance(value, Quantity) else Quantity(_plain(value), "")


def _raw(value: Any) -> Any:
    """Return the numeric value of a quantity or plain operand."""
    return value.value if isinstance(value, Quantity) else _plain(value)


def _wrap(value: Any, units: Unit | str) -> Quantity:
    """Build a quantity, turning 0-d NumPy results into Python floats."""
    if isinstance(value, (np.generic, np.ndarray)) and np.ndim(value) == 0:
        item = np.asarray(value).item()
        if isinstance(item, (int, float)):
            value = float(item)
    return Quantity(value, units)


def _convert_value(quantity: Quantity, units: Unit) -> Any:
    """Return the value of ``quantity`` expressed in ``units``."""
    if quantity.dimensions != units.dimensions:
        raise IncompatibleDimensions(quantity.units, units)
    if quantity.units == units:
        return quantity.value
    return get_si_value(quantity) / units.si_scaling_factor - units.si_offset


def _align(inputs: Sequence[Any]) -> tuple[Unit, list[Any]]:
    """Express all inputs in the units of the first one."""
    quantities = [_as_quantity(item) for item in inputs]
    units = quantities[0].units
    return units, [quantities[0].value] + [
        _convert_value(item, units) for item in quantities[1:]
    ]


def _si_value(value: Any, allowed: Sequence[Dimensions], name: str) -> Any:
    """Return a plain value in SI units, requiring dimensionless (or angle) input."""
    if not isinstance(value, Quantity):
        return _plain(value)
    if value.dimensions not in allowed:
        raise DimensionlessArgumentRequired(name, value.units, angle=_ANGLE in allowed)
    return get_si_value(value)


def _check_offset(units: Unit, op: str) -> None:
    if units.has_offset:
        raise ProhibitedOffsetUnitOperation(units, op)


def _check_additive(units: Unit) -> None:
    """Absolute temperatures cannot be added together."""
    if units.is_absolute_temperature:
        raise ProhibitedTemperatureOperation()


def _difference_units(units: Unit) -> Unit:
    """Units of a difference (or spread) of values expressed in ``units``."""
    if units.is_absolute_temperature:
        return units.to_temperature_difference()
    return units


def _no_out(kwargs: dict[str, Any]) -> bool:
    return kwargs.get("out") is None


# ---------------------------------------------------------------------------
# __array_ufunc__
# ---------------------------------------------------------------------------

_COMPARISONS = _funcs(
    "equal", "not_equal", "less", "less_equal", "greater", "greater_equal"
)
_SAME_UNITS = _funcs("maximum", "minimum", "fmax", "fmin")
_SAME_UNITS_MULTIPLICATIVE = _funcs("hypot", "fmod", "remainder")
_UNARY_SAME_UNITS = _funcs(
    "negative", "positive", "absolute", "fabs", "rint", "floor", "ceil", "trunc"
)
_UNARY_PLAIN_RESULT = _funcs("isnan", "isinf", "isfinite", "signbit")
_UNARY_POWERS: dict[Any, float] = {
    np.sqrt: 0.5,
    np.square: 2.0,
    np.cbrt: 1.0 / 3.0,
    np.reciprocal: -1.0,
}
_DIMENSIONLESS_FUNCS = _funcs(
    "exp",
    "exp2",
    "expm1",
    "log",
    "log2",
    "log10",
    "log1p",
    "sinh",
    "cosh",
    "tanh",
    "arcsinh",
    "arccosh",
    "arctanh",
)
_ANGLE_FUNCS = _funcs("sin", "cos", "tan")
_INVERSE_TRIG = _funcs("arcsin", "arccos", "arctan")
_REDUCIBLE = _funcs("add", "maximum", "minimum", "fmax", "fmin")


def array_ufunc(
    ufunc: np.ufunc, method: str, inputs: tuple[Any, ...], kwargs: dict[str, Any]
) -> Any:
    """Implement ``Quantity.__array_ufunc__``."""
    if not _no_out(kwargs):
        return NotImplemented
    kwargs = {key: val for key, val in kwargs.items() if key != "out"}

    if method == "__call__":
        return _ufunc_call(ufunc, inputs, kwargs)
    if method in ("reduce", "accumulate") and ufunc in _REDUCIBLE and len(inputs) == 1:
        quantity = _as_quantity(inputs[0])
        if ufunc is np.add:
            _check_additive(quantity.units)
        result = getattr(ufunc, method)(quantity.value, **kwargs)
        return _wrap(result, quantity.units)
    return NotImplemented


def _ufunc_call(
    ufunc: np.ufunc, inputs: tuple[Any, ...], kwargs: dict[str, Any]
) -> Any:
    if ufunc in (np.add, np.subtract):
        if kwargs:
            return NotImplemented
        left, right = (_as_quantity(item) for item in inputs)
        return left + right if ufunc is np.add else left - right

    if ufunc in _COMPARISONS:
        _, values = _align(inputs)
        return ufunc(*values, **kwargs)

    if ufunc in _SAME_UNITS or ufunc in _SAME_UNITS_MULTIPLICATIVE:
        units, values = _align(inputs)
        if ufunc in _SAME_UNITS_MULTIPLICATIVE:
            _check_offset(units, ufunc.__name__)
        return _wrap(ufunc(*values, **kwargs), units)

    if ufunc in (np.multiply, np.matmul, np.divide):
        return _product_or_quotient(ufunc, inputs, kwargs)

    if ufunc is np.power:
        return _power(ufunc, inputs, kwargs)

    if ufunc is np.arctan2:
        _, values = _align(inputs)
        return _wrap(ufunc(*values, **kwargs), "radian")

    if len(inputs) != 1:
        return NotImplemented
    (operand,) = inputs

    if ufunc in _UNARY_SAME_UNITS:
        return _wrap(ufunc(operand.value, **kwargs), operand.units)
    if ufunc in _UNARY_PLAIN_RESULT:
        return ufunc(operand.value, **kwargs)
    if ufunc is np.sign:
        return _wrap(ufunc(operand.value, **kwargs), "")
    if ufunc in _UNARY_POWERS:
        exponent = _UNARY_POWERS[ufunc]
        units = operand.units**exponent
        return _wrap(ufunc(operand.value, **kwargs), units)
    if ufunc in _ANGLE_FUNCS:
        value = _si_value(operand, (_DIMENSIONLESS, _ANGLE), ufunc.__name__)
        return _wrap(ufunc(value, **kwargs), "")
    if ufunc in _DIMENSIONLESS_FUNCS:
        value = _si_value(operand, (_DIMENSIONLESS,), ufunc.__name__)
        return _wrap(ufunc(value, **kwargs), "")
    if ufunc in _INVERSE_TRIG:
        value = _si_value(operand, (_DIMENSIONLESS,), ufunc.__name__)
        return _wrap(ufunc(value, **kwargs), "radian")
    return NotImplemented


def _product_or_quotient(
    ufunc: np.ufunc, inputs: tuple[Any, ...], kwargs: dict[str, Any]
) -> Quantity:
    left, right = inputs
    op = "/" if ufunc is np.divide else "*"
    left_is_q, right_is_q = isinstance(left, Quantity), isinstance(right, Quantity)

    if left_is_q and right_is_q:
        units = left.units / right.units if op == "/" else left.units * right.units
    elif left_is_q:
        _check_offset(left.units, op)
        units = left.units
    elif op == "/":
        _check_offset(right.units, op)
        units = right.units**-1
    else:
        _check_offset(right.units, op)
        units = right.units

    values = [_raw(item) for item in inputs]
    return _wrap(ufunc(*values, **kwargs), units)


def _power(
    ufunc: np.ufunc, inputs: tuple[Any, ...], kwargs: dict[str, Any]
) -> Quantity:
    base, exponent = inputs
    exponent = _si_value(exponent, (_DIMENSIONLESS,), "power exponent")
    if not isinstance(base, Quantity) or base.dimensions == _DIMENSIONLESS:
        base_value = _si_value(base, (_DIMENSIONLESS,), "power")
        return _wrap(ufunc(base_value, exponent, **kwargs), "")
    if np.ndim(exponent) != 0:
        raise ValueError(
            "Only a scalar exponent is supported for a quantity with units."
        )
    units = base.units ** float(exponent)
    return _wrap(ufunc(base.value, exponent, **kwargs), units)


# ---------------------------------------------------------------------------
# __array_function__
# ---------------------------------------------------------------------------

_Handler = Callable[[Any, tuple[Any, ...], dict[str, Any]], Any]

_SAME_UNITS_FUNCS = _funcs(
    "mean",
    "nanmean",
    "median",
    "nanmedian",
    "min",
    "max",
    "amin",
    "amax",
    "nanmin",
    "nanmax",
    "percentile",
    "nanpercentile",
    "quantile",
    "nanquantile",
    "sort",
    "round",
    "around",
    "ravel",
    "reshape",
    "transpose",
    "squeeze",
    "expand_dims",
    "flip",
    "copy",
    "take",
    "repeat",
    "roll",
    "swapaxes",
    "moveaxis",
    "broadcast_to",
    "tile",
)
_ADDITIVE_FUNCS = _funcs("sum", "nansum", "cumsum", "nancumsum")
_DIFFERENCE_FUNCS = _funcs("ptp", "diff", "std", "nanstd")
_VARIANCE_FUNCS = _funcs("var", "nanvar")
_PLAIN_RESULT_FUNCS = _funcs("shape", "ndim", "size", "argmax", "argmin", "argsort")
_STACKING_FUNCS = _funcs("concatenate", "stack", "hstack", "vstack")
_COMPARING_FUNCS = _funcs("isclose", "allclose", "array_equal")
_ATLEAST_FUNCS = _funcs("atleast_1d", "atleast_2d")


def array_function(
    func: Any, types: Sequence[type], args: tuple[Any, ...], kwargs: dict[str, Any]
) -> Any:
    """Implement ``Quantity.__array_function__``."""
    handler = _function_handler(func)
    if handler is None or not _no_out(kwargs):
        return NotImplemented
    kwargs = {key: val for key, val in kwargs.items() if key != "out"}
    return handler(func, args, kwargs)


def _function_handler(func: Any) -> _Handler | None:
    if func in _SAME_UNITS_FUNCS:
        return _same_units
    if func in _ADDITIVE_FUNCS:
        return _additive
    if func in _DIFFERENCE_FUNCS:
        return _difference
    if func in _VARIANCE_FUNCS:
        return _variance
    if func in _PLAIN_RESULT_FUNCS:
        return _plain_result
    if func in _STACKING_FUNCS:
        return _stacking
    if func in _COMPARING_FUNCS:
        return _comparing
    if func in _ATLEAST_FUNCS:
        return _atleast
    return {
        np.clip: _clip,
        np.where: _where,
        np.dot: _dot,
        np.linspace: _linspace,
        np.linalg.norm: _norm,
    }.get(func)


def _same_units(func: Any, args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
    quantity, rest = args[0], args[1:]
    if not isinstance(quantity, Quantity):
        return NotImplemented
    return _wrap(func(quantity.value, *rest, **kwargs), quantity.units)


def _norm(func: Any, args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
    # A norm squares its input, which is meaningless for offset units such as 'C'.
    if isinstance(args[0], Quantity):
        _check_offset(args[0].units, "norm")
    return _same_units(func, args, kwargs)


def _additive(func: Any, args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
    if isinstance(args[0], Quantity):
        _check_additive(args[0].units)
    return _same_units(func, args, kwargs)


def _difference(func: Any, args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
    quantity, rest = args[0], args[1:]
    if not isinstance(quantity, Quantity):
        return NotImplemented
    units = _difference_units(quantity.units)
    return _wrap(func(quantity.value, *rest, **kwargs), units)


def _variance(func: Any, args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
    quantity, rest = args[0], args[1:]
    if not isinstance(quantity, Quantity):
        return NotImplemented
    units = _difference_units(quantity.units) ** 2
    return _wrap(func(quantity.value, *rest, **kwargs), units)


def _plain_result(func: Any, args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
    return func(args[0].value, *args[1:], **kwargs)


def _atleast(func: Any, args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
    if len(args) != 1:
        return NotImplemented
    return _same_units(func, args, kwargs)


def _stacking(func: Any, args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
    sequence, rest = args[0], args[1:]
    units, values = _align(sequence)
    return _wrap(func(values, *rest, **kwargs), units)


def _comparing(func: Any, args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
    _, values = _align(args[:2])
    return func(*values, *args[2:], **kwargs)


def _clip(func: Any, args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
    quantity = args[0]
    if not isinstance(quantity, Quantity):
        return NotImplemented
    lower = args[1] if len(args) > 1 else kwargs.pop("a_min", None)
    upper = args[2] if len(args) > 2 else kwargs.pop("a_max", None)
    lower = kwargs.pop("min", lower)
    upper = kwargs.pop("max", upper)
    limits = [
        None if limit is None else _convert_value(_as_quantity(limit), quantity.units)
        for limit in (lower, upper)
    ]
    return _wrap(func(quantity.value, *limits, **kwargs), quantity.units)


def _where(func: Any, args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
    if len(args) != 3:
        return NotImplemented
    condition, first, second = args
    quantities = [item for item in (first, second) if isinstance(item, Quantity)]
    if not quantities:
        return NotImplemented
    units = quantities[0].units
    values = []
    for item in (first, second):
        if isinstance(item, Quantity):
            values.append(_convert_value(item, units))
        elif np.all(~np.isfinite(_plain(item))):
            # Non-finite placeholders such as NaN carry no units.
            values.append(_plain(item))
        else:
            raise IncompatibleDimensions(Unit(""), units)
    return _wrap(func(condition, *values, **kwargs), units)


def _dot(func: Any, args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
    left, right = args[:2]
    # Combine units of unit-valued placeholders so that the multiplication rules
    # (including offset-unit validation) apply.
    placeholders = [
        Quantity(1.0, item.units) if isinstance(item, Quantity) else 1.0
        for item in (left, right)
    ]
    units = _product_or_quotient(np.multiply, tuple(placeholders), {}).units
    values = [_raw(item) for item in (left, right)]
    return _wrap(func(*values, *args[2:], **kwargs), units)


def _linspace(func: Any, args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
    names = ("start", "stop")
    start, stop = (
        args[i] if len(args) > i else kwargs.pop(names[i], None) for i in range(2)
    )
    if not isinstance(start, Quantity) or stop is None:
        return NotImplemented
    stop_value = _convert_value(_as_quantity(stop), start.units)
    return _wrap(func(start.value, stop_value, *args[2:], **kwargs), start.units)
