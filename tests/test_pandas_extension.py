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
"""Tests for pandas extension for ansys-units."""


from typing import Any, Literal

import numpy as np
from numpy.typing import NDArray
import pandas as pd
from pandas import DataFrame, Series
from pandas._typing import Scalar
from pandas.core.groupby.generic import DataFrameGroupBy
import pytest

from ansys.units import Unit
from ansys.units.extensions.pandas_extension import QuantityArray, QuantityDtype
from ansys.units.quantity import Quantity, Vector
from ansys.units.unit import (
    ProhibitedOffsetUnitOperation,
    ProhibitedTemperatureOperation,
)


class TestQuantityDtype:
    """Tests for QuantityDtype."""

    def test_create_dtype_from_string(self):
        """Test creating dtype from string."""
        dtype: QuantityDtype = QuantityDtype("m")
        assert dtype.units == Unit("m")
        assert dtype.subdtype == "Float64"

    def test_create_dtype_from_unit(self):
        """Test creating dtype from Unit object."""
        unit: Unit = Unit("kg")
        dtype: QuantityDtype = QuantityDtype(unit)
        assert dtype.units == unit

    def test_dtype_name(self):
        """Test dtype name property."""
        dtype: QuantityDtype = QuantityDtype("m")
        assert "m" in dtype.name
        assert dtype.name == "quantity[m]"

    def test_dtype_with_subdtype(self):
        """Test dtype with specified subdtype."""
        dtype: QuantityDtype = QuantityDtype("m", subdtype="float32")
        assert "float32" in dtype.name

    def test_dtype_equality(self):
        """Test dtype equality."""
        dtype1: QuantityDtype = QuantityDtype("m")
        dtype2: QuantityDtype = QuantityDtype("m")
        dtype3: QuantityDtype = QuantityDtype("kg")

        assert dtype1 == dtype2
        assert dtype1 != dtype3

    def test_dtype_hash(self):
        """Test dtype hashing."""
        dtype: QuantityDtype = QuantityDtype("m")
        # Should be hashable
        _ = hash(dtype)

    def test_construct_from_string(self):
        """Test construct_from_string classmethod."""
        dtype: QuantityDtype = QuantityDtype.construct_from_string("quantity[m]")
        assert dtype.units == Unit("m")

    def test_na_value(self):
        """Test NA value for dtype."""
        dtype: QuantityDtype = QuantityDtype("m")
        na: Quantity[float | Vector] = dtype.na_value
        assert isinstance(na, Quantity)
        # Convert to array and check for NaN
        val_array: NDArray[Any] = np.asarray(na.value)
        assert np.isnan(val_array).any() if val_array.size > 0 else np.isnan(val_array)


class TestQuantityArray:
    """Tests for QuantityArray."""

    def test_create_from_list(self):
        """Test creating QuantityArray from list."""
        arr: QuantityArray = QuantityArray([1.0, 2.0, 3.0], dtype="quantity[m]")
        assert len(arr) == 3
        assert arr.dtype == QuantityDtype("m")

    def test_create_from_quantity(self):
        """Test creating QuantityArray from Quantity."""
        q: Quantity[Vector] = Quantity([1.0, 2.0, 3.0], "m")
        arr = QuantityArray(q)
        assert len(arr) == 3

    def test_getitem_scalar(self):
        """Test getting single item."""
        arr: QuantityArray = QuantityArray([1.0, 2.0, 3.0], dtype="quantity[m]")
        item: Quantity[float | Vector] | QuantityArray = arr[0]
        assert isinstance(item, Quantity)
        assert item.value == 1.0
        assert item.units == Unit("m")

    def test_getitem_slice(self):
        """Test getting slice."""
        arr: QuantityArray = QuantityArray([1.0, 2.0, 3.0], dtype="quantity[m]")
        subset: Quantity[float | Vector] | QuantityArray = arr[0:2]
        assert isinstance(subset, QuantityArray)
        assert len(subset) == 2

    def test_setitem(self):
        """Test setting item."""
        arr: QuantityArray = QuantityArray([1.0, 2.0, 3.0], dtype="quantity[m]")
        arr[0] = 10.0
        assert arr[0].value == 10.0

    def test_setitem_with_quantity(self):
        """Test setting item with Quantity."""
        arr: QuantityArray = QuantityArray([1.0, 2.0, 3.0], dtype="quantity[m]")
        arr[0] = Quantity(100.0, "cm")
        # Should convert to meters
        assert abs(arr[0].value - 1.0) < 0.01

    def test_isna(self):
        """Test NA detection."""
        arr: QuantityArray = QuantityArray([1.0, np.nan, 3.0], dtype="quantity[m]")
        na_mask = arr.isna()
        assert not na_mask[0]
        assert na_mask[1]
        assert not na_mask[2]

    def test_take(self):
        """Test take operation."""
        arr: QuantityArray = QuantityArray([1.0, 2.0, 3.0], dtype="quantity[m]")
        result: QuantityArray = arr.take([0, 2])
        assert len(result) == 2
        assert result[0].value == 1.0
        assert result[1].value == 3.0

    def test_copy(self):
        """Test copy operation."""
        arr: QuantityArray = QuantityArray([1.0, 2.0, 3.0], dtype="quantity[m]")
        copied: QuantityArray = arr.copy()
        assert len(copied) == len(arr)
        assert copied is not arr

    def test_concat(self):
        """Test concatenation."""
        arr1: QuantityArray = QuantityArray([1.0, 2.0], dtype="quantity[m]")
        arr2: QuantityArray = QuantityArray([3.0, 4.0], dtype="quantity[m]")
        result: QuantityArray = QuantityArray._concat_same_type([arr1, arr2])
        assert len(result) == 4

    def test_from_sequence_with_quantities(self):
        """Test _from_sequence with Quantity objects."""
        quantities: list[Quantity[float]] = [
            Quantity(1.0, "m"),
            Quantity(2.0, "m"),
            Quantity(3.0, "m"),
        ]
        arr: QuantityArray = QuantityArray._from_sequence(quantities)
        assert len(arr) == 3
        assert arr.dtype.units == Unit("m")

    def test_to_different_units(self):
        """Test unit conversion."""
        arr: QuantityArray = QuantityArray([1.0, 2.0, 3.0], dtype="quantity[m]")
        converted: QuantityArray = arr.to("cm")
        assert converted[0].value == 100.0
        assert converted.dtype.units == Unit("cm")

    def test_quantity_property(self):
        """Test quantity property."""
        arr: QuantityArray = QuantityArray([1.0, 2.0, 3.0], dtype="quantity[m]")
        q: Quantity[float | Vector] = arr.quantity
        assert isinstance(q, Quantity)
        assert q.units == Unit("m")

    def test_astype_to_object(self):
        """Test conversion to object dtype."""
        arr: QuantityArray = QuantityArray([1.0, 2.0, 3.0], dtype="quantity[m]")
        obj_arr = arr.astype(object)
        assert isinstance(obj_arr[0], Quantity)

    def test_reduce_operations(self):
        """Test reduction operations."""
        arr: QuantityArray = QuantityArray([1.0, 2.0, 3.0], dtype="quantity[m]")

        # Sum
        result1: Quantity[float | Vector] = arr._reduce("sum")
        assert isinstance(result1, Quantity)
        assert result1.value == 6.0

        # Mean
        result2: Quantity[float | Vector] = arr._reduce("mean")
        assert result2.value == 2.0

        # Min/Max
        result3: Quantity[float | Vector] = arr._reduce("min")
        assert result3.value == 1.0

        result4: Quantity[float | Vector] = arr._reduce("max")
        assert result4.value == 3.0


class TestPandasIntegration:
    """Test integration with pandas Series and DataFrame."""

    def test_create_series_with_dtype_string(self):
        """Test creating Series with dtype string."""
        series: Series[float] = Series([1.0, 2.0, 3.0], dtype="quantity[m]")
        assert isinstance(series.dtype, QuantityDtype)
        assert len(series) == 3

    def test_create_series_with_dtype_object(self):
        """Test creating Series with QuantityDtype object."""
        dtype: QuantityDtype = QuantityDtype("kg")
        series: Series[float] = Series([1.0, 2.0, 3.0], dtype=dtype)
        assert series.dtype == dtype

    def test_create_dataframe(self):
        """Test creating DataFrame with quantity columns."""
        df: DataFrame = DataFrame(
            {
                "length": Series([1.0, 2.0, 3.0], dtype="quantity[m]"),
                "mass": Series([10.0, 20.0, 30.0], dtype="quantity[kg]"),
            }
        )
        assert isinstance(df["length"].dtype, QuantityDtype)
        assert isinstance(df["mass"].dtype, QuantityDtype)

    def test_series_units_accessor(self):
        """Test .units accessor on Series."""
        series: Series[float] = Series([1.0, 2.0, 3.0], dtype="quantity[m]")
        # Access the units accessor
        assert hasattr(series, "units")

    def test_series_units_to_conversion(self):
        """Test unit conversion via accessor."""
        series: Series = Series([1.0, 2.0, 3.0], dtype="quantity[m]")
        converted: Series = series.units.to("cm")
        assert converted[0] == Quantity(100.0, "cm")
        assert converted.dtype.units == Unit("cm")

    def test_series_units_quantity_property(self):
        """Test quantity property via accessor."""
        series: Series = Series([1.0, 2.0, 3.0], dtype="quantity[m]")
        q: Quantity = series.units.quantity
        assert isinstance(q, Quantity)
        assert q.units == Unit("m")

    def test_dataframe_units_accessor(self):
        """Test .units accessor on DataFrame."""
        df: DataFrame = DataFrame(
            {
                "length": Series([1.0, 2.0], dtype="quantity[m]"),
                "mass": Series([10.0, 20.0], dtype="quantity[kg]"),
            }
        )
        assert hasattr(df, "units")

    def test_dataframe_units_summary(self):
        """Test units summary."""
        df: DataFrame = DataFrame(
            {
                "length": Series([1.0, 2.0], dtype="quantity[m]"),
                "mass": Series([10.0, 20.0], dtype="quantity[kg]"),
                "count": Series([1, 2]),  # No units
            }
        )
        summary = df.units.summary()
        assert "length" in summary
        assert "mass" in summary
        assert "count" not in summary
        assert summary["length"] == "m"
        assert summary["mass"] == "kg"

    def test_dataframe_units_to_conversion(self):
        """Test unit conversion on DataFrame columns."""
        df: DataFrame = DataFrame(
            {
                "length": Series([1.0, 2.0], dtype="quantity[m]"),
                "mass": Series([1.0, 2.0], dtype="quantity[kg]"),
            }
        )
        converted: DataFrame = df.units.to({"length": "cm", "mass": "g"})
        assert converted["length"].dtype.units == Unit("cm")
        assert converted["mass"].dtype.units == Unit("g")

    def test_series_operations(self):
        """Test arithmetic operations on Series."""
        s1: Series = Series([1.0, 2.0, 3.0], dtype="quantity[m]")
        s2: Series = Series([100.0, 200.0, 300.0], dtype="quantity[cm]")

        result = s1 + s2
        assert isinstance(result.dtype, QuantityDtype)
        assert result.dtype.units == Unit("m")
        assert result.units.quantity.value.tolist() == [2.0, 4.0, 6.0]

        doubled = s1 * 2
        assert doubled.units.quantity.value.tolist() == [2.0, 4.0, 6.0]

    def test_indexing_and_slicing(self):
        """Test indexing operations."""
        series: Series[float] = Series([1.0, 2.0, 3.0, 4.0, 5.0], dtype="quantity[m]")

        # Single item
        item: float = series.iloc[0]
        assert isinstance(item, Quantity)

        # Slice
        subset: Series[float] = series.iloc[1:3]
        assert len(subset) == 2
        assert isinstance(subset.dtype, QuantityDtype)

    def test_concat_series(self):
        """Test concatenating series."""
        s1: Series[float] = Series([1.0, 2.0], dtype="quantity[m]")
        s2: Series[float] = Series([3.0, 4.0], dtype="quantity[m]")

        result: Series[float] = pd.concat([s1, s2], ignore_index=True)
        assert len(result) == 4
        assert isinstance(result.dtype, QuantityDtype)

    def test_groupby_operations(self):
        """Test groupby with quantity columns."""
        df: DataFrame = DataFrame(
            {
                "group": ["A", "A", "B", "B"],
                "value": Series([1.0, 2.0, 3.0, 4.0], dtype="quantity[m]"),
            }
        )

        # Groupby should work
        grouped: DataFrameGroupBy[Scalar, Literal[True]] = df.groupby("group")
        # Basic operations
        _ = grouped.size()

    def test_nan_handling(self):
        """Test handling of NaN values."""
        series: Series[float] = Series([1.0, np.nan, 3.0], dtype="quantity[m]")
        assert series.isna()[1]
        assert not series.isna()[0]

    def test_dtype_preservation(self):
        """Test that dtype is preserved through operations."""
        df: DataFrame = DataFrame({"a": Series([1.0, 2.0, 3.0], dtype="quantity[m]")})

        # Select column
        col: Series[float] = df["a"]
        assert isinstance(col.dtype, QuantityDtype)

        # Reset index
        df_reset: DataFrame = df.reset_index(drop=True)
        assert isinstance(df_reset["a"].dtype, QuantityDtype)


class TestEdgeCases:
    """Test edge cases."""

    def test_empty_array(self):
        """Test creating empty array."""
        arr: QuantityArray = QuantityArray([], dtype="quantity[m]")
        assert len(arr) == 0

    def test_single_element_array(self):
        """Test single element array."""
        arr: QuantityArray = QuantityArray([5.0], dtype="quantity[m]")
        assert len(arr) == 1
        assert arr[0].value == 5.0

    def test_mixed_unit_conversion(self):
        """Test converting array with different source units."""
        quantities: list[Quantity[float]] = [
            Quantity(1.0, "m"),
            Quantity(100.0, "cm"),
            Quantity(1000.0, "mm"),
        ]
        arr: QuantityArray = QuantityArray._from_sequence(quantities)
        # All should be normalized to first unit
        assert arr.dtype.units == Unit("m")

    def test_incompatible_units_error(self):
        """Test that incompatible units raise errors."""
        # This should work - same dimension
        arr: QuantityArray = QuantityArray([1.0, 2.0], dtype="quantity[m]")
        arr.to("ft")  # Length to length

        # This should fail - different dimensions
        with pytest.raises(Exception):  # Will raise some error from Quantity.to()
            arr.to("kg")  # Length to mass


class TestDocExamples:
    """Test examples from documentation."""

    def test_basic_usage_example(self):
        """Test basic usage example."""
        # Create a Series with units
        distances: Series = Series([1.0, 2.0, 3.0], dtype="quantity[m]")
        assert len(distances) == 3

        # Convert units
        distances_ft: Any = distances.units.to("ft")
        assert distances_ft.dtype.units == Unit("ft")

    def test_dataframe_example(self):
        """Test DataFrame example."""
        df: DataFrame = DataFrame(
            {
                "torque": Series([1.0, 2.0, 3.0], dtype="quantity[N m]"),
                "force": Series([10.0, 20.0, 30.0], dtype="quantity[N]"),
            }
        )

        assert isinstance(df["torque"].dtype, QuantityDtype)
        assert isinstance(df["force"].dtype, QuantityDtype)

        # Check units
        summary: Any = df.units.summary()
        assert "torque" in summary
        assert "force" in summary


class TestQuantityDtypeDetails:
    """Tests for less common QuantityDtype paths."""

    def test_dtype_from_dtype_returns_same_instance(self):
        dtype = QuantityDtype("m")
        assert QuantityDtype(dtype) is dtype

    def test_empty_dtype_for_pickling(self):
        dtype = QuantityDtype()
        assert isinstance(dtype, QuantityDtype)
        assert dtype.units is None

    def test_dtype_properties(self):
        dtype = QuantityDtype("m")
        assert dtype._is_numeric is True
        assert repr(dtype) == "quantity[m]"

    def test_dtype_equality_with_strings_and_other_objects(self):
        dtype = QuantityDtype("m")
        assert dtype == "quantity[m]"
        assert dtype != "not_a_unit_xyz"
        assert dtype != 5


class TestQuantityArrayDetails:
    """Tests for less common QuantityArray paths."""

    def test_construct_from_quantity_array(self):
        arr = QuantityArray([1.0, 2.0], dtype="quantity[m]")
        assert list(QuantityArray(arr).quantity.value) == [1.0, 2.0]

        # Re-wrapping with other units converts the values.
        in_cm = QuantityArray(arr, dtype="quantity[cm]")
        assert in_cm.dtype.units == Unit("cm")
        assert list(in_cm.quantity.value) == [100.0, 200.0]

    def test_construct_without_dtype_or_quantity_raises(self):
        with pytest.raises(ValueError, match="Must specify dtype"):
            QuantityArray([1.0, 2.0])
        with pytest.raises(ValueError, match="Cannot infer dtype"):
            QuantityArray._from_sequence([1.0, 2.0])

    def test_getitem_missing_value(self):
        arr = QuantityArray([np.nan, 1.0], dtype="quantity[m]")
        assert pd.isna(arr[0])
        assert arr[1] == Quantity(1.0, "m")

    def test_take_with_quantity_fill_value(self):
        arr = QuantityArray([1.0, 2.0], dtype="quantity[m]")
        result = arr.take([0, -1], allow_fill=True, fill_value=Quantity(500, "cm"))
        assert list(result.quantity.value) == [1.0, 5.0]

    def test_deep_copy(self):
        arr = QuantityArray([1.0, 2.0], dtype="quantity[m]")
        copied = arr.copy(deep=True)
        copied[0] = Quantity(9.0, "m")
        assert arr[0] == Quantity(1.0, "m")

    def test_factorize(self):
        series = Series(QuantityArray([1.0, 1.0, 2.0], dtype="quantity[m]"))
        codes, uniques = series.factorize()
        assert list(codes) == [0, 0, 1]
        assert uniques.dtype == QuantityDtype("m")
        assert len(uniques) == 2

    def test_astype(self):
        arr = QuantityArray([1.0, 2.0], dtype="quantity[m]")

        assert arr.astype(arr.dtype, copy=False) is arr
        in_cm = arr.astype("quantity[cm]")
        assert list(in_cm.quantity.value) == [100.0, 200.0]

        as_strings = arr.astype(str)
        assert list(as_strings) == ["1.0 m", "2.0 m"]

        as_floats = arr.astype("float64")
        assert list(as_floats) == [1.0, 2.0]

    def test_numpy_conversion(self):
        arr = QuantityArray([1.0, 2.0], dtype="quantity[m]")
        as_objects = np.asarray(arr)
        assert as_objects.dtype == object
        assert as_objects[0] == Quantity(1.0, "m")
        assert np.asarray(arr, dtype=float).tolist() == [1.0, 2.0]

    def test_arithmetic(self):
        a = QuantityArray([1.0, 2.0, 3.0], dtype="quantity[m]")
        b = QuantityArray([100.0, 200.0, 300.0], dtype="quantity[cm]")

        assert list((a + b).quantity.value) == [2.0, 4.0, 6.0]
        assert list((a - Quantity(1.0, "m")).quantity.value) == [0.0, 1.0, 2.0]
        assert list((a * 2).quantity.value) == [2.0, 4.0, 6.0]
        assert list((2 * a).quantity.value) == [2.0, 4.0, 6.0]
        assert list((a * np.array([1.0, 2.0, 3.0])).quantity.value) == [1.0, 4.0, 9.0]
        assert (a / Quantity(1.0, "s")).dtype.units == Unit("m s^-1")

        # Reflected operations keep the operand order.
        ratio = QuantityArray([1.0, 2.0], dtype=QuantityDtype(Unit("")))
        assert list((10 - ratio).quantity.value) == [9.0, 8.0]
        assert list((6 / ratio).quantity.value) == [6.0, 3.0]
        assert (6 / ratio).dtype == QuantityDtype(Unit(""))

    def test_arithmetic_with_unsupported_operands(self):
        a = QuantityArray([1.0, 2.0], dtype="quantity[m]")
        assert a.__add__(Series([1.0, 2.0])) is NotImplemented
        with pytest.raises(TypeError):
            a / "x"

    def test_comparisons_are_element_wise(self):
        a = QuantityArray([1.0, 2.0, 3.0], dtype="quantity[m]")
        b = QuantityArray([100.0, 250.0, 300.0], dtype="quantity[cm]")

        assert (a == b).tolist() == [True, False, True]
        assert (a != b).tolist() == [False, True, False]
        assert (a < Quantity(2.5, "m")).tolist() == [True, True, False]
        assert (a >= b).tolist() == [True, False, True]
        assert a.__eq__(Series([1.0, 2.0, 3.0])) is NotImplemented

    def test_reductions(self):
        series = Series([1.0, 2.0, 3.0, 10.0], dtype="quantity[m]")
        assert series.sum(skipna=False) == Quantity(16.0, "m")
        assert series.median() == Quantity(2.5, "m")
        assert series.var().units == Unit("m^2")
        assert series.std().units == Unit("m")
        assert series.std(ddof=0).value == pytest.approx(np.std([1, 2, 3, 10]))
        assert series.sem().units == Unit("m")
        with pytest.raises(TypeError, match="any"):
            series.any()

    def test_shape_statistics_have_no_units(self):
        series = Series([1.0, 2.0, 4.0, 8.0], dtype="quantity[m]")
        assert series.skew() == pytest.approx(Series([1.0, 2.0, 4.0, 8.0]).skew())
        assert series.kurt() == pytest.approx(Series([1.0, 2.0, 4.0, 8.0]).kurt())
        assert np.isnan(Series([1.0, 2.0], dtype="quantity[m]").skew())

    def test_product_units_depend_on_the_number_of_values(self):
        series = Series([1.0, 2.0, np.nan, 4.0], dtype="quantity[m]")
        assert series.prod() == Quantity(8.0, "m^3")
        assert series.prod(skipna=False).units == Unit("m^4")
        with pytest.raises(ProhibitedOffsetUnitOperation):
            Series([1.0, 2.0], dtype="quantity[C]").prod()

    def test_cumulative_product_needs_dimensionless_values(self):
        ratios = Series([2.0, 3.0, 4.0], dtype="quantity[]")
        assert ratios.dtype == QuantityDtype(Unit(""))
        assert ratios.prod() == Quantity(24.0, "")
        assert ratios.cumprod().tolist() == [
            Quantity(2.0, ""),
            Quantity(6.0, ""),
            Quantity(24.0, ""),
        ]
        with pytest.raises(TypeError, match="different units"):
            Series([2.0, 3.0], dtype="quantity[m]").cumprod()

    def test_reductions_of_empty_and_missing_values(self):
        assert Series([], dtype="quantity[m]").sum() == Quantity(0.0, "m")
        assert np.isnan(Series([], dtype="quantity[m]").mean().value)
        result = Series([np.nan], dtype="quantity[m]").sum(min_count=1)
        assert result.units == Unit("m") and np.isnan(result.value)

    def test_dataframe_reductions_keep_units(self):
        df = DataFrame(
            {
                "L": Series([1.0, 2.0, np.nan], dtype="quantity[m]"),
                "M": Series([1.0, 2.0, 3.0], dtype="quantity[kg]"),
            }
        )
        assert df.sum().tolist() == [Quantity(3.0, "m"), Quantity(6.0, "kg")]
        assert df.mean().tolist() == [Quantity(1.5, "m"), Quantity(2.0, "kg")]
        assert df.max().tolist() == [Quantity(2.0, "m"), Quantity(3.0, "kg")]
        assert df.std()["M"].units == Unit("kg")
        # Shape statistics have no units, also with ``keepdims``.
        skew = df.skew()
        assert np.isnan(skew["L"]) and skew["M"] == pytest.approx(0.0)

    def test_temperature_spread_is_a_difference(self):
        series = Series([10.0, 20.0], dtype="quantity[C]")
        assert series.std().units == Unit("delta_C")
        assert series.var().units == Unit("delta_C^2")
        assert series.var().value == pytest.approx(50.0)
        assert series.mean() == Quantity(15.0, "C")

    def test_absolute_temperatures_cannot_be_summed(self):
        series = Series([10.0, 20.0], dtype="quantity[C]")
        with pytest.raises(ProhibitedTemperatureOperation):
            series.sum()
        with pytest.raises(ProhibitedTemperatureOperation):
            series.cumsum()
        deltas = Series([10.0, 20.0], dtype="quantity[delta_C]")
        assert deltas.sum() == Quantity(30.0, "delta_C")


class TestPandasOperations:
    """Tests for pandas operations on unit-aware Series and DataFrames."""

    def test_copy_and_fillna_do_not_modify_the_original(self):
        series = Series([1.0, np.nan], dtype="quantity[m]")
        filled = series.fillna(Quantity(0.0, "m"))
        assert filled[1] == Quantity(0.0, "m")
        assert pd.isna(series[1])

        copied = series.copy()
        copied.iloc[0] = Quantity(9.0, "m")
        assert series[0] == Quantity(1.0, "m")

        arr = series.array
        assert arr.copy(deep=False)._data is not arr._data

    def test_unique_values(self):
        series = Series([1.0, 2.0, 2.0, np.nan], dtype="quantity[m]")
        uniques = series.unique()
        assert isinstance(uniques, QuantityArray)
        assert len(uniques) == 3
        assert series.nunique() == 2
        assert series.drop_duplicates().tolist()[:2] == [
            Quantity(1.0, "m"),
            Quantity(2.0, "m"),
        ]

    def test_cumulative_operations(self):
        series = Series([1.0, 3.0, 2.0], dtype="quantity[m]")
        assert series.cumsum().tolist() == [
            Quantity(1.0, "m"),
            Quantity(4.0, "m"),
            Quantity(6.0, "m"),
        ]
        assert series.cummax().tolist()[-1] == Quantity(3.0, "m")
        assert series.cummin().dtype == QuantityDtype("m")
        with pytest.raises(TypeError, match="cumprod"):
            series.cumprod()
        with pytest.raises(TypeError, match="diff"):
            series.array._accumulate("diff")

    def test_unary_operations_and_round(self):
        series = Series([-1.25, 2.5], dtype="quantity[m]")
        assert (-series).tolist() == [Quantity(1.25, "m"), Quantity(-2.5, "m")]
        assert (+series).tolist() == series.tolist()
        assert abs(series).dtype == QuantityDtype("m")
        assert abs(series).tolist()[0] == Quantity(1.25, "m")
        assert series.round(1).tolist()[0] == Quantity(-1.2, "m")

    def test_concat_with_compatible_units_converts(self):
        meters = Series([1.0], dtype="quantity[m]")
        centimeters = Series([250.0], dtype="quantity[cm]")
        combined = pd.concat([meters, centimeters], ignore_index=True)
        assert combined.dtype == QuantityDtype("m")
        assert combined.tolist() == [Quantity(1.0, "m"), Quantity(2.5, "m")]

    def test_concat_with_incompatible_units_is_object(self):
        combined = pd.concat(
            [Series([1.0], dtype="quantity[m]"), Series([2.0], dtype="quantity[kg]")]
        )
        assert combined.dtype == object

    def test_groupby_aggregations_keep_units(self):
        df = DataFrame(
            {
                "g": [1, 1, 2, 2],
                "length": Series([1.0, 3.0, 5.0, 6.0], dtype="quantity[m]"),
            }
        )
        grouped = df.groupby("g")["length"]
        assert grouped.sum().tolist() == [Quantity(4.0, "m"), Quantity(11.0, "m")]
        assert grouped.mean().dtype == QuantityDtype("m")
        assert grouped.var().dtype == QuantityDtype("m^2")
        assert grouped.std().dtype == QuantityDtype("m")
        assert grouped.cumsum().tolist()[1] == Quantity(4.0, "m")
        assert grouped.count().tolist() == [2, 2]
        # Ranks have no units.
        assert grouped.rank().tolist() == [1.0, 2.0, 1.0, 2.0]
        with pytest.raises(TypeError, match="different units"):
            grouped.prod()

    def test_groupby_products_and_shape_statistics(self):
        df = DataFrame(
            {
                "g": [1, 1, 1, 2],
                "ratio": Series([2.0, 3.0, 4.0, 5.0], dtype="quantity[]"),
            }
        )
        grouped = df.groupby("g")["ratio"]
        assert grouped.prod().tolist() == [Quantity(24.0, ""), Quantity(5.0, "")]
        assert grouped.cumprod().tolist()[2] == Quantity(24.0, "")
        skew = grouped.skew()
        assert not isinstance(skew.dtype, QuantityDtype)
        assert skew.iloc[0] == pytest.approx(0.0)

    def test_groupby_on_temperatures(self):
        df = DataFrame({"g": [1, 1], "T": Series([10.0, 20.0], dtype="quantity[C]")})
        grouped = df.groupby("g")["T"]
        assert grouped.mean().tolist() == [Quantity(15.0, "C")]
        assert grouped.std().dtype == QuantityDtype("delta_C")
        assert grouped.var().dtype == QuantityDtype("delta_C^2")
        with pytest.raises(ProhibitedTemperatureOperation):
            grouped.sum()

    def test_describe_keeps_units(self):
        series = Series([1.0, 2.0, np.nan, 4.0], dtype="quantity[m]", name="L")
        stats = series.units.describe()
        assert stats["count"] == 3
        assert stats["min"] == Quantity(1.0, "m")
        assert stats["50%"] == Quantity(2.0, "m")
        assert stats["max"] == Quantity(4.0, "m")
        assert stats.name == "L"

        temperatures = Series([10.0, 20.0], dtype="quantity[C]")
        assert temperatures.units.describe()["std"].units == Unit("delta_C")

    def test_dataframe_describe_keeps_units(self):
        df = DataFrame(
            {
                "L": Series([1.0, 2.0], dtype="quantity[m]"),
                "n": [1, 2],
            }
        )
        stats = df.units.describe(percentiles=(0.125,))
        assert list(stats.columns) == ["L"]
        assert list(stats.index) == ["count", "mean", "std", "min", "12.5%", "max"]
        assert stats.loc["mean", "L"] == Quantity(1.5, "m")

    def test_windows_keep_units(self):
        series = Series([1.0, 2.0, np.nan, 4.0], dtype="quantity[m]")

        mean = series.units.rolling(2).mean()
        assert mean.dtype == QuantityDtype("m")
        assert mean[1] == Quantity(1.5, "m")
        assert pd.isna(mean[0])
        assert series.units.rolling(2).std().dtype == QuantityDtype("m")
        assert series.units.rolling(2, min_periods=1).var().dtype == QuantityDtype(
            "m^2"
        )
        assert series.units.expanding().max().tolist()[-1] == Quantity(4.0, "m")
        assert series.units.ewm(span=2).mean().dtype == QuantityDtype("m")

        # Results whose units can't be determined are plain floats.
        counts = series.units.rolling(2, min_periods=1).count()
        assert counts.tolist() == [1.0, 2.0, 1.0, 1.0]
        applied = series.units.rolling(2).apply(np.sum, raw=True)
        assert applied.dtype == np.float64
        # Window attributes pass through.
        assert series.units.rolling(3).window == 3

    def test_windows_on_temperatures(self):
        temperatures = Series([10.0, 20.0, 40.0], dtype="quantity[C]")
        assert temperatures.units.rolling(2).mean().dtype == QuantityDtype("C")
        assert temperatures.units.rolling(2).std().dtype == QuantityDtype("delta_C")
        with pytest.raises(ProhibitedTemperatureOperation):
            temperatures.units.rolling(2).sum()

    def test_builtin_windows_handle_missing_values(self):
        series = Series([1.0, 2.0, np.nan, 4.0], dtype="quantity[m]")
        assert series.rolling(2).mean().tolist()[1] == 1.5

    def test_to_numpy(self):
        arr = Series([1.0, np.nan], dtype="quantity[m]").array
        floats = arr.to_numpy(dtype="float64", na_value=np.nan)
        assert floats[0] == 1.0 and np.isnan(floats[1])
        objects = arr.to_numpy()
        assert objects[0] == Quantity(1.0, "m") and pd.isna(objects[1])
        assert arr.to_numpy(na_value=None)[1] is None


class TestAccessorErrors:
    """Tests for accessor error handling."""

    def test_accessor_requires_quantity_dtype(self):
        with pytest.raises(AttributeError, match="QuantityDtype"):
            Series([1.0, 2.0]).units

    def test_accessor_requires_quantity_array(self):
        from types import SimpleNamespace

        from ansys.units.extensions.pandas_extension import UnitsSeriesAccessor

        fake_series = SimpleNamespace(dtype=QuantityDtype("m"), array=[1.0, 2.0])
        accessor = UnitsSeriesAccessor(fake_series)
        with pytest.raises(TypeError, match="QuantityArray"):
            accessor.to("cm")
        with pytest.raises(TypeError, match="QuantityArray"):
            accessor.quantity


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
