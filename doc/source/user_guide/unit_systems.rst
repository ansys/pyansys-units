Custom Unit Systems
====================

A ``UnitSystem`` defines the unit used for each base dimension (mass, length,
time, and so on). In addition to the predefined systems (``"SI"``, ``"CGS"``,
``"BT"``), you can define your own unit system, for example an ``"MMGS"``
(millimeter, gram, second) system commonly used for material databases.

Custom Unit Systems From Mappings
---------------------------------

Pass a ``base_units`` mapping to override only the dimensions you care about.
Unspecified dimensions default to the base system (``"SI"`` by default):

.. code-block:: python

    from ansys.units import BaseDimensions, UnitSystem

    dims = BaseDimensions
    mmgs = UnitSystem(
        base_units={
            dims.MASS: "g",
            dims.LENGTH: "mm",
        }
    )
    mmgs.MASS  # "g"
    mmgs.LENGTH  # "mm"
    mmgs.TIME  # "s" (inherited from SI)

SI-prefixed units (``"mm"``, ``"km"``, and so on) and single-composition
derived units (``"tonne"``, defined as ``1000 kg``) are accepted as long as
they are dimensionally atomic, that is, equivalent to exactly one base
dimension. Compound units that span more than one base dimension, such as
``"N"`` or ``"MPa"``, cannot be assigned directly since pressure and force
are not base dimensions - they always emerge as derived quantities of a
consistent unit system.

For example, the classic mm-tonne-second system used by structural material
databases produces stress/pressure values that are numerically consistent
with ``MPa``. You can also provide ``preferred_units`` to simplify matching
derived quantities to a domain-preferred unit such as ``MPa``:

.. code-block:: python

    from ansys.units import BaseDimensions, Quantity, UnitSystem

    dims = BaseDimensions
    us = UnitSystem(
        base_units={
            dims.MASS: "tonne",
            dims.LENGTH: "mm",
            dims.TIME: "s",
        },
        preferred_units=["MPa"],
    )
    youngs_modulus = Quantity(210e9, "Pa").convert(us)
    youngs_modulus.value  # 210000.0
    youngs_modulus.units.name  # "MPa"

Registering a Named Unit System
--------------------------------

Use ``UnitSystem.register_system()`` to make a fully defined custom system
reusable by name, the same way built-in systems are used:

.. code-block:: python

    from ansys.units import BaseDimensions, UnitSystem

    dims = BaseDimensions
    UnitSystem.register_system(
        name="MMGS",
        base_units={
            dims.MASS: "g",
            dims.LENGTH: "mm",
            dims.TIME: "s",
            dims.TEMPERATURE: "K",
            dims.TEMPERATURE_DIFFERENCE: "delta_K",
            dims.ANGLE: "radian",
            dims.CHEMICAL_AMOUNT: "mol",
            dims.LIGHT: "cd",
            dims.CURRENT: "A",
            dims.SOLID_ANGLE: "sr",
        },
    )

    mmgs = UnitSystem(system="MMGS")

``register_system()`` requires every base dimension to be provided and
raises:

- ``UnitSystemAlreadyRegistered`` if ``name`` is already used by a built-in
  or previously registered system.
- ``IncompleteUnitSystem`` if any base dimension is missing.
- ``NotBaseUnit`` / ``IncorrectUnitType`` if a unit is invalid for its slot.

Registration is global for the running process, matching the behavior of the
predefined unit systems loaded from ``cfg.yaml``.
