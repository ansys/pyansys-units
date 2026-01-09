Registering Custom Units
========================

You can register new derived units at runtime using
instance-scoped registration directly on a ``UnitRegistry`` instance.

Instance-Scoped
---------------

- ``UnitRegistry.register_unit(unit, composition, factor)`` adds a new unit
  symbol to that single registry instance. It does not change global state,
  avoids temporal coupling, and keeps the registry scope clean.
- Duplicate registrations on the same instance (including collisions with
  built-in units) raise ``UnitAlreadyRegistered``.

See also: :download:`tests/test_register_unit.py <../../../tests/test_register_unit.py>` (function ``test_instance_register_unit``)

Example
-------

.. code-block:: python

   from ansys.units import UnitRegistry

   ur = UnitRegistry()
   # Register a symbol 'Q' equivalent to Joule (N m)
   ur.register_unit(unit="Q", composition="N m", factor=1)
   assert ur.Q == ur.J

   # A new registry does not see instance registrations
   ur2 = UnitRegistry()
   try:
       _ = ur2.Q
       raise AssertionError("Expected AttributeError for ur2.Q")
   except AttributeError:
       pass

.. note::
   Dynamic registration is instance-scoped. Register units on the specific
  ``UnitRegistry`` you want to use; new registries do not automatically
   inherit instance-registered units.

Notes
-----

- ``composition`` must be a valid unit string composed of configured base/derived
  units (for example, ``"N m"``).
- ``factor`` is the scale factor relating the composition to the new unit symbol.