.. _pandas_integration:

==================================
Pandas Integration for ansys-units
==================================

The ``ansys-units`` library provides pandas extension types for unit-aware
``DataFrame`` and ``Series`` objects, similar to ``pint-pandas``.

Installation
------------

Pandas integration is available when pandas is installed:

.. code-block:: bash

   pip install ansys-units pandas

Features
--------

- **ExtensionDtype**: ``QuantityDtype`` for declaring unit-aware column types
- **ExtensionArray**: ``QuantityArray`` for storing arrays of quantities with consistent units
- **Unit-aware operations**: Automatic unit tracking and conversion
- **Series accessor**: ``.units`` accessor for unit operations on ``Series``
- **DataFrame accessor**: ``.units`` accessor for DataFrame-level unit operations

Quick Start
-----------

Creating Unit-Aware Series
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas as pd
   from ansys.units import QuantityDtype

   # Create a Series with units
   distances = pd.Series([1.0, 2.0, 3.0], dtype="quantity[m]")
   print(distances)
   # 0    1.0 m
   # 1    2.0 m
   # 2    3.0 m
   # dtype: quantity[m]

   # Or use QuantityDtype explicitly
   dtype = QuantityDtype("kg")
   masses = pd.Series([10.0, 20.0, 30.0], dtype=dtype)

Creating Unit-Aware DataFrames
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas as pd

   df = pd.DataFrame(
       {
           "length": pd.Series([1.0, 2.0, 3.0], dtype="quantity[m]"),
           "mass": pd.Series([10.0, 20.0, 30.0], dtype="quantity[kg]"),
           "time": pd.Series([5.0, 10.0, 15.0], dtype="quantity[s]"),
       }
   )

   print(df)

Unit Conversion
---------------

Converting Series Units
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   distances = pd.Series([1.0, 2.0, 3.0], dtype="quantity[m]")
   distances_cm = distances.units.to("cm")
   print(distances_cm)

Converting DataFrame Columns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   df = pd.DataFrame(
       {
           "length": pd.Series([1.0, 2.0], dtype="quantity[m]"),
           "mass": pd.Series([1.0, 2.0], dtype="quantity[kg]"),
       }
   )

   df_converted = df.units.to(
       {
           "length": "cm",
           "mass": "g",
       }
   )

   print(df_converted)

DataFrame Unit Summary
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   df = pd.DataFrame(
       {
           "length": pd.Series([1.0, 2.0], dtype="quantity[m]"),
           "mass": pd.Series([10.0, 20.0], dtype="quantity[kg]"),
           "count": pd.Series([1, 2]),
       }
   )

   summary = df.units.summary()
   print(summary)

Working with Quantity Objects
-----------------------------

Creating Arrays from Quantities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas as pd
   from ansys.units import Quantity, QuantityArray

   quantities = [
       Quantity(1.0, "m"),
       Quantity(2.0, "m"),
       Quantity(3.0, "m"),
   ]

   arr = QuantityArray._from_sequence(quantities)
   series = pd.Series(arr)

Accessing as Quantity
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   series = pd.Series([1.0, 2.0, 3.0], dtype="quantity[m]")
   q = series.units.quantity

   print(type(q))
   print(q.units)

Indexing and Selection
----------------------

.. code-block:: python

   series = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0], dtype="quantity[m]")

   element = series.iloc[0]
   subset = series.iloc[1:3]

Concatenation
-------------

Series with compatible units are combined in the units of the first one. Series
with incompatible units, such as ``m`` and ``kg``, are combined into an ``object``
series.

.. code-block:: python

   s1 = pd.Series([1.0, 2.0], dtype="quantity[m]")
   s2 = pd.Series([250.0], dtype="quantity[cm]")

   result = pd.concat([s1, s2], ignore_index=True)
   print(result.dtype)  # quantity[m], values [1.0, 2.0, 2.5]

Missing Values (NaN)
--------------------

.. code-block:: python

   import numpy as np
   import pandas as pd

   series = pd.Series([1.0, np.nan, 3.0], dtype="quantity[m]")
   print(series.isna())

Reduction Operations
--------------------

.. code-block:: python

   series = pd.Series([1.0, 2.0, 3.0, 4.0], dtype="quantity[m]")

   total = series.sum()
   average = series.mean()
   middle = series.median()
   minimum = series.min()
   maximum = series.max()
   spread = series.std()  # in "m"
   variance = series.var()  # in "m^2"
   error = series.sem()  # in "m"
   product = series.prod()  # 24.0 in "m^4"
   series.skew()  # plain float, shape statistics have no units
   series.kurt()

The units of ``prod()`` depend on the number of values that are multiplied, so
missing values that are skipped don't count.

DataFrame reductions return one quantity per column, so columns with different units
can be reduced together:

.. code-block:: python

   df = pd.DataFrame(
       {
           "length": pd.Series([1.0, 2.0], dtype="quantity[m]"),
           "mass": pd.Series([3.0, 4.0], dtype="quantity[kg]"),
       }
   )

   df.sum()  # [Quantity(3.0, "m"), Quantity(7.0, "kg")]
   df.mean()

``Series.describe()`` converts its results to plain floats, which drops the units.
Use the ``.units`` accessor to get the same statistics with units:

.. code-block:: python

   series.units.describe()  # count, mean, std, min, 25%, 50%, 75%, max
   df.units.describe()  # one column per unit-aware column

Cumulative Operations and Unique Values
---------------------------------------

.. code-block:: python

   series = pd.Series([1.0, 2.0, 2.0, 4.0], dtype="quantity[m]")

   series.cumsum()  # [1.0, 3.0, 5.0, 9.0] in "m"
   series.cummax()
   series.unique()  # [1.0, 2.0, 4.0] in "m"
   series.nunique()  # 3
   series.drop_duplicates()
   series.round(1)
   abs(series)

A cumulative product of quantities would have different units for each value, so
``cumprod()`` is only available for dimensionless series:

.. code-block:: python

   ratios = pd.Series([2.0, 3.0, 4.0], dtype="quantity[]")
   ratios.cumprod()  # [2.0, 6.0, 24.0], dimensionless

Rolling, Expanding, and Exponentially Weighted Windows
------------------------------------------------------

pandas converts window data to plain floats, so ``series.rolling(2).mean()`` has no
units. Use the ``.units`` accessor to keep them:

.. code-block:: python

   series = pd.Series([1.0, 2.0, 3.0, 4.0], dtype="quantity[m]")

   series.units.rolling(2).mean()  # [NaN, 1.5, 2.5, 3.5] in "m"
   series.units.rolling(2).var()  # in "m^2"
   series.units.expanding().max()  # in "m"
   series.units.ewm(span=2).mean()  # in "m"

``sum``, ``mean``, ``median``, ``min``, ``max``, ``quantile``, ``first``, and ``last``
keep the units of the series. ``std`` and ``sem`` are in the units of a difference,
and ``var`` is in squared units. Results whose units can't be determined, such as
``count``, ``apply``, and ``corr``, are plain floats.

Grouping
--------

Grouped aggregations keep the units of the column:

.. code-block:: python

   df = pd.DataFrame(
       {
           "beam": ["A", "A", "B"],
           "load": pd.Series([10.0, 20.0, 30.0], dtype="quantity[kN]"),
       }
   )

   df.groupby("beam")["load"].sum()  # [30.0, 30.0] in "kN"
   df.groupby("beam")["load"].mean()
   df.groupby("beam")["load"].std()  # in "kN"
   df.groupby("beam")["load"].var()  # in "kN^2"

Grouped ``prod()`` and ``cumprod()`` are only available for dimensionless columns,
because each group would otherwise have different units.

Temperatures
------------

Unit-aware series follow the same temperature rules as quantities. See
:ref:`temperature`:

- Absolute temperatures, such as ``quantity[C]``, can't be summed, so ``sum()`` and
  ``cumsum()`` raise a ``ProhibitedTemperatureOperation`` error, including in grouped
  aggregations. ``mean()``, ``min()``, and ``max()`` are allowed.
- The standard deviation and variance of absolute temperatures are temperature
  differences, for example ``delta_C`` and ``delta_C^2``.

Arithmetic and Comparisons
--------------------------

Arithmetic between unit-aware ``Series`` objects converts units and returns a
unit-aware ``Series``. Comparisons are element-wise:

.. code-block:: python

   length = pd.Series([1.0, 2.0], dtype="quantity[m]")
   width = pd.Series([50.0, 100.0], dtype="quantity[cm]")

   length + width  # [1.5, 3.0] in "m"
   length * width  # [50.0, 200.0] in "m cm"
   length * 2  # [2.0, 4.0] in "m"
   length > width  # [True, True]
   -length  # [-1.0, -2.0] in "m"

Advanced: Subdtype Specification
--------------------------------

.. code-block:: python

   from ansys.units import QuantityDtype

   series = pd.Series(
       [1.0, 2.0, 3.0],
       dtype=QuantityDtype("m", subdtype="float32"),
   )

   print(series.dtype.name)

Integration with Existing Code
------------------------------

.. code-block:: python

   df = pd.read_csv("data.csv")

   df["length"] = pd.Series(df["length"].values, dtype="quantity[m]")
   df["mass"] = pd.Series(df["mass"].values, dtype="quantity[kg]")

   units_info = df.units.summary()

Limitations
-----------

- **Products**: ``cumprod()`` and grouped ``prod()`` raise a ``TypeError`` unless the
  series is dimensionless, because each result would have different units.
- **Built-in windows and describe()**: ``series.rolling()``, ``series.expanding()``,
  ``series.ewm()``, and ``series.describe()`` return plain floats. Use the ``.units``
  versions of these methods to keep units.

Examples
--------

Engineering Data Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas as pd

   df = pd.DataFrame(
       {
           "beam_id": [1, 2, 3, 4],
           "length": pd.Series([5.0, 10.0, 15.0, 20.0], dtype="quantity[m]"),
           "load": pd.Series([1000.0, 2000.0, 3000.0, 4000.0], dtype="quantity[N]"),
           "deflection": pd.Series([0.5, 1.0, 1.5, 2.0], dtype="quantity[mm]"),
       }
   )

   df_imperial = df.units.to(
       {
           "length": "ft",
           "load": "lbf",
           "deflection": "in",
       }
   )

Temperature Data
~~~~~~~~~~~~~~~~

.. code-block:: python

   temps = pd.Series([20.0, 25.0, 30.0], dtype="quantity[C]")
   temps_f = temps.units.to("F")
   print(temps_f)

Multiple Unit Systems
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   df = pd.DataFrame(
       {
           "metric_length": pd.Series([1.0, 2.0], dtype="quantity[m]"),
           "imperial_length": pd.Series([3.0, 4.0], dtype="quantity[ft]"),
       }
   )

   df_si = df.units.to(
       {
           "metric_length": "m",
           "imperial_length": "m",
       }
   )
