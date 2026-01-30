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
Pandas Integration Example for ansys-units
==========================================

This example demonstrates how to use ansys-units with pandas DataFrames
for unit-aware data analysis.
"""

import numpy as np

try:
    import pandas as pd

    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    print("Pandas not installed. Install with: pip install pandas")
    exit(1)

from ansys.units import Quantity
from ansys.units.pandas_extension import QuantityArray, QuantityDtype

###############################################################################
# Basic Usage
# -----------
# Create Series with units

print("=" * 70)
print("1. Creating Unit-Aware Series")
print("=" * 70)

# Method 1: Using dtype string
distances = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0], dtype="quantity[m]")
print("\nDistances in meters:")
print(distances)
print(f"Dtype: {distances.dtype}")

# Method 2: Using QuantityDtype object
mass_dtype = QuantityDtype("kg")
masses = pd.Series([10.0, 20.0, 30.0, 40.0, 50.0], dtype=mass_dtype)
print("\nMasses in kilograms:")
print(masses)

###############################################################################
# Unit Conversion
# ---------------
# Convert between different units

print("\n" + "=" * 70)
print("2. Unit Conversion")
print("=" * 70)

# Convert meters to feet
distances_ft = distances.units.to("ft")
print("\nDistances converted to feet:")
print(distances_ft)
print(f"Dtype: {distances_ft.dtype}")

# Convert meters to centimeters
distances_cm = distances.units.to("cm")
print("\nDistances converted to centimeters:")
print(distances_cm)

# Convert kilograms to grams
masses_g = masses.units.to("g")
print("\nMasses converted to grams:")
print(masses_g)

###############################################################################
# DataFrame Operations
# --------------------
# Working with multiple unit columns

print("\n" + "=" * 70)
print("3. Unit-Aware DataFrame")
print("=" * 70)

# Create DataFrame with multiple unit columns
df = pd.DataFrame(
    {
        "specimen_id": [1, 2, 3, 4, 5],
        "length": pd.Series([10.0, 20.0, 30.0, 40.0, 50.0], dtype="quantity[mm]"),
        "width": pd.Series([5.0, 5.0, 5.0, 5.0, 5.0], dtype="quantity[mm]"),
        "thickness": pd.Series([2.0, 2.0, 2.0, 2.0, 2.0], dtype="quantity[mm]"),
        "mass": pd.Series([10.0, 20.0, 30.0, 40.0, 50.0], dtype="quantity[g]"),
        "force": pd.Series([100.0, 200.0, 300.0, 400.0, 500.0], dtype="quantity[N]"),
    }
)

print("\nOriginal DataFrame:")
print(df)

# Get units summary
print("\nUnits Summary:")
units_summary = df.units.summary()
for col, unit in units_summary.items():
    print(f"  {col}: {unit}")

###############################################################################
# Batch Unit Conversion
# ----------------------
# Convert multiple columns at once

print("\n" + "=" * 70)
print("4. Batch Unit Conversion")
print("=" * 70)

# Convert to different unit system
df_converted = df.units.to(
    {"length": "cm", "width": "cm", "thickness": "cm", "mass": "kg"}
)

print("\nDataFrame with converted units:")
print(df_converted)

print("\nNew Units Summary:")
units_summary = df_converted.units.summary()
for col, unit in units_summary.items():
    print(f"  {col}: {unit}")

###############################################################################
# Creating from Quantity Objects
# -------------------------------
# Build arrays from existing Quantity objects

print("\n" + "=" * 70)
print("5. Creating from Quantity Objects")
print("=" * 70)

# Create list of Quantity objects
quantities = [
    Quantity(1.0, "m"),
    Quantity(100.0, "cm"),  # Will be converted to meters
    Quantity(1000.0, "mm"),  # Will be converted to meters
]

# Create array from quantities (they get normalized)
arr = QuantityArray._from_sequence(quantities)
series = pd.Series(arr)

print("\nSeries created from mixed-unit Quantities (normalized to first unit):")
print(series)
print(f"All values in: {series.dtype.units}")

###############################################################################
# Indexing and Selection
# -----------------------
# Access individual elements and slices

print("\n" + "=" * 70)
print("6. Indexing and Selection")
print("=" * 70)

# Get single element (returns Quantity)
first_distance = distances.iloc[0]
print(f"\nFirst distance: {first_distance}")
print(f"Type: {type(first_distance)}")
print(f"Value: {first_distance.value} {first_distance.units}")

# Get slice (returns Series)
middle_distances = distances.iloc[1:4]
print("\nMiddle distances (indices 1-3):")
print(middle_distances)
print(f"Type: {type(middle_distances)}")

# Boolean indexing
large_masses = masses[masses.units.quantity.value > 25.0]  # type: ignore[assignment]
print("\nMasses greater than 25 kg:")
print(large_masses)  # type: ignore[reportUnknownArgumentType]

###############################################################################
# Handling Missing Values
# ------------------------
# Working with NaN values

print("\n" + "=" * 70)
print("7. Missing Values")
print("=" * 70)

# Create series with NaN
data_with_nan = pd.Series([1.0, 2.0, np.nan, 4.0, 5.0], dtype="quantity[m]")  # type: ignore[list-item] # noqa: E501
print("\nData with missing values:")
print(data_with_nan)

# Check for NaN
print("\nMissing value mask:")
print(data_with_nan.isna())

# Drop NaN values
clean_data = data_with_nan.dropna()
print("\nData after dropping NaN:")
print(clean_data)

###############################################################################
# Concatenation
# --------------
# Combining Series with units

print("\n" + "=" * 70)
print("8. Concatenation")
print("=" * 70)

s1 = pd.Series([1.0, 2.0, 3.0], dtype="quantity[m]")
s2 = pd.Series([4.0, 5.0, 6.0], dtype="quantity[m]")

combined = pd.concat([s1, s2], ignore_index=True)
print("\nConcatenated Series:")
print(combined)
print(f"Dtype preserved: {combined.dtype}")

###############################################################################
# Reduction Operations
# --------------------
# Statistical operations that preserve units

print("\n" + "=" * 70)
print("9. Reduction Operations")
print("=" * 70)

measurements = pd.Series([10.5, 12.3, 11.8, 13.2, 10.9], dtype="quantity[mm]")

print("\nMeasurements:")
print(measurements)

# Sum
total = measurements.sum()
print(f"\nSum: {total}")

# Mean
average = measurements.mean()
print(f"Mean: {average}")

# Min and Max
minimum = measurements.min()
maximum = measurements.max()
print(f"Min: {minimum}")
print(f"Max: {maximum}")

# Standard deviation
std = measurements.std()
print(f"Std Dev: {std}")

###############################################################################
# Real-World Example: Structural Analysis
# ----------------------------------------
# Analyzing beam deflection data

print("\n" + "=" * 70)
print("10. Real-World Example: Structural Analysis")
print("=" * 70)

# Simulated beam deflection data
analysis_df = pd.DataFrame(
    {
        "beam_id": ["B001", "B002", "B003", "B004", "B005"],
        "length": pd.Series([5.0, 10.0, 15.0, 20.0, 25.0], dtype="quantity[m]"),
        "load": pd.Series(
            [5000.0, 10000.0, 15000.0, 20000.0, 25000.0], dtype="quantity[N]"
        ),
        "deflection": pd.Series([2.5, 5.0, 7.5, 10.0, 12.5], dtype="quantity[mm]"),
        "stress": pd.Series([50.0, 100.0, 150.0, 200.0, 250.0], dtype="quantity[MPa]"),
    }
)

print("\nBeam Analysis Data (SI units):")
print(analysis_df)
print("\nUnits:")
for col, unit in analysis_df.units.summary().items():
    print(f"  {col}: {unit}")

# Convert to imperial units for reporting
imperial_df = analysis_df.units.to({"length": "ft", "load": "lbf", "deflection": "in"})

print("\nBeam Analysis Data (Imperial units):")
print(imperial_df)
print("\nUnits:")
for col, unit in imperial_df.units.summary().items():
    print(f"  {col}: {unit}")

# Calculate load per unit length (would need arithmetic support)
print("\nAnalysis Summary:")
print(f"  Total beams analyzed: {len(analysis_df)}")
print(f"  Average beam length: {analysis_df['length'].mean()}")
print(f"  Average load: {analysis_df['load'].mean()}")
print(f"  Average deflection: {analysis_df['deflection'].mean()}")
print(f"  Max stress: {analysis_df['stress'].max()}")

###############################################################################
# Accessing Underlying Quantity
# ------------------------------
# Get the full Quantity object from a Series

print("\n" + "=" * 70)
print("11. Accessing Underlying Quantity")
print("=" * 70)

temps = pd.Series([20.0, 25.0, 30.0, 35.0], dtype="quantity[C]")
print("\nTemperature Series:")
print(temps)

# Get as Quantity object
temp_quantity = temps.units.quantity
print(f"\nAs Quantity object: {temp_quantity}")
print(f"Type: {type(temp_quantity)}")
print(f"Units: {temp_quantity.units}")

# Can use Quantity methods
temp_kelvin = temp_quantity.to("K")
print(f"Converted to Kelvin: {temp_kelvin}")

###############################################################################
# Summary
# -------

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print(
    """
The ansys-units pandas extension provides:

✓ Unit-aware Series and DataFrames
✓ Seamless unit conversion
✓ Type preservation through operations
✓ Integration with pandas ecosystem
✓ Missing value handling
✓ Statistical operations with units

This enables safer, more maintainable engineering data analysis
with automatic unit tracking and conversion.
"""
)

print("\nExample completed successfully!")
