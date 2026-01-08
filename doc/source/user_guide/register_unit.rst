Registering Custom Units
========================

You can register new derived units at runtime and make them available to all
subsequent ``UnitRegistry`` instances using ``register_unit``.

Overview
--------

- ``register_unit(unit, composition, factor)`` adds a new unit symbol and ties it
  to an existing composition of configured units. The registration is process-local
  and applies to any new ``UnitRegistry()`` created after registration.
- Duplicate registrations (including collisions with built-in units) raise
  ``UnitAlreadyRegistered``.

Example
-------

.. code-block:: python

   from ansys.units import UnitRegistry, register_unit
   from ansys.units.unit_registry import UnitAlreadyRegistered

   # Register a new symbol 'Q' equivalent to joule (J)
   register_unit(unit="Q", composition="N m", factor=1)

   ur = UnitRegistry()
   assert ur.Q == ur.J

   # Re-registering the same unit raises an error
   try:
       register_unit(unit="Q", composition="N m", factor=1)
   except UnitAlreadyRegistered:
       pass

   # Register another alias 'Z' now
   register_unit(unit="Z", composition="N m", factor=1)

   # Existing registries don't update retroactively
   try:
       _ = ur.Z
       raise AssertionError("Expected AttributeError for ur.Z")
   except AttributeError:
       pass

   # New registries see all registered units
   ur2 = UnitRegistry()
   assert ur2.Q == ur2.J == ur2.Z

Notes
-----

- ``composition`` must be a valid unit string composed of configured base/derived
  units (for example, ``"N m"``).
- ``factor`` is the scale factor relating the composition to the new unit symbol.