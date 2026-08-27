Registering Custom Units
========================

You can register new derived units at runtime using instance-scoped
registration on a ``UnitRegistry`` instance.

At Construction
---------------

Use the ``custom_units`` parameter to register units when creating a registry:

.. code-block:: python

    from ansys.units import UnitRegistry, get_si_value

    ur = UnitRegistry(
        custom_units=[
            {"unit": "micron", "composition": "m", "factor": 1e-6},
            {"unit": "thou", "composition": "m", "factor": 2.54e-5},
        ]
    )

    # Use string-based lookup with ur.Quantity()
    q = ur.Quantity(10, "micron")
    print(get_si_value(q))  # 1e-05

After Construction
------------------

Use ``register_unit()`` to add units to an existing registry:

.. code-block:: python

    from ansys.units import UnitRegistry

    ur = UnitRegistry()
    ur.register_unit(unit="Q", composition="N m", factor=1)
    assert ur.Q == ur.J

String-Based Lookup
-------------------

Registered units can be accessed by name using:

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
-------------------

The collision check is **name-only**:

- Duplicate names raise ``UnitNameAlreadyRegistered``
- Built-in unit names (``m``, ``kg``, ``J``, etc.) cannot be overridden
- Equivalent definitions with different names are allowed

.. code-block:: python

    ur = UnitRegistry()

    # These are allowed (different names, same definition)
    ur.register_unit(unit="energy1", composition="N m", factor=1)
    ur.register_unit(unit="energy2", composition="N m", factor=1)

    # This raises UnitNameAlreadyRegistered
    ur.register_unit(unit="m", composition="ft", factor=1)  # Error!

Notes
-----

- ``composition`` must be a valid unit string composed of configured base/derived
  units (for example, ``"N m"``).
- ``factor`` is the scale factor relating the composition to the new unit symbol.