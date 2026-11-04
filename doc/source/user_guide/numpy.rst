.. _numpy_integration:

=================
NumPy integration
=================

With NumPy installed, ``Quantity`` objects work directly with NumPy functions and
universal functions. The result is a ``Quantity`` with the correct units,
and operations that don't make sense for the units raise an error.

Units in NumPy functions
------------------------

Functions that keep the units of their input, such as ``np.mean``, ``np.max``, or
``np.sort``, return a ``Quantity`` in the same units. Functions that combine
operands, such as ``np.maximum`` or ``np.concatenate``, first convert all operands
to the units of the first one:

.. code:: python

    import numpy as np
    from ansys.units import Quantity

    lengths = Quantity(np.array([1.0, 2.0, 3.0, 6.0]), "m")

    np.mean(lengths)  # Quantity (3.0, "m")
    np.sum(lengths)  # Quantity (12.0, "m")
    np.std(lengths)  # Quantity (1.87..., "m")
    np.var(lengths)  # Quantity (3.5, "m^2")
    np.diff(lengths)  # Quantity ([1. 1. 3.], "m")

    np.concatenate([lengths, Quantity([300.0], "cm")])  # Quantity ([1. 2. 3. 6. 3.], "m")
    np.maximum(lengths, Quantity(250.0, "cm"))  # Quantity ([2.5 2.5 3. 6.], "m")

    # Quantity ([1.5 2. 3. 4.], "m")
    np.clip(lengths, Quantity(150.0, "cm"), Quantity(4.0, "m"))

Arithmetic functions combine units in the same way as the arithmetic operators:

.. code:: python

    import numpy as np
    from ansys.units import Quantity

    np.sqrt(Quantity(9.0, "m^2"))  # Quantity (3.0, "m")
    np.multiply(Quantity(2.0, "m"), Quantity(3.0, "s"))  # Quantity (6.0, "m s")
    np.power(Quantity(2.0, "m"), 3)  # Quantity (8.0, "m^3")

Plain NumPy arrays combined with quantities are treated as dimensionless:

.. code:: python

    import numpy as np
    from ansys.units import Quantity

    np.array([1.0, 2.0]) * Quantity(2.0, "m")  # Quantity ([2. 4.], "m")
    np.array([2.0, 4.0]) / Quantity(2.0, "s")  # Quantity ([1. 2.], "s^-1")

Trigonometric, exponential, and logarithmic functions
-----------------------------------------------------

``np.sin``, ``np.cos``, and ``np.tan`` accept angles in any angle unit, or
dimensionless values. ``np.exp``, ``np.log``, and the hyperbolic functions accept
only dimensionless values. Inverse trigonometric functions return radians. Other
units raise a ``DimensionlessArgumentRequired`` error:

.. code:: python

    import numpy as np
    from ansys.units import Quantity

    np.sin(Quantity(90.0, "degree"))  # Quantity (1.0, "")
    np.arccos(Quantity(0.0, ""))  # Quantity (1.5707..., "radian")
    np.arctan2(Quantity(1.0, "m"), Quantity(100.0, "cm"))  # Quantity (0.785..., "radian")
    np.exp(Quantity(1.0, ""))  # Quantity (2.718..., "")

    np.sin(Quantity(1.0, "m"))  # raises DimensionlessArgumentRequired

Matrix multiplication
---------------------

The ``@`` operator and ``np.matmul`` multiply the units of their operands:

.. code:: python

    import numpy as np
    from ansys.units import Quantity

    matrix = Quantity(np.array([[1.0, 2.0], [3.0, 4.0]]), "m")
    vector = Quantity(np.array([1.0, 1.0]), "N")

    matrix @ vector  # Quantity ([3. 7.], "m N")
    matrix @ [1.0, 2.0]  # Quantity ([5. 11.], "m")
    np.dot(matrix[0], vector)  # Quantity (3.0, "m N")

Temperatures
------------

NumPy functions follow the same temperature rules as the arithmetic operators. See
:ref:`temperature`:

- Absolute temperatures can't be summed, so ``np.sum`` and ``np.cumsum`` raise a
  ``ProhibitedTemperatureOperation`` error. ``np.mean``, ``np.min``, and ``np.max``
  are allowed.
- Spreads of absolute temperatures, such as ``np.ptp``, ``np.diff``, and
  ``np.std``, return temperature differences.
- Multiplicative functions, such as ``np.multiply``, ``np.sqrt``, or ``@``, raise a
  ``ProhibitedOffsetUnitOperation`` error for C and F.

.. code:: python

    import numpy as np
    from ansys.units import Quantity

    temperatures = Quantity(np.array([10.0, 20.0, 40.0]), "C")

    np.mean(temperatures)  # Quantity (23.33..., "C")
    np.ptp(temperatures)  # Quantity (30.0, "delta_C")
    np.sum(temperatures)  # raises ProhibitedTemperatureOperation

Limitations
-----------

- Functions that aren't supported, such as ``np.prod``, raise a ``TypeError``
  instead of guessing the units of the result.
- The ``out`` argument isn't supported.
- ``np.asarray(quantity)`` doesn't remove the units. Use ``quantity.value`` to get
  the plain array.
