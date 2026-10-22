Registering Custom Units
========================

You can register new derived units at runtime using instance-scoped
registration on a ``UnitRegistry`` instance.

At Construction
---------------

Use the ``custom_units`` parameter to register units when creating a registry.
Each entry supports an optional ``"aliases"`` list:

.. code-block:: python

    from ansys.units import UnitRegistry, get_si_value

    ur = UnitRegistry(
        custom_units=[
            {"unit": "micron", "composition": "m", "factor": 1e-6},
            {"unit": "thou", "composition": "m", "factor": 2.54e-5},
            {
                "unit": "furlong",
                "composition": "m",
                "factor": 201.168,
                "aliases": ["furlongs"],
            },
        ]
    )

    # Use string-based lookup with ur.Quantity()
    q = ur.Quantity(10, "micron")
    print(get_si_value(q))  # 1e-05

After Construction
------------------

Use ``register_unit()`` to add units to an existing registry. Two equivalent
calling conventions are supported: a ``composition``/``factor`` form, and an
object-based form that accepts a ``Unit`` or ``Quantity`` definition. Both
forms accept an optional ``aliases`` argument:

.. code-block:: python

    from ansys.units import UnitRegistry
    from ansys.units.common import m

    ur = UnitRegistry()

    # composition/factor form
    ur.register_unit(unit="Q", composition="N m", factor=1)
    assert ur.Q == ur.J

    # Object-based form, with an alias
    ur.register_unit("furlong", 201.168 * m, aliases=["furlongs"])
    assert ur.furlong is ur.furlongs

The object-based form accepts a ``Quantity`` (as produced by ``factor * unit``)
or a bare ``Unit`` (treated as a factor of ``1``).

String-Based Lookup
-------------------

Registered units, and their aliases, can be accessed by name using:

- ``ur.get_unit(name)`` - Returns the ``Unit`` object
- ``ur.Quantity(value, name)`` - Creates a ``Quantity`` with the registered unit

.. code-block:: python

    ur = UnitRegistry(
        custom_units=[
            {"unit": "micron", "composition": "m", "factor": 1e-6},
        ]
    )

    # String-based lookup
    unit = ur.get_unit("micron")
    q = ur.Quantity(1, "micron")

.. note::
   The global ``Quantity()`` constructor does not see instance-registered units.
   Use ``ur.Quantity()`` for string-based creation with custom units.

Instance Isolation
------------------

Each registry maintains its own set of registered units:

.. code-block:: python

    ur1 = UnitRegistry(custom_units=[{"unit": "X", "composition": "m", "factor": 10}])
    ur2 = UnitRegistry(custom_units=[{"unit": "X", "composition": "m", "factor": 100}])
    ur3 = UnitRegistry()  # No custom units

    ur1.X.si_scaling_factor  # 10
    ur2.X.si_scaling_factor  # 100
    ur3.X  # AttributeError - not registered

Collision Detection
--------------------

- Built-in unit names (``m``, ``kg``, ``J``, etc.) can never be overridden,
  even with an equivalent definition.
- Re-registering an existing custom name with the **same effective
  definition** (dimensions, SI scaling factor, and SI offset) is a no-op:
  it returns the existing unit instead of raising. This makes repeated setup
  calls idempotent.
- Re-registering an existing custom name with a **different** effective
  definition raises ``UnitNameAlreadyRegistered``.
- Equivalent definitions registered under **different** names are still
  allowed (the check only applies to the exact name being registered).

.. code-block:: python

    ur = UnitRegistry()

    # These are allowed (different names, same definition)
    ur.register_unit(unit="energy1", composition="N m", factor=1)
    ur.register_unit(unit="energy2", composition="N m", factor=1)

    # Re-registering "energy1" with an equivalent composition is a no-op
    ur.register_unit(unit="energy1", composition="W s", factor=1)

    # Re-registering "energy1" with a different definition raises
    ur.register_unit(unit="energy1", composition="m", factor=1)  # Error!

    # This raises UnitNameAlreadyRegistered (built-in collision)
    ur.register_unit(unit="m", composition="ft", factor=1)  # Error!

Notes
-----

- ``composition`` must be a valid unit string composed of configured base/derived
  units (for example, ``"N m"``).
- ``factor`` is the scale factor relating the composition to the new unit symbol.
- ``aliases`` additional names resolve to the same registered ``Unit`` object
  and are subject to the same collision rules as the primary name.

Persistence
-----------

Custom units registered at runtime are **not** written back to ``cfg.yaml``
or any installed configuration file. They only live on the ``UnitRegistry``
instance and are lost once that instance (or the process) goes away.

To persist custom units across sessions, export them to your own YAML file
and reload them explicitly. This only exports units added via
``register_unit()`` (including through ``custom_units``/``custom_units_file``);
built-in units are never included:

.. code-block:: python

    from ansys.units import UnitRegistry, load_custom_units
    from ansys.units.common import m

    ur = UnitRegistry()
    ur.register_unit("furlong", 201.168 * m, aliases=["furlongs"])

    # Save for later use
    ur.export_custom_units("my_units.yaml")

    # Reload in a new session, or a new registry
    ur2 = UnitRegistry(custom_units_file="my_units.yaml")
    assert ur2.furlong is ur2.furlongs

    # Equivalently, load the definitions yourself and pass them along
    custom_units = load_custom_units("my_units.yaml")
    ur3 = UnitRegistry(custom_units=custom_units)

``export_custom_units()`` raises ``ValueError`` if the registry has no
custom units to export, and raises ``FileExistsError`` if the destination
file already exists (pass ``overwrite=True`` to replace it).

.. note::
   This export/import mechanism is independent of ``register_alias()``,
   whose global aliases are never persisted (see :ref:`unit_aliases`).