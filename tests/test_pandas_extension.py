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

from typing import Any

import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import pytest

from ansys.units import Quantity, Unit
from ansys.units.extensions.pandas_extension import QuantityArray, QuantityDtype


class TestQuantityDtype:
    """Tests for QuantityDtype."""

    def test_create_dtype_from_string(self):
        """Test creating dtype from string."""
        dtype = QuantityDtype("m")
        assert dtype.units == Unit("m")
        assert dtype.subdtype == "Float64"

    def test_create_dtype_from_unit(self):
        """Test creating dtype from Unit object."""
        unit = Unit("kg")
        dtype = QuantityDtype(unit)
        assert dtype.units == unit

    def test_dtype_name(self):
        """Test dtype name property."""
        dtype = QuantityDtype("m")
        assert "m" in dtype.name
        assert dtype.name == "quantity[m]"

    def test_dtype_with_subdtype(self):
        """Test dtype with specified subdtype."""
        dtype = QuantityDtype("m", subdtype="float32")
        assert "float32" in dtype.name

    def test_dtype_equality(self):
        """Test dtype equality."""
        dtype1 = QuantityDtype("m")
        dtype2 = QuantityDtype("m")
        dtype3 = QuantityDtype("kg")

        assert dtype1 == dtype2
        assert dtype1 != dtype3

    def test_dtype_hash(self):
        """Test dtype hashing."""
        dtype = QuantityDtype("m")
        # Should be hashable
        _ = hash(dtype)

    def test_construct_from_string(self):
        """Test construct_from_string classmethod."""
        dtype = QuantityDtype.construct_from_string("quantity[m]")
        assert dtype.units == Unit("m")

    def test_na_value(self):
        """Test NA value for dtype."""
        dtype = QuantityDtype("m")
        na = dtype.na_value
        assert isinstance(na, Quantity)
        # Convert to array and check for NaN
        val_array = np.asarray(na.value)
        assert np.isnan(val_array).any() if val_array.size > 0 else np.isnan(val_array)


class TestQuantityArray:
    """Tests for QuantityArray."""

    def test_create_from_list(self):
        """Test creating QuantityArray from list."""
        arr = QuantityArray([1.0, 2.0, 3.0], dtype="quantity[m]")
        assert len(arr) == 3
        assert arr.dtype == QuantityDtype("m")

    def test_create_from_quantity(self):
        """Test creating QuantityArray from Quantity."""
        q = Quantity([1.0, 2.0, 3.0], "m")  # type: ignore[arg-type]
        arr = QuantityArray(q)
        assert len(arr) == 3

    def test_getitem_scalar(self):
        """Test getting single item."""
        arr = QuantityArray([1.0, 2.0, 3.0], dtype="quantity[m]")
        item = arr[0]
        assert isinstance(item, Quantity)
        assert item.value == 1.0
        assert item.units == Unit("m")

    def test_getitem_slice(self):
        """Test getting slice."""
        arr = QuantityArray([1.0, 2.0, 3.0], dtype="quantity[m]")
        subset = arr[0:2]
        assert isinstance(subset, QuantityArray)
        assert len(subset) == 2

    def test_setitem(self):
        """Test setting item."""
        arr = QuantityArray([1.0, 2.0, 3.0], dtype="quantity[m]")
        arr[0] = 10.0
        assert arr[0].value == 10.0

    def test_setitem_with_quantity(self):
        """Test setting item with Quantity."""
        arr = QuantityArray([1.0, 2.0, 3.0], dtype="quantity[m]")
        arr[0] = Quantity(100.0, "cm")
        # Should convert to meters
        assert abs(arr[0].value - 1.0) < 0.01

    def test_isna(self):
        """Test NA detection."""
        arr = QuantityArray([1.0, np.nan, 3.0], dtype="quantity[m]")  # type: ignore[list-item]
        na_mask = arr.isna()
        assert not na_mask[0]
        assert na_mask[1]
        assert not na_mask[2]

    def test_take(self):
        """Test take operation."""
        arr = QuantityArray([1.0, 2.0, 3.0], dtype="quantity[m]")
        result = arr.take([0, 2])
        assert len(result) == 2
        assert result[0].value == 1.0
        assert result[1].value == 3.0

    def test_copy(self):
        """Test copy operation."""
        arr = QuantityArray([1.0, 2.0, 3.0], dtype="quantity[m]")
        copied = arr.copy()
        assert len(copied) == len(arr)
        assert copied is not arr

    def test_concat(self):
        """Test concatenation."""
        arr1 = QuantityArray([1.0, 2.0], dtype="quantity[m]")
        arr2 = QuantityArray([3.0, 4.0], dtype="quantity[m]")
        result = QuantityArray._concat_same_type([arr1, arr2])
        assert len(result) == 4

    def test_from_sequence_with_quantities(self):
        """Test _from_sequence with Quantity objects."""
        quantities = [Quantity(1.0, "m"), Quantity(2.0, "m"), Quantity(3.0, "m")]
        arr = QuantityArray._from_sequence(quantities)
        assert len(arr) == 3
        assert arr.dtype.units == Unit("m")

    def test_to_different_units(self):
        """Test unit conversion."""
        arr = QuantityArray([1.0, 2.0, 3.0], dtype="quantity[m]")
        converted = arr.to("cm")
        assert converted[0].value == 100.0
        assert converted.dtype.units == Unit("cm")

    def test_quantity_property(self):
        """Test quantity property."""
        arr = QuantityArray([1.0, 2.0, 3.0], dtype="quantity[m]")
        q = arr.quantity
        assert isinstance(q, Quantity)
        assert q.units == Unit("m")

    def test_astype_to_object(self):
        """Test conversion to object dtype."""
        arr = QuantityArray([1.0, 2.0, 3.0], dtype="quantity[m]")
        obj_arr = arr.astype(object)
        assert isinstance(obj_arr[0], Quantity)

    def test_reduce_operations(self):
        """Test reduction operations."""
        arr = QuantityArray([1.0, 2.0, 3.0], dtype="quantity[m]")

        # Sum
        result = arr._reduce("sum")
        assert isinstance(result, Quantity)
        assert result.value == 6.0

        # Mean
        result = arr._reduce("mean")
        assert result.value == 2.0

        # Min/Max
        result = arr._reduce("min")
        assert result.value == 1.0

        result = arr._reduce("max")
        assert result.value == 3.0


class TestPandasIntegration:
    """Test integration with pandas Series and DataFrame."""

    def test_create_series_with_dtype_string(self):
        """Test creating Series with dtype string."""
        series = Series([1.0, 2.0, 3.0], dtype="quantity[m]")
        assert isinstance(series.dtype, QuantityDtype)
        assert len(series) == 3

    def test_create_series_with_dtype_object(self):
        """Test creating Series with QuantityDtype object."""
        dtype = QuantityDtype("kg")
        series = Series([1.0, 2.0, 3.0], dtype=dtype)
        assert series.dtype == dtype

    def test_create_dataframe(self):
        """Test creating DataFrame with quantity columns."""
        df = DataFrame(
            {
                "length": Series([1.0, 2.0, 3.0], dtype="quantity[m]"),
                "mass": Series([10.0, 20.0, 30.0], dtype="quantity[kg]"),
            }
        )
        assert isinstance(df["length"].dtype, QuantityDtype)
        assert isinstance(df["mass"].dtype, QuantityDtype)

    def test_series_units_accessor(self):
        """Test .units accessor on Series."""
        series = Series([1.0, 2.0, 3.0], dtype="quantity[m]")
        # Access the units accessor
        assert hasattr(series, "units")

    def test_series_units_to_conversion(self):
        """Test unit conversion via accessor."""
        series = Series([1.0, 2.0, 3.0], dtype="quantity[m]")
        converted = series.units.to("cm")
        assert converted[0] == Quantity(100.0, "cm")
        assert converted.dtype.units == Unit("cm")

    def test_series_units_quantity_property(self):
        """Test quantity property via accessor."""
        series = Series([1.0, 2.0, 3.0], dtype="quantity[m]")
        q = series.units.quantity
        assert isinstance(q, Quantity)
        assert q.units == Unit("m")

    def test_dataframe_units_accessor(self):
        """Test .units accessor on DataFrame."""
        df = DataFrame(
            {
                "length": Series([1.0, 2.0], dtype="quantity[m]"),
                "mass": Series([10.0, 20.0], dtype="quantity[kg]"),
            }
        )
        assert hasattr(df, "units")

    def test_dataframe_units_summary(self):
        """Test units summary."""
        df = DataFrame(
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
        df = DataFrame(
            {
                "length": Series([1.0, 2.0], dtype="quantity[m]"),
                "mass": Series([1.0, 2.0], dtype="quantity[kg]"),
            }
        )
        converted = df.units.to({"length": "cm", "mass": "g"})
        assert converted["length"].dtype.units == Unit("cm")
        assert converted["mass"].dtype.units == Unit("g")

    def test_series_operations(self):
        """Test arithmetic operations on Series."""
        s1 = Series([1.0, 2.0, 3.0], dtype="quantity[m]")
        s2 = Series([1.0, 2.0, 3.0], dtype="quantity[m]")

        # Addition (not yet implemented but structure exists)
        # result = s1 + s2
        # assert isinstance(result.dtype, QuantityDtype)

    def test_indexing_and_slicing(self):
        """Test indexing operations."""
        series = Series([1.0, 2.0, 3.0, 4.0, 5.0], dtype="quantity[m]")

        # Single item
        item = series.iloc[0]
        assert isinstance(item, Quantity)

        # Slice
        subset = series.iloc[1:3]
        assert len(subset) == 2
        assert isinstance(subset.dtype, QuantityDtype)

    def test_concat_series(self):
        """Test concatenating series."""
        s1 = Series([1.0, 2.0], dtype="quantity[m]")
        s2 = Series([3.0, 4.0], dtype="quantity[m]")

        result = pd.concat([s1, s2], ignore_index=True)
        assert len(result) == 4
        assert isinstance(result.dtype, QuantityDtype)

    def test_groupby_operations(self):
        """Test groupby with quantity columns."""
        df = DataFrame(
            {
                "group": ["A", "A", "B", "B"],
                "value": Series([1.0, 2.0, 3.0, 4.0], dtype="quantity[m]"),
            }
        )

        # Groupby should work
        grouped = df.groupby("group")
        # Basic operations
        _ = grouped.size()

    def test_nan_handling(self):
        """Test handling of NaN values."""
        series = Series([1.0, np.nan, 3.0], dtype="quantity[m]")  # type: ignore[list-item]
        assert series.isna()[1]
        assert not series.isna()[0]

    def test_dtype_preservation(self):
        """Test that dtype is preserved through operations."""
        df: DataFrame = DataFrame({"a": Series([1.0, 2.0, 3.0], dtype="quantity[m]")})

        # Select column
        col = df["a"]
        assert isinstance(col.dtype, QuantityDtype)

        # Reset index
        df_reset = df.reset_index(drop=True)
        assert isinstance(df_reset["a"].dtype, QuantityDtype)


class TestEdgeCases:
    """Test edge cases."""

    def test_empty_array(self):
        """Test creating empty array."""
        arr = QuantityArray([], dtype="quantity[m]")
        assert len(arr) == 0

    def test_single_element_array(self):
        """Test single element array."""
        arr = QuantityArray([5.0], dtype="quantity[m]")
        assert len(arr) == 1
        assert arr[0].value == 5.0

    def test_mixed_unit_conversion(self):
        """Test converting array with different source units."""
        quantities = [
            Quantity(1.0, "m"),
            Quantity(100.0, "cm"),
            Quantity(1000.0, "mm"),
        ]
        arr = QuantityArray._from_sequence(quantities)
        # All should be normalized to first unit
        assert arr.dtype.units == Unit("m")

    def test_incompatible_units_error(self):
        """Test that incompatible units raise errors."""
        # This should work - same dimension
        arr = QuantityArray([1.0, 2.0], dtype="quantity[m]")
        arr.to("ft")  # Length to length

        # This should fail - different dimensions
        with pytest.raises(Exception):  # Will raise some error from Quantity.to()
            arr.to("kg")  # Length to mass


class TestDocExamples:
    """Test examples from documentation."""

    def test_basic_usage_example(self):
        """Test basic usage example."""
        # Create a Series with units
        distances = Series([1.0, 2.0, 3.0], dtype="quantity[m]")
        assert len(distances) == 3

        # Convert units
        distances_ft: Any = distances.units.to("ft")
        assert distances_ft.dtype.units == Unit("ft")

    def test_dataframe_example(self):
        """Test DataFrame example."""
        df = DataFrame(
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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
