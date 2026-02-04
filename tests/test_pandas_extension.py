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

import importlib.util
from typing import Any

from _pytest.mark.structures import MarkDecorator
import numpy as np
from numpy import ndarray
from numpy._typing._array_like import NDArray
from pandas.core.frame import DataFrame
from pandas.core.groupby.generic import DataFrameGroupBy
from pandas.core.series import Series
import pytest

from ansys.units import Quantity, Unit
from ansys.units.extensions.pandas_extension import QuantityArray, QuantityDtype
from ansys.units.quantity import Quantity, Vector
from ansys.units.unit import Unit

# Check if pandas is available
HAS_PANDAS = importlib.util.find_spec(name="pandas") is not None

if HAS_PANDAS:
    import pandas as pd  # type: ignore[import-not-found]

    from ansys.units.extensions.pandas_extension import QuantityArray, QuantityDtype

pytestmark: MarkDecorator = pytest.mark.skipif(
    condition=not HAS_PANDAS, reason="pandas not available"
)


class TestQuantityDtype:
    """Tests for QuantityDtype."""

    def test_create_dtype_from_string(self) -> None:
        """Test creating dtype from string."""
        dtype: QuantityDtype = QuantityDtype(units="m")
        assert dtype.units == Unit("m")
        assert dtype.subdtype == "Float64"

    def test_create_dtype_from_unit(self) -> None:
        """Test creating dtype from Unit object."""
        unit: Unit = Unit(units="kg")
        dtype: QuantityDtype = QuantityDtype(units=unit)
        assert dtype.units == unit

    def test_dtype_name(self) -> None:
        """Test dtype name property."""
        dtype: QuantityDtype = QuantityDtype(units="m")
        assert "m" in dtype.name
        assert dtype.name == "quantity[m]"

    def test_dtype_with_subdtype(self) -> None:
        """Test dtype with specified subdtype."""
        dtype: QuantityDtype = QuantityDtype(units="m", subdtype="float32")
        assert "float32" in dtype.name

    def test_dtype_equality(self) -> None:
        """Test dtype equality."""
        dtype1: QuantityDtype = QuantityDtype(units="m")
        dtype2: QuantityDtype = QuantityDtype(units="m")
        dtype3: QuantityDtype = QuantityDtype(units="kg")

        assert dtype1 == dtype2
        assert dtype1 != dtype3

    def test_dtype_hash(self) -> None:
        """Test dtype hashing."""
        dtype: QuantityDtype = QuantityDtype(units="m")
        # Should be hashable
        _ = hash(dtype)

    def test_construct_from_string(self) -> None:
        """Test construct_from_string classmethod."""
        dtype: QuantityDtype = QuantityDtype.construct_from_string(string="quantity[m]")
        assert dtype.units == Unit("m")

    def test_na_value(self) -> None:
        """Test NA value for dtype."""
        dtype: QuantityDtype = QuantityDtype(units="m")
        na: Quantity[float | Vector] = dtype.na_value
        assert isinstance(na, Quantity)
        # Convert to array and check for NaN
        val_array: NDArray[Any] = np.asarray(na.value)
        assert np.isnan(val_array).any() if val_array.size > 0 else np.isnan(val_array)


class TestQuantityArray:
    """Tests for QuantityArray."""

    def test_create_from_list(self) -> None:
        """Test creating QuantityArray from list."""
        arr: QuantityArray = QuantityArray(values=[1.0, 2.0, 3.0], dtype="quantity[m]")
        assert len(arr) == 3
        assert arr.dtype == QuantityDtype(units="m")

    def test_create_from_quantity(self) -> None:
        """Test creating QuantityArray from Quantity."""
        q: Quantity[Vector] = Quantity([1.0, 2.0, 3.0], "m")  # type: ignore[arg-type]
        arr: QuantityArray = QuantityArray(q)
        assert len(arr) == 3

    def test_getitem_scalar(self) -> None:
        """Test getting single item."""
        arr: QuantityArray = QuantityArray(values=[1.0, 2.0, 3.0], dtype="quantity[m]")
        item: Quantity[float | Vector] | QuantityArray | Any = arr[0]
        assert isinstance(item, Quantity)
        assert item.value == 1.0
        assert item.units == Unit(units="m")

    def test_getitem_slice(self) -> None:
        """Test getting slice."""
        arr: QuantityArray = QuantityArray(values=[1.0, 2.0, 3.0], dtype="quantity[m]")
        subset: Quantity[float | Vector] | QuantityArray = arr[0:2]
        assert isinstance(subset, QuantityArray)
        assert len(subset) == 2

    def test_setitem(self) -> None:
        """Test setting item."""
        arr: QuantityArray = QuantityArray(values=[1.0, 2.0, 3.0], dtype="quantity[m]")
        arr[0] = 10.0
        assert arr[0].value == 10.0

    def test_setitem_with_quantity(self) -> None:
        """Test setting item with Quantity."""
        arr: QuantityArray = QuantityArray(values=[1.0, 2.0, 3.0], dtype="quantity[m]")
        arr[0] = Quantity(100.0, units="cm")
        # Should convert to meters
        assert abs(arr[0].value - 1.0) < 0.01

    def test_isna(self) -> None:
        """Test NA detection."""
        arr: QuantityArray = QuantityArray(values=[1.0, np.nan, 3.0], dtype="quantity[m]")  # type: ignore[list-item] # noqa: E501
        na_mask: ndarray[Any, Any] = arr.isna()
        assert not na_mask[0]
        assert na_mask[1]
        assert not na_mask[2]

    def test_take(self) -> None:
        """Test take operation."""
        arr: QuantityArray = QuantityArray(values=[1.0, 2.0, 3.0], dtype="quantity[m]")
        result: QuantityArray = arr.take(indices=[0, 2])
        assert len(result) == 2
        assert result[0].value == 1.0
        assert result[1].value == 3.0

    def test_copy(self) -> None:
        """Test copy operation."""
        arr: QuantityArray = QuantityArray(values=[1.0, 2.0, 3.0], dtype="quantity[m]")
        copied: QuantityArray = arr.copy()
        assert len(copied) == len(arr)
        assert copied is not arr

    def test_concat(self) -> None:
        """Test concatenation."""
        arr1: QuantityArray = QuantityArray(values=[1.0, 2.0], dtype="quantity[m]")
        arr2: QuantityArray = QuantityArray(values=[3.0, 4.0], dtype="quantity[m]")
        result: QuantityArray = QuantityArray._concat_same_type([arr1, arr2])
        assert len(result) == 4

    def test_from_sequence_with_quantities(self) -> None:
        """Test _from_sequence with Quantity objects."""
        quantities: list[Quantity[float]] = [
            Quantity[float](1.0, "m"),
            Quantity[float](2.0, "m"),
            Quantity[float](3.0, "m"),
        ]
        arr: QuantityArray = QuantityArray._from_sequence(quantities)
        assert len(arr) == 3
        assert arr.dtype.units == Unit(units="m")

    def test_to_different_units(self) -> None:
        """Test unit conversion."""
        arr: QuantityArray = QuantityArray(values=[1.0, 2.0, 3.0], dtype="quantity[m]")
        converted: QuantityArray = arr.to(units="cm")
        assert converted[0].value == 100.0
        assert converted.dtype.units == Unit(units="cm")

    def test_quantity_property(self) -> None:
        """Test quantity property."""
        arr: QuantityArray = QuantityArray(values=[1.0, 2.0, 3.0], dtype="quantity[m]")
        q: Quantity[float | Vector] = arr.quantity
        assert isinstance(q, Quantity)
        assert q.units == Unit("m")

    def test_astype_to_object(self) -> None:
        """Test conversion to object dtype."""
        arr: QuantityArray = QuantityArray([1.0, 2.0, 3.0], dtype="quantity[m]")
        obj_arr = arr.astype(object)
        assert isinstance(obj_arr[0], Quantity)

    def test_reduce_operations(self) -> None:
        """Test reduction operations."""
        arr: QuantityArray = QuantityArray(values=[1.0, 2.0, 3.0], dtype="quantity[m]")

        # Sum
        result: Quantity[float | Vector] = arr._reduce(name="sum")
        assert isinstance(result, Quantity)
        assert result.value == 6.0

        # Mean
        result: Quantity[float | Vector] = arr._reduce(name="mean")
        assert result.value == 2.0

        # Min/Max
        result: Quantity[float | Vector] = arr._reduce(name="min")
        assert result.value == 1.0

        result: Quantity[float | Vector] = arr._reduce(name="max")
        assert result.value == 3.0


class TestPandasIntegration:
    """Test integration with pandas Series and DataFrame."""

    def test_create_series_with_dtype_string(self) -> None:
        """Test creating Series with dtype string."""
        series: Series = Series([1.0, 2.0, 3.0], dtype="quantity[m]")
        assert isinstance(series.dtype, QuantityDtype)
        assert len(series) == 3

    def test_create_series_with_dtype_object(self) -> None:
        """Test creating Series with QuantityDtype object."""
        dtype: QuantityDtype = QuantityDtype("kg")
        series: Series = Series([1.0, 2.0, 3.0], dtype=dtype)
        assert series.dtype == dtype

    def test_create_dataframe(self) -> None:
        """Test creating DataFrame with quantity columns."""
        df: DataFrame = DataFrame(
            data={
                "length": Series(data=[1.0, 2.0, 3.0], dtype="quantity[m]"),
                "mass": Series(data=[10.0, 20.0, 30.0], dtype="quantity[kg]"),
            }
        )
        assert isinstance(df["length"].dtype, QuantityDtype)
        assert isinstance(df["mass"].dtype, QuantityDtype)

    def test_series_units_accessor(self) -> None:
        """Test .units accessor on Series."""
        series: Series = Series(data=[1.0, 2.0, 3.0], dtype="quantity[m]")
        # Access the units accessor
        assert hasattr(series, "units")

    def test_series_units_to_conversion(self) -> None:
        """Test unit conversion via accessor."""
        series: Series = Series(data=[1.0, 2.0, 3.0], dtype="quantity[m]")
        converted: Any = series.units.to("cm")
        assert converted[0] == Quantity[float](value=100.0, units="cm")
        assert converted.dtype.units == Unit(units="cm")

    def test_series_units_quantity_property(self) -> None:
        """Test quantity property via accessor."""
        series: Series = Series(data=[1.0, 2.0, 3.0], dtype="quantity[m]")
        q: Any = series.units.quantity
        assert isinstance(q, Quantity)
        assert q.units == Unit(units="m")

    def test_dataframe_units_accessor(self) -> None:
        """Test .units accessor on DataFrame."""
        df: DataFrame = DataFrame(
            data={
                "length": Series(data=[1.0, 2.0], dtype="quantity[m]"),
                "mass": Series(data=[10.0, 20.0], dtype="quantity[kg]"),
            }
        )
        assert hasattr(df, "units")

    def test_dataframe_units_summary(self) -> None:
        """Test units summary."""
        df: DataFrame = DataFrame(
            data={
                "length": Series(data=[1.0, 2.0], dtype="quantity[m]"),
                "mass": Series(data=[10.0, 20.0], dtype="quantity[kg]"),
                "count": Series(data=[1, 2]),  # No units
            }
        )
        summary: Any = df.units.summary()
        assert "length" in summary
        assert "mass" in summary
        assert "count" not in summary
        assert summary["length"] == "m"
        assert summary["mass"] == "kg"

    def test_dataframe_units_to_conversion(self) -> None:
        """Test unit conversion on DataFrame columns."""
        df: DataFrame = DataFrame(
            data={
                "length": Series(data=[1.0, 2.0], dtype="quantity[m]"),
                "mass": Series(data=[1.0, 2.0], dtype="quantity[kg]"),
            }
        )
        converted: Any = df.units.to({"length": "cm", "mass": "g"})
        assert converted["length"].dtype.units == Unit(units="cm")
        assert converted["mass"].dtype.units == Unit(units="g")

    def test_series_operations(self) -> None:
        """Test arithmetic operations on Series."""
        s1: Series = Series(data=[1.0, 2.0, 3.0], dtype="quantity[m]")
        s2: Series = Series(data=[1.0, 2.0, 3.0], dtype="quantity[m]")

        # Addition (not yet implemented but structure exists)
        # result = s1 + s2
        # assert isinstance(result.dtype, QuantityDtype)

    def test_indexing_and_slicing(self) -> None:
        """Test indexing operations."""
        series: Series = Series(data=[1.0, 2.0, 3.0, 4.0, 5.0], dtype="quantity[m]")

        # Single item
        item: Any = series.iloc[0]
        assert isinstance(item, Quantity)

        # Slice
        subset: Any = series.iloc[1:3]
        assert len(subset) == 2
        assert isinstance(subset.dtype, QuantityDtype)

    def test_concat_series(self) -> None:
        """Test concatenating series."""
        s1: Series = Series(data=[1.0, 2.0], dtype="quantity[m]")
        s2: Series = Series(data=[3.0, 4.0], dtype="quantity[m]")

        result: Series = pd.concat([s1, s2], ignore_index=True)
        assert len(result) == 4
        assert isinstance(result.dtype, QuantityDtype)

    def test_groupby_operations(self) -> None:
        """Test groupby with quantity columns."""
        df: DataFrame = DataFrame(
            data={
                "group": ["A", "A", "B", "B"],
                "value": Series(data=[1.0, 2.0, 3.0, 4.0], dtype="quantity[m]"),
            }
        )

        # Groupby should work
        grouped: DataFrameGroupBy = df.groupby("group")
        # Basic operations
        _ = grouped.size()

    def test_nan_handling(self) -> None:
        """Test handling of NaN values."""
        series: Series = Series(data=[1.0, np.nan, 3.0], dtype="quantity[m]")  # type: ignore[list-item] # noqa: E501
        assert series.isna()[1]
        assert not series.isna()[0]

    def test_dtype_preservation(self) -> None:
        """Test that dtype is preserved through operations."""
        df: DataFrame = DataFrame(
            data={"a": Series([1.0, 2.0, 3.0], dtype="quantity[m]")}
        )

        # Select column
        col: Series | Any | DataFrame = df["a"]
        assert isinstance(col.dtype, QuantityDtype)

        # Reset index
        df_reset: DataFrame = df.reset_index(drop=True)
        assert isinstance(df_reset["a"].dtype, QuantityDtype)


class TestEdgeCases:
    """Test edge cases."""

    def test_empty_array(self) -> None:
        """Test creating empty array."""
        arr: QuantityArray = QuantityArray(values=[], dtype="quantity[m]")
        assert len(arr) == 0

    def test_single_element_array(self) -> None:
        """Test single element array."""
        arr: QuantityArray = QuantityArray([5.0], dtype="quantity[m]")
        assert len(arr) == 1
        assert arr[0].value == 5.0

    def test_mixed_unit_conversion(self) -> None:
        """Test converting array with different source units."""
        quantities: list[Quantity[float]] = [
            Quantity[float](value=1.0, units="m"),
            Quantity[float](value=100.0, units="cm"),
            Quantity[float](value=1000.0, units="mm"),
        ]
        arr: QuantityArray = QuantityArray._from_sequence(scalars=quantities)
        # All should be normalized to first unit
        assert arr.dtype.units == Unit(units="m")

    def test_incompatible_units_error(self) -> None:
        """Test that incompatible units raise errors."""
        # This should work - same dimension
        arr: QuantityArray = QuantityArray(values=[1.0, 2.0], dtype="quantity[m]")
        arr.to(units="ft")  # Length to length

        # This should fail - different dimensions
        with pytest.raises(Exception):  # Will raise some error from Quantity.to()
            arr.to(units="kg")  # Length to mass


class TestDocExamples:
    """Test examples from documentation."""

    def test_basic_usage_example(self) -> None:
        """Test basic usage example."""
        # Create a Series with units
        distances: Series = Series(data=[1.0, 2.0, 3.0], dtype="quantity[m]")
        assert len(distances) == 3

        # Convert units
        distances_ft: Any = distances.units.to("ft")
        assert distances_ft.dtype.units == Unit("ft")

    def test_dataframe_example(self) -> None:
        """Test DataFrame example."""
        df: DataFrame = DataFrame(
            data={
                "torque": Series(data=[1.0, 2.0, 3.0], dtype="quantity[N m]"),
                "force": Series(data=[10.0, 20.0, 30.0], dtype="quantity[N]"),
            }
        )

        assert isinstance(df["torque"].dtype, QuantityDtype)
        assert isinstance(df["force"].dtype, QuantityDtype)

        # Check units
        summary: Any = df.units.summary()
        assert "torque" in summary
        assert "force" in summary


if __name__ == "__main__":
    pytest.main(args=[__file__, "-v"])
