.. _quantity_dimensions:

Quantity Dimensions
===================

The `ansys.units.quantity_dimensions` module defines standard physical quantity dimensions, covering SI base quantities (e.g., mass, time) and many commonly used derived quantities (e.g., force, pressure, energy).

Overview
--------

A **quantity dimension** describes the physical nature of a value, such as length, time, or force. These dimensions are used internally in dimensional analysis, unit validation, and conversion.

This module provides a set of immutable, predefined dimension objects via the `QuantityDimensions` class. Each attribute of this class represents a `Dimensions` object composed from SI base dimensions.

These objects support symbolic operations such as multiplication, division, and exponentiation to allow for composition and comparison of dimensions.

Usage
-----

You do not create `QuantityDimensions` instances directly. Instead, you use the class-level attributes:

.. code-block:: python

    from ansys.units.quantity_dimensions import QuantityDimensions

    # Access predefined dimensions
    force = QuantityDimensions.FORCE
    area = QuantityDimensions.AREA
    pressure = QuantityDimensions.PRESSURE

    # Perform dimensional checks
    assert pressure == force / area

    # Velocity has expected dimensional form: LENGTH / TIME
    print(QuantityDimensions.VELOCITY)

    # Dimensions can be compared or used in analysis
    print(QuantityDimensions.ENERGY == QuantityDimensions.FORCE * QuantityDimensions.LENGTH)

Vector Quantities
-----------------

Certain quantities, such as velocity or momentum, are marked as **vector quantities**. For these, additional attributes are automatically generated:

- `<NAME>_X`, `<NAME>_Y`, `<NAME>_Z` - Cartesian components
- `<NAME>_MAGNITUDE` - scalar magnitude

Example:

.. code-block:: python

    QuantityDimensions.VELOCITY_X  # Cartesian component
    QuantityDimensions.VELOCITY_MAGNITUDE  # Scalar form

These variants share the same dimensional structure as the base quantity.

Use Cases
---------

- Validating consistency of physical equations and formulas
- Enabling unit-aware computation and conversions
- Providing structure to variable descriptors and unit systems
