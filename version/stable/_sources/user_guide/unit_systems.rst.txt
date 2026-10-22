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

A ``UnitSystem`` is only the set of base units: it has no opinion on how
derived quantities should be displayed. Choosing a display unit such as
``"MPa"`` instead of an expanded expression is a separate concern, handled by
``PreferredUnits`` (see below).

Preferred Units
---------------

For example, the classic mm-tonne-second system used by structural material
databases produces stress and pressure values that are numerically consistent
with ``MPa``, but without any extra configuration, converting through that
system produces an expanded base-unit expression:

.. code-block:: python

    from ansys.units import BaseDimensions, Quantity, UnitSystem

    dims = BaseDimensions
    base = {
        dims.MASS: "tonne",
        dims.LENGTH: "mm",
        dims.TIME: "s",
    }
    mm_tonne_second = UnitSystem(base_units=base)

    expanded = Quantity(210e9, "Pa").convert(mm_tonne_second)
    print(expanded.value, expanded.units.name)
    # 210000.0 tonne mm^-1 s^-2

Pass a ``PreferredUnits`` object (or a plain string or list, which is wrapped
automatically) to ``Quantity.convert()`` to pick a named unit for matching
dimensions instead:

.. code-block:: python

    from ansys.units import PreferredUnits

    simplified = Quantity(210e9, "Pa").convert(mm_tonne_second, preferred_units=["MPa"])
    print(simplified.value, simplified.units.name)
    # 210000.0 MPa

Because ``PreferredUnits`` is independent of the ``UnitSystem``, the same
system produces different output depending on what is passed to
``convert()``:

.. code-block:: python

    force_expanded = Quantity(5000, "N").convert(mm_tonne_second)
    print(force_expanded.value, force_expanded.units.name)
    # 5000.0 tonne mm s^-2

    material_prefs = PreferredUnits(["MPa", "N"])

    stress = Quantity(210e9, "Pa").convert(mm_tonne_second, preferred_units=material_prefs)
    print(stress.value, stress.units.name)
    # 210000.0 MPa

    load = Quantity(5000, "N").convert(mm_tonne_second, preferred_units=material_prefs)
    print(load.value, load.units.name)
    # 5000.0 N

A preferred unit only applies to quantities whose dimensions match; it has no
effect on anything else, and quantities with no matching entry keep their
expanded base-unit expression.

Dimension-Only Preferred Unit Matching
---------------------------------------

Preferred unit matching is intentionally based on dimensions only. This means
that quantities with the same dimensions use the same preferred-unit entry,
even when they represent different physical concepts. For example, torque and
energy both have dimensions ``M L^2 T^-2``, while stress and energy density
both have dimensions ``M L^-1 T^-2``:

.. code-block:: python

    mechanical_prefs = PreferredUnits(["J", "MPa"])

    torque = Quantity(50, "N m").convert(mm_tonne_second, preferred_units=mechanical_prefs)
    print(torque.units.name)
    # J

    energy = Quantity(50, "J").convert(mm_tonne_second, preferred_units=mechanical_prefs)
    print(energy.units.name)
    # J

    stress = Quantity(210e9, "Pa").convert(
        mm_tonne_second, preferred_units=mechanical_prefs
    )
    print(stress.units.name)
    # MPa

    energy_density = Quantity(210e9, "J m^-3").convert(
        mm_tonne_second, preferred_units=mechanical_prefs
    )
    print(energy_density.units.name)
    # MPa

Quantity-type-aware preferences are not part of ``PreferredUnits``. If two
concepts have identical dimensions but require different display units, keep
that choice explicit in the calling code.

Registering a Named Unit System
--------------------------------

Use ``UnitSystem.register_system()`` to make a fully defined custom system
reusable by name, the same way built-in systems are used. Registration only
covers the base units - keep any ``PreferredUnits`` you want to pair with it
in a separate variable:

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

Migrating from ``UnitSystem(preferred_units=...)``
-----------------------------------------------------

Earlier releases stored preferred units directly on ``UnitSystem``. That API
has been removed because a ``UnitSystem`` (a coherent set of base units) and
a display/conversion policy (which named unit to show for a derived
quantity) are different concepts with different identities - conflating them
made equality ambiguous (two systems with identical base units but different
display choices should be substitutable, but were not). Use the table below
to migrate:

.. list-table::
   :header-rows: 1

   * - Before
     - After
   * - ``UnitSystem(base_units=b, preferred_units=["MPa"])``
     - ``UnitSystem(base_units=b)`` plus ``convert(system, preferred_units=["MPa"])``
   * - ``UnitSystem.register_system(name, b, preferred_units=[...])``
     - ``register_system(name, b)``; keep a ``PreferredUnits`` alongside
   * - ``us.add_preferred_units(...)`` / ``us.preferred_unit_for(d)``
     - ``PreferredUnits(...)`` / ``PreferredUnits.unit_for(d)``

