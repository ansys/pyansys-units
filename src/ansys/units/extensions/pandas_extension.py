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
from numpy.typing import NDArray
import pandas as pd
from pandas.api.extensions import (
    ExtensionArray,
    ExtensionDtype,
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
from ansys.units.unit import Unit

# Default subdtype for numeric data
DEFAULT_SUBDTYPE = "Float64"


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
        r"quantity\[(?P<units>.+)\](?:\[(?P<subdtype>.+)\])?"
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
    @classmethod
    def construct_array_type(cls) -> Any:
        """Return the array type associated with this dtype."""
        return QuantityArray


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

    def copy(self, deep: bool = False) -> "QuantityArray":
        """
        Copy the array.

        Parameters
        ----------
        deep : bool, default False
            Whether to deep copy the underlying data.

        Returns
        -------
        QuantityArray
        """
        data = self._data
        if deep:
            data = data.copy()

        return type(self)(data, dtype=self.dtype)

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

    def _values_for_factorize(self) -> tuple[np.ndarray[Any, Any], Quantity]:
        """Return values for factorization."""
        return np.asarray(self._data), self.dtype.na_value

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

    @staticmethod
    def _create_arithmetic_method(op: Callable[..., Any]) -> Callable[..., Any]:
        """Create arithmetic method."""

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

            # Perform operation
            result = op(lhs, rhs)

            # Convert back to array
            if isinstance(result, Quantity):
                return QuantityArray._from_sequence([result])
            return NotImplemented

        return method

    @staticmethod
    def _create_comparison_method(op: Callable[..., Any]) -> Callable[..., Any]:
        """Create comparison method."""

        def method(self: "QuantityArray", other: Any) -> Any:
            if isinstance(other, (pd.Series, pd.DataFrame, pd.Index)):
                return NotImplemented

            lhs: Quantity[float | Vector] = self.quantity

            if isinstance(other, QuantityArray):
                rhs: Quantity[float | Vector] = other.quantity
            elif isinstance(other, Quantity):
                rhs = other
            else:
                rhs = other

            result = op(lhs, rhs)
            return result

        return method

    def _reduce(self, name: str, *, skipna: bool = True, **kwargs: Any) -> "Quantity":
        """
        Perform reduction operation on the QuantityArray.

        Parameters
        ----------
        name : str
            Name of the reduction function: 'sum', 'mean', 'min', 'max', 'std', 'var'.
        skipna : bool, default True
            Whether to ignore NaNs in the reduction.
        **kwargs : Any
            Extra keyword arguments for NumPy functions.

        Returns
        -------
        Quantity
            The result as a Quantity with proper units.
        """
        # Map names to NumPy functions that handle NaNs
        functions: dict[str, Callable[..., Any]] = {
            "sum": np.nansum,
            "mean": np.nanmean,
            "min": np.nanmin,
            "max": np.nanmax,
            "std": np.nanstd,
            "var": np.nanvar,
        }

        if name not in functions:
            raise TypeError(f"Cannot perform {name} with dtype {self.dtype}")

        data: NDArray[Any] = np.asarray(self._data)

        if skipna:
            result = functions[name](data, **kwargs)
        else:
            # Use normal NumPy functions which propagate NaNs
            result = getattr(np, name)(data, **kwargs)

        # Adjust units for variance
        if name == "var":
            return Quantity(result, f"({self._dtype.units})**2")

        return Quantity(result, str(self._dtype.units))

    # Ensure pandas / numpy defer to us for ops
    __array_priority__: int = 1000

    # Arithmetic operators
    __add__: Callable[[Any, Any], Any] = _create_arithmetic_method(operator.add)
    __sub__: Callable[[Any, Any], Any] = _create_arithmetic_method(operator.sub)
    __mul__: Callable[[Any, Any], Any] = _create_arithmetic_method(operator.mul)
    __truediv__: Callable[[Any, Any], Any] = _create_arithmetic_method(operator.truediv)

    # Reverse ops
    __radd__: Callable[[Any, Any], Any] = _create_arithmetic_method(operator.add)
    __rsub__: Callable[[Any, Any], Any] = _create_arithmetic_method(operator.sub)
    __rmul__: Callable[[Any, Any], Any] = _create_arithmetic_method(operator.mul)
    __rtruediv__: Callable[[Any, Any], Any] = _create_arithmetic_method(
        operator.truediv
    )

    # Comparisons
    __eq__: Callable[[Any, Any], Any] = _create_comparison_method(operator.eq)
    __ne__: Callable[[Any, Any], Any] = _create_comparison_method(operator.ne)
    __lt__: Callable[[Any, Any], Any] = _create_comparison_method(operator.lt)
    __le__: Callable[[Any, Any], Any] = _create_comparison_method(operator.le)
    __gt__: Callable[[Any, Any], Any] = _create_comparison_method(operator.gt)
    __ge__: Callable[[Any, Any], Any] = _create_comparison_method(operator.ge)


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

    @property
    def quantity(self) -> Quantity:
        """Get the underlying Quantity."""
        if not isinstance(self._obj.array, QuantityArray):
            raise TypeError("Series must contain QuantityArray")
        return self._obj.array.quantity


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
