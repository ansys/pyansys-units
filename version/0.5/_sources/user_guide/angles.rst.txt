.. _angles:

======
Angles
======

PyAnsys Units treats angles as non-dimensional unit quantity by default but it
supports configuration of angle quantities as dimension.
Angle quantity units such as degree, radian and solid angle can be treated as dimension.

You can set the environment variable ``PYANSYS_UNITS_ANGLE_AS_DIMENSION`` to treat angle quantity
units as dimension.

Angle as non-dimension
**********************

.. code:: python

    import ansys.units as pyunits

    degree = pyunits.Quantity(1.0, "degree")

    degree.is_dimensionless  # True
    degree + 1  # Quantity (58.29577951308232, "degree")


Angle as dimension
******************

.. code:: python

    import os

    os.environ["PYANSYS_UNITS_ANGLE_AS_DIMENSION"] = "1"
    import ansys.units as pyunits

    degree = pyunits.Quantity(1.0, "degree")

    degree.is_dimensionless  # False
    degree + 1  # Not allowed
