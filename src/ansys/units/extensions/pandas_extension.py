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
Pandas extension for ansys-units.

This module provides pandas ExtensionDtype and ExtensionArray implementations for unit-
aware DataFrames and Series.
"""

# flake8: noqa: E501

import numbers
import operator
import re
from typing import Any, Callable

import numpy as np
import pandas as pd
from pandas.api.extensions import (
    ExtensionArray,
    ExtensionDtype,
    no_default,
    register_dataframe_accessor,
    register_extension_dtype,
    register_series_accessor,
    take,
)
from pandas.api.indexers import (
    check_array_indexer,
)
from pandas.api.types import (
    is_integer,
    is_object_dtype,
    is_string_dtype,
)
from typing_extensions import override

from ansys.units.quantity import Quantity, Vector
from ansys.units.unit import ProhibitedTemperatureOperation, Unit

# Default subdtype for numeric data
DEFAULT_SUBDTYPE = "Float64"

# Grouped aggregations whose result has the units of the input
_SAME_UNIT_GROUPBY_OPS = frozenset(
    {"sum", "mean", "median", "min", "max", "first", "last"}
    | {"cumsum", "cummin", "cummax", "prod", "cumprod"}
)

# Reductions whose result has the units of the input
_SAME_UNIT_REDUCTIONS = frozenset({"sum", "mean", "median", "min", "max"})
# Reductions of the spread of the values
_SPREAD_REDUCTIONS = frozenset({"std", "sem", "var"})
# Dimensionless shape statistics
_UNITLESS_REDUCTIONS = frozenset({"skew", "kurt"})


def _spread_units(name: str, units: Unit) -> Unit:
    """Units of a standard deviation or variance of values in ``units``."""
    # The spread of absolute temperatures is a temperature difference.
    if units.is_absolute_temperature:
        units = units.to_temperature_difference()
    return units**2 if name == "var" else units


def _check_product(name: str, dtype: "QuantityDtype") -> None:
    """Products of a varying number of values only work without units."""
    if dtype.units != Unit(""):
        raise TypeError(
            f"Cannot perform {name} with dtype {dtype}: each result would have "
            "different units. Convert to a dimensionless series first."
        )


def _check_accumulation(name: str, dtype: "QuantityDtype") -> None:
    if name == "cumprod":
        _check_product(name, dtype)
    elif name not in ("cumsum", "cummin", "cummax"):
        raise TypeError(f"Cannot perform {name} with dtype {dtype}")
    elif name == "cumsum" and dtype.units.is_absolute_temperature:
        raise ProhibitedTemperatureOperation()


def _reduction_units(name: str, dtype: "QuantityDtype", count: int) -> Unit | None:
    """
    Units of the result of a reduction over ``count`` values.

    Returns ``None`` for dimensionless shape statistics and raises an error for
    reductions that make no sense for the units.
    """
    units = dtype.units
    if name in _SAME_UNIT_REDUCTIONS:
        if name == "sum" and units.is_absolute_temperature:
            raise ProhibitedTemperatureOperation()
        return units
    if name in _SPREAD_REDUCTIONS:
        return _spread_units(name, units)
    if name == "prod":
        # The product of ``count`` values in ``u`` has units ``u^count``.
        return units**count
    if name in _UNITLESS_REDUCTIONS:
        return None
    raise TypeError(f"Cannot perform {name} with dtype {dtype}")


@register_extension_dtype
class QuantityDtype(ExtensionDtype):
    """
    An ExtensionDtype for holding unit-aware Quantity data.

    Parameters
    ----------
    units : str or Unit
        The units for the quantities in this dtype.
    subdtype : str or dtype, optional
        The underlying numpy dtype for numeric values.

    Examples
    --------
    >>> import pandas as pd
    >>> from ansys.units.extensions.pandas_extension import QuantityDtype
    >>> dtype = QuantityDtype("m")
    >>> series = pd.Series([1.0, 2.0, 3.0], dtype=dtype)
    """

    type: "type[Quantity]" = Quantity
    units: Unit | None = None
    subdtype: Any | None = None
    _metadata: tuple[str, ...] = ("units", "subdtype")
    _match: re.Pattern[str] = re.compile(
        r"quantity\[(?P<units>[^\]]*)\](?:\[(?P<subdtype>.+)\])?"
    )
    _cache: dict[tuple[str, Any], "QuantityDtype"] = {}

    def __new__(
        cls, units: str | Unit | None = None, subdtype: Any | None = None
    ) -> "QuantityDtype":
        """
        Create a new QuantityDtype.

        Parameters
        ----------
        units : str or Unit, optional
            Units for this dtype.
        subdtype : str or dtype, optional
            Underlying dtype for numeric values.
        """
        if isinstance(units, QuantityDtype):
            return units

        if units is None:
            # Empty constructor for pickle compatibility
            return object.__new__(cls)

        # Parse units if string
        if isinstance(units, str):
            # Check if it's a full dtype string like "quantity[m][float64]"
            if units.startswith("quantity["):
                m = cls._match.search(units)
                if m:
                    units = m.group("units")
                    subdtype = subdtype or m.group("subdtype") or DEFAULT_SUBDTYPE

        # Convert string to Unit
        if not isinstance(units, Unit):
            units = Unit(units)

        if subdtype is None:
            subdtype = DEFAULT_SUBDTYPE

        # Use cached dtype if available
        try:
            return cls._cache[(str(units), subdtype)]
        except KeyError:
            u = object.__new__(cls)
            u.units = units
            u.subdtype = subdtype
            cls._cache[(str(units), subdtype)] = u
            return u

    @property
    def _is_numeric(self) -> bool:
        """Whether this dtype is numeric."""
        return True

    @override
    @classmethod
    def construct_from_string(cls, string: str) -> "QuantityDtype":
        """
        Construct dtype from string.

        Parameters
        ----------
        string : str
            String representation of the dtype.

        Returns
        -------
        QuantityDtype
        """
        if string.startswith("quantity["):
            return cls(string)

        # Try to interpret as unit string
        try:
            return cls(units=string)
        except Exception:
            raise TypeError(f"Cannot construct a 'QuantityDtype' from '{string}'")

    @property
    @override
    def name(self) -> str:
        """String representation of the dtype."""
        if self.subdtype and self.subdtype != DEFAULT_SUBDTYPE:
            return f"quantity[{self.units}][{self.subdtype}]"
        return f"quantity[{self.units}]"

    @property
    @override
    def na_value(self) -> Quantity:
        """The NA value for this dtype."""
        return Quantity(np.nan, str(self.units))

    @override
    def __hash__(self) -> int:
        """Hash the dtype."""
        return hash((str(self.units), str(self.subdtype)))

    @override
    def __eq__(self, other: Any) -> bool:
        """Check equality with another dtype."""
        if isinstance(other, str):
            try:
                other = QuantityDtype(other)
            except (ValueError, TypeError):
                return False

        if not isinstance(other, QuantityDtype):
            return False

        return str(self.units) == str(other.units) and self.subdtype == other.subdtype

    @override
    def __repr__(self) -> str:
        """String representation."""
        return self.name

    @override
    def construct_array_type(self) -> Any:
        """Return the array type associated with this dtype."""
        return QuantityArray

    def _get_common_dtype(self, dtypes: list[Any]) -> "QuantityDtype | None":
        """
        Return the dtype to use when combining arrays, for example in ``pd.concat``.

        Arrays with compatible units are combined in the units of the first array.
        Otherwise the result is an ``object`` array.
        """
        if all(
            isinstance(dtype, QuantityDtype)
            and dtype.units.dimensions == self.units.dimensions
            for dtype in dtypes
        ):
            return self
        return None


class QuantityArray(ExtensionArray):
    """
    An ExtensionArray for holding Quantity data.

    Parameters
    ----------
    values : array-like
        Numeric values for the quantities.
    dtype : QuantityDtype or str
        The dtype containing unit information.
    copy : bool, default False
        Whether to copy the input values.

    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> from ansys.units.extensions.pandas_extension import QuantityArray
    >>> arr = QuantityArray([1.0, 2.0, 3.0], dtype="quantity[m]")
    >>> series = pd.Series(arr)
    """

    _data: Any
    _dtype: QuantityDtype
    _can_hold_na: bool = True

    def __init__(
        self, values: Any, dtype: QuantityDtype | str | None = None, copy: bool = False
    ) -> None:
        """Initialize the QuantityArray."""
        # Parse dtype
        if dtype is None:
            if isinstance(values, QuantityArray):
                dtype = values._dtype
            elif isinstance(values, Quantity):
                dtype = QuantityDtype(units=values.units)
            else:
                raise ValueError("Must specify dtype when values are not Quantity")

        if not isinstance(dtype, QuantityDtype):
            dtype = QuantityDtype(dtype)

        self._dtype = dtype

        # Extract values from Quantity if needed
        if isinstance(values, Quantity):
            # Convert to target units
            values = values.to(str(dtype.units)).value
        elif isinstance(values, QuantityArray):
            if values.dtype.units != dtype.units:
                values = values.to(str(dtype.units))
            values = values._data

        # Convert to pandas array with subdtype
        if not isinstance(values, ExtensionArray):
            values = pd.array(values, copy=copy, dtype=dtype.subdtype)

        self._data = values

    @property
    def dtype(self) -> QuantityDtype:
        """The dtype for this array."""
        return self._dtype

    def __len__(self) -> int:
        """Length of the array."""
        return len(self._data)

    def __getitem__(self, item: Any) -> Any:
        """
        Select subset of self.

        Parameters
        ----------
        item : int, slice, or ndarray
            Indexer for the array.

        Returns
        -------
        Quantity or QuantityArray
        """
        if is_integer(item):
            value = self._data[item]
            # Check if value is NaN/NA and return it directly
            if pd.isna(value):
                return value
            return Quantity(value, str(self._dtype.units))

        item: Any = check_array_indexer(self, item)
        return type(self)(self._data[item], self._dtype)

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Set values in the array.

        Parameters
        ----------
        key : int, slice, or ndarray
            Indexer for the array.
        value : scalar or array-like
            Value(s) to set.
        """
        # Convert Quantity to magnitude in our units
        if isinstance(value, Quantity):
            value = value.to(str(self._dtype.units)).value

        self._data[key] = value

    def isna(self) -> np.ndarray[Any, Any]:
        """
        Boolean indicator of missing values.

        Returns
        -------
        np.ndarray
        """
        return np.asarray(self._data.isna())

    def take(
        self, indices: Any, allow_fill: bool = False, fill_value: Any = None
    ) -> "QuantityArray":
        """
        Take elements from array.

        Parameters
        ----------
        indices : sequence of int
            Indices to take.
        allow_fill : bool, default False
            Whether to allow filling with fill_value.
        fill_value : any, optional
            Value to use for missing indices.

        Returns
        -------
        QuantityArray
        """
        if isinstance(fill_value, Quantity):
            fill_value = fill_value.to(str(self._dtype.units)).value

        result: np.ndarray[Any, Any] | ExtensionArray = take(
            self._data, indices, fill_value=fill_value, allow_fill=allow_fill
        )
        return QuantityArray(result, dtype=self.dtype)

    def copy(self, deep: bool = True) -> "QuantityArray":
        """
        Copy the array.

        Parameters
        ----------
        deep : bool, default True
            Kept for backward compatibility. The underlying data is always copied,
            as pandas requires, so changes to the copy never affect the original.

        Returns
        -------
        QuantityArray
        """
        return type(self)(self._data.copy(), dtype=self.dtype)

    def unique(self) -> "QuantityArray":
        """Return the unique values, in order of appearance."""
        return type(self)(self._data.unique(), dtype=self.dtype)

    def round(self, decimals: int = 0, *args: Any, **kwargs: Any) -> "QuantityArray":
        """Round the values to the given number of decimals, keeping the units."""
        return type(self)(self._data.round(decimals), dtype=self.dtype)

    def __neg__(self) -> "QuantityArray":
        return type(self)(-self._data, dtype=self.dtype)

    def __pos__(self) -> "QuantityArray":
        return type(self)(self._data.copy(), dtype=self.dtype)

    def __abs__(self) -> "QuantityArray":
        return type(self)(abs(self._data), dtype=self.dtype)

    @classmethod
    def _concat_same_type(cls, to_concat: list["QuantityArray"]) -> "QuantityArray":
        """
        Concatenate multiple arrays of this type.

        Parameters
        ----------
        to_concat : list of QuantityArray

        Returns
        -------
        QuantityArray
        """
        output_units: Unit | None = to_concat[0]._dtype.units

        data: list[Any] = []
        for arr in to_concat:
            # Convert all arrays to output units
            converted: QuantityArray = arr.to(str(output_units))
            data.append(np.atleast_1d(converted._data))

        return cls(np.concatenate(data), to_concat[0].dtype)

    @classmethod
    def _from_sequence(
        cls, scalars: Any, dtype: QuantityDtype | None = None, copy: bool = False
    ) -> "QuantityArray":
        """
        Construct array from sequence of scalars.

        Parameters
        ----------
        scalars : sequence
            Sequence of values.
        dtype : QuantityDtype, optional
            Dtype for the array.
        copy : bool, default False
            Whether to copy the data.

        Returns
        -------
        QuantityArray
        """
        # Try to find a Quantity in scalars to infer units
        master_quantity: Quantity | None = None
        for item in scalars:
            if isinstance(item, Quantity):
                master_quantity = item
                break

        if dtype is None:
            if master_quantity is None:
                raise ValueError(
                    "Cannot infer dtype. No dtype specified and no Quantity found"
                )
            dtype = QuantityDtype(units=master_quantity.units)

        # Convert all Quantities to magnitudes in target units
        values: list[Any] = []
        for item in scalars:
            if isinstance(item, Quantity):
                values.append(item.to(str(dtype.units)).value)
            else:
                values.append(item)

        return cls(values, dtype=dtype, copy=copy)

    @classmethod
    def _from_factorized(
        cls, values: Any, original: "QuantityArray"
    ) -> "QuantityArray":
        """Reconstruct from factorized values."""
        return cls(values, dtype=original.dtype)

    def _values_for_factorize(self) -> tuple[np.ndarray[Any, Any], float]:
        """Return values for factorization."""
        return self._data.to_numpy(dtype="float64", na_value=np.nan), np.nan

    @property
    def quantity(self) -> Quantity:
        """Convert to single Quantity with array value."""
        return Quantity(np.asarray(self._data), str(self._dtype.units))

    def to(self, units: str | Unit) -> "QuantityArray":
        """
        Convert to different units.

        Parameters
        ----------
        units : str or Unit
            Target units.

        Returns
        -------
        QuantityArray
        """
        if not isinstance(units, Unit):
            units = Unit(units)

        # Convert the quantity
        converted: Quantity[float | Vector] = self.quantity.to(str(units))
        return QuantityArray(converted.value, dtype=QuantityDtype(units))

    def astype(self, dtype: Any, copy: bool = True) -> Any:
        """
        Cast to different dtype.

        Parameters
        ----------
        dtype : str or dtype
            Target dtype.
        copy : bool, default True
            Whether to copy the data.

        Returns
        -------
        array
        """
        if isinstance(dtype, str) and dtype.startswith("quantity["):
            dtype = QuantityDtype(dtype)

        if isinstance(dtype, QuantityDtype):
            if dtype == self._dtype and not copy:
                return self
            return self.to(str(dtype.units))

        if is_object_dtype(dtype):
            return np.array([self[i] for i in range(len(self))], dtype=object)

        if is_string_dtype(dtype):
            return pd.Series([str(self[i]) for i in range(len(self))], dtype=dtype)

        return pd.array(self._data, dtype=dtype, copy=copy)

    def __array__(
        self, dtype: Any | None = None, copy: bool = False
    ) -> np.ndarray[Any, Any]:
        """Convert to numpy array."""
        if dtype is None or is_object_dtype(dtype):
            # Return array of Quantity objects
            return np.array([self[i] for i in range(len(self))], dtype=object)
        return np.array(self._data, dtype=dtype, copy=copy)

    def to_numpy(
        self, dtype: Any = None, copy: bool = False, na_value: Any = no_default
    ) -> np.ndarray[Any, Any]:
        """
        Convert to a NumPy array.

        With a numeric ``dtype``, return the plain values in the array's units, with
        missing values replaced by ``na_value``. Otherwise return ``Quantity``
        objects.
        """
        if dtype is None or is_object_dtype(dtype):
            values = np.array([self[i] for i in range(len(self))], dtype=object)
            if na_value is not no_default:
                values[np.asarray(self.isna())] = na_value
            return values
        return self._data.to_numpy(dtype=dtype, copy=copy, na_value=na_value)

    @staticmethod
    def _create_arithmetic_method(
        op: Callable[[Any, Any], Any], reflected: bool = False
    ) -> Callable[..., Any]:
        """
        Create arithmetic method.

        Parameters
        ----------
        op : Callable
            The binary operator to apply.
        reflected : bool, optional
            If ``True``, reverse operand order so that ``op(rhs, lhs)`` is
            computed instead of ``op(lhs, rhs)``.  Required for
            ``__rsub__`` and ``__rtruediv__`` where the array is the *right*
            operand of the original expression.
        """

        def method(self: "QuantityArray", other: Any) -> Any:
            if isinstance(other, (pd.Series, pd.DataFrame, pd.Index)):
                return NotImplemented

            # Convert to quantities
            lhs: Quantity[float | Vector] = self.quantity
            rhs: Any

            if isinstance(other, QuantityArray):
                rhs = other.quantity
            elif isinstance(other, Quantity):
                rhs = other
            elif isinstance(other, (numbers.Number, np.ndarray)):
                rhs = other
            else:
                return NotImplemented

            # Perform operation — reflected ops swap operand order so that
            # e.g. ``x - array`` computes ``op(x, array)`` not ``op(array, x)``.
            result = op(rhs, lhs) if reflected else op(lhs, rhs)

            # Convert back to array
            return QuantityArray(result)

        return method

    @staticmethod
    def _create_comparison_method(op: Callable[..., Any]) -> Callable[..., Any]:
        """Create an element-wise comparison method from a NumPy comparison ufunc."""

        def method(self: "QuantityArray", other: Any) -> Any:
            if isinstance(other, (pd.Series, pd.DataFrame, pd.Index)):
                return NotImplemented

            rhs = other.quantity if isinstance(other, QuantityArray) else other
            return op(self.quantity, rhs)

        return method

    def _reduce(
        self, name: str, *, skipna: bool = True, keepdims: bool = False, **kwargs: Any
    ) -> Any:
        """Reductions such as ``sum``, ``mean``, ``std`` and ``prod``."""
        count = int(np.sum(~self.isna())) if skipna else len(self)
        units = _reduction_units(name, self._dtype, count)
        result = self._data._reduce(name, skipna=skipna, keepdims=keepdims, **kwargs)
        if units is None:
            # Shape statistics such as skewness have no units, so they are plain
            # floats.
            if keepdims:
                return result.to_numpy(dtype="float64", na_value=np.nan)
            return np.nan if result is pd.NA else result
        if keepdims:
            # DataFrame reductions ask for a length-1 array.
            return type(self)(result, dtype=QuantityDtype(units))
        if result is pd.NA:
            result = np.nan
        return Quantity(result, units)

    def _accumulate(
        self, name: str, *, skipna: bool = True, **kwargs: Any
    ) -> "QuantityArray":
        """Cumulative sum, minimum, maximum and (dimensionless) product."""
        _check_accumulation(name, self._dtype)
        result = self._data._accumulate(name, skipna=skipna, **kwargs)
        return type(self)(result, dtype=self.dtype)

    def _groupby_op(
        self,
        *,
        how: str,
        has_dropped_na: bool,
        min_count: int,
        ngroups: int,
        ids: Any,
        **kwargs: Any,
    ) -> Any:
        """Grouped aggregations (``df.groupby(...)[col].sum()`` and so on)."""
        units = self._dtype.units
        if how in ("prod", "cumprod"):
            _check_product(how, self._dtype)
        if how in ("sum", "cumsum") and units.is_absolute_temperature:
            raise ProhibitedTemperatureOperation()

        result = self._data._groupby_op(
            how=how,
            has_dropped_na=has_dropped_na,
            min_count=min_count,
            ngroups=ngroups,
            ids=ids,
            **kwargs,
        )

        if how in ("std", "sem", "var"):
            units = _spread_units(how, units)
        elif how not in _SAME_UNIT_GROUPBY_OPS:
            # Counts, ranks, skewness, and similar results have no units.
            return result
        return type(self)(result, dtype=QuantityDtype(units))

    # Ensure pandas / numpy defer to us for ops
    __array_priority__: int = 1000

    # Arithmetic operators
    __add__: Callable[[Any, Any], Any] = _create_arithmetic_method(operator.add)
    __sub__: Callable[[Any, Any], Any] = _create_arithmetic_method(operator.sub)
    __mul__: Callable[[Any, Any], Any] = _create_arithmetic_method(operator.mul)
    __truediv__: Callable[[Any, Any], Any] = _create_arithmetic_method(operator.truediv)

    # Reverse ops
    __radd__: Callable[[Any, Any], Any] = _create_arithmetic_method(operator.add)
    __rsub__: Callable[[Any, Any], Any] = _create_arithmetic_method(
        operator.sub, reflected=True
    )
    __rmul__: Callable[[Any, Any], Any] = _create_arithmetic_method(operator.mul)
    __rtruediv__: Callable[[Any, Any], Any] = _create_arithmetic_method(
        operator.truediv, reflected=True
    )

    # Comparisons (element-wise, with unit conversion)
    __eq__: Callable[[Any, Any], Any] = _create_comparison_method(np.equal)
    __ne__: Callable[[Any, Any], Any] = _create_comparison_method(np.not_equal)
    __lt__: Callable[[Any, Any], Any] = _create_comparison_method(np.less)
    __le__: Callable[[Any, Any], Any] = _create_comparison_method(np.less_equal)
    __gt__: Callable[[Any, Any], Any] = _create_comparison_method(np.greater)
    __ge__: Callable[[Any, Any], Any] = _create_comparison_method(np.greater_equal)


@register_series_accessor("units")
class UnitsSeriesAccessor:
    """
    Accessor for unit-aware operations on Series.

    Examples
    --------
    >>> import pandas as pd
    >>> from ansys.units.extensions.pandas_extension import QuantityDtype
    >>> series = pd.Series([1.0, 2.0, 3.0], dtype=QuantityDtype("m"))
    >>> series.units.to("ft")
    """

    def __init__(self, pandas_obj: Any) -> None:
        """Initialize the accessor."""
        self._obj = pandas_obj
        if not isinstance(pandas_obj.dtype, QuantityDtype):
            raise AttributeError(
                "Series must have QuantityDtype to use .units accessor"
            )

    def to(self, units: str | Unit) -> Any:
        """
        Convert to different units.

        Parameters
        ----------
        units : str or Unit
            Target units.

        Returns
        -------
        pd.Series
        """
        if not isinstance(self._obj.array, QuantityArray):
            raise TypeError("Series must contain QuantityArray")

        converted: QuantityArray = self._obj.array.to(units)
        return pd.Series(converted, index=self._obj.index, name=self._obj.name)

    def describe(self, percentiles: tuple[float, ...] = (0.25, 0.5, 0.75)) -> pd.Series:
        """
        Summary statistics that keep their units.

        ``Series.describe()`` converts its results to plain floats, which drops the
        units. This method returns the same statistics as ``Quantity`` objects.

        Parameters
        ----------
        percentiles : tuple of float, default (0.25, 0.5, 0.75)
            Percentiles to include, between 0 and 1.

        Returns
        -------
        pd.Series
            ``count`` followed by ``Quantity`` values for ``mean``, ``std``,
            ``min``, the percentiles, and ``max``.
        """
        series = self._obj
        stats: dict[str, Any] = {
            "count": series.count(),
            "mean": series.mean(),
            "std": series.std(),
            "min": series.min(),
        }
        for percentile in percentiles:
            stats[f"{percentile * 100:g}%"] = series.quantile(percentile)
        stats["max"] = series.max()
        return pd.Series(stats, name=series.name, dtype=object)

    @property
    def quantity(self) -> Quantity:
        """Get the underlying Quantity."""
        if not isinstance(self._obj.array, QuantityArray):
            raise TypeError("Series must contain QuantityArray")
        return self._obj.array.quantity

    def rolling(self, *args: Any, **kwargs: Any) -> "UnitAwareWindow":
        """
        Rolling window whose results keep their units.

        Takes the same arguments as :meth:`pandas.Series.rolling`. For example,
        ``series.units.rolling(3).mean()``.
        """
        return UnitAwareWindow(self._values().rolling(*args, **kwargs), self._obj.dtype)

    def expanding(self, *args: Any, **kwargs: Any) -> "UnitAwareWindow":
        """
        Expanding window whose results keep their units.

        See :meth:`rolling`.
        """
        return UnitAwareWindow(
            self._values().expanding(*args, **kwargs), self._obj.dtype
        )

    def ewm(self, *args: Any, **kwargs: Any) -> "UnitAwareWindow":
        """Exponentially weighted window whose results keep their units."""
        return UnitAwareWindow(self._values().ewm(*args, **kwargs), self._obj.dtype)

    def _values(self) -> pd.Series:
        """The values as a plain float series, with missing values as NaN."""
        values = self._obj.array.to_numpy(dtype="float64", na_value=np.nan)
        return pd.Series(values, index=self._obj.index, name=self._obj.name)


# Window methods whose result has the units of the input
_SAME_UNIT_WINDOW_METHODS = frozenset(
    {"sum", "mean", "median", "min", "max", "quantile", "first", "last"}
)


class UnitAwareWindow:
    """
    Rolling, expanding, or exponentially weighted window that keeps units.

    Returned by ``series.units.rolling()``, ``series.units.expanding()`` and
    ``series.units.ewm()``. Methods such as ``mean`` and ``max`` return a series in
    the original units, ``std`` and ``sem`` return the units of a difference, and
    ``var`` returns squared units. Methods whose units can't be determined, such as
    ``apply``, return plain floats.
    """

    def __init__(self, window: Any, dtype: QuantityDtype) -> None:
        self._window = window
        self._dtype = dtype

    def __getattr__(self, name: str) -> Any:
        attribute = getattr(self._window, name)
        if not callable(attribute):
            return attribute

        units = self._units_for(name)

        def method(*args: Any, **kwargs: Any) -> Any:
            result = attribute(*args, **kwargs)
            if units is None:
                return result
            return pd.Series(
                QuantityArray(result.to_numpy(), dtype=QuantityDtype(units)),
                index=result.index,
                name=result.name,
            )

        return method

    def _units_for(self, name: str) -> Unit | None:
        units = self._dtype.units
        if name in _SAME_UNIT_WINDOW_METHODS:
            if name == "sum" and units.is_absolute_temperature:
                raise ProhibitedTemperatureOperation()
            return units
        if name in _SPREAD_REDUCTIONS:
            return _spread_units(name, units)
        return None


@register_dataframe_accessor("units")
class UnitsDataFrameAccessor:
    """
    Accessor for unit-aware operations on DataFrames.

    Examples
    --------
    >>> import pandas as pd
    >>> from ansys.units.extensions.pandas_extension import QuantityDtype
    >>> df = pd.DataFrame({
    ...     "length": pd.Series([1.0, 2.0], dtype=QuantityDtype("m")),
    ...     "mass": pd.Series([10.0, 20.0], dtype=QuantityDtype("kg"))
    ... })
    >>> df.units.summary()
    """

    def __init__(self, pandas_obj: Any) -> None:
        """Initialize the accessor."""
        self._obj = pandas_obj

    def summary(self) -> dict[str, str]:
        """
        Get summary of units in the DataFrame.

        Returns
        -------
        dict
            Dictionary mapping column names to their units.
        """
        summary: dict[str, str] = {}
        for col in self._obj.columns:
            if isinstance(self._obj[col].dtype, QuantityDtype):
                summary[col] = str(self._obj[col].dtype.units)
        return summary

    def describe(
        self, percentiles: tuple[float, ...] = (0.25, 0.5, 0.75)
    ) -> pd.DataFrame:
        """
        Summary statistics of the unit-aware columns that keep their units.

        Parameters
        ----------
        percentiles : tuple of float, default (0.25, 0.5, 0.75)
            Percentiles to include, between 0 and 1.

        Returns
        -------
        pd.DataFrame
            One column per unit-aware column. See
            :meth:`UnitsSeriesAccessor.describe`.
        """
        return pd.DataFrame(
            {
                col: self._obj[col].units.describe(percentiles)
                for col in self._obj.columns
                if isinstance(self._obj[col].dtype, QuantityDtype)
            }
        )

    def to(self, units_map: dict[str, str | Unit]) -> Any:
        """
        Convert columns to different units.

        Parameters
        ----------
        units_map : dict
            Dictionary mapping column names to target units.

        Returns
        -------
        pd.DataFrame
        """
        df = self._obj.copy()
        for col, units in units_map.items():
            if col in df.columns and isinstance(df[col].dtype, QuantityDtype):
                df[col] = df[col].units.to(units)
        return df
