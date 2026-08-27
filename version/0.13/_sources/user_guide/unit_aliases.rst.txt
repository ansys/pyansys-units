.. _unit_aliases:

============
Unit aliases
============

PyAnsys Units supports **unit aliases**, allowing you to use shorthand or
alternative names for units. For example, you can write ``deg`` instead of
``degree``, ``meter`` instead of ``m``, or ``newton`` instead of ``N``.

Aliases resolve transparently to their canonical unit names during parsing,
so they work everywhere a unit string is accepted: ``Unit()``, ``Quantity()``,
compound unit strings, and conversions.

Built-in aliases
----------------

A set of common aliases is shipped out of the box in the ``cfg.yaml``
configuration file. Some examples:

.. list-table::
   :header-rows: 1
   :widths: 30 30

   * - Alias
     - Canonical unit
   * - ``deg``
     - ``degree``
   * - ``rad``
     - ``radian``
   * - ``sec``
     - ``s``
   * - ``meter`` / ``metre``
     - ``m``
   * - ``kilogram``
     - ``kg``
   * - ``foot`` / ``feet``
     - ``ft``
   * - ``newton``
     - ``N``
   * - ``pascal``
     - ``Pa``
   * - ``watt``
     - ``W``
   * - ``joule``
     - ``J``
   * - ``volt``
     - ``V``
   * - ``hertz``
     - ``Hz``
   * - ``liter`` / ``litre``
     - ``l``

Using aliases
-------------

Aliases can be used anywhere you would normally write a unit name:

.. code-block:: python

    from ansys.units import Unit, Quantity

    # Create a unit from an alias
    angle = Unit("deg")  # resolves to "degree"
    length = Unit("meter")  # resolves to "m"

    # Create quantities with aliases
    q = Quantity(90, "deg")  # 90.0 degree

    # Aliases work inside compound unit strings
    angular_vel = Unit("deg sec^-1")  # "degree s^-1"
    accel = Unit("meter sec^-2")  # "m s^-2"

    # Conversions work normally
    q_rad = Quantity(180, "deg").to("radian")

Alias equality
--------------

A unit created from an alias is identical to the canonical unit. They share
the same dimensions, SI scaling factor, and SI offset:

.. code-block:: python

    from ansys.units import Unit

    assert Unit("deg") == Unit("degree")
    assert Unit("rad") == Unit("radian")
    assert Unit("meter") == Unit("m")

Registering custom aliases
--------------------------

You can register your own aliases at runtime using the
``UnitRegistry.register_alias()`` method:

.. code-block:: python

    from ansys.units import Unit, UnitRegistry

    ureg = UnitRegistry()
    ureg.register_alias("angular_deg", "degree")

    u = Unit("angular_deg")  # resolves to "degree"

The method validates that:

- The alias does not shadow an existing base unit, derived unit, or alias
  (raises ``AliasAlreadyRegistered``).
- The canonical target is a configured unit or an existing alias
  (raises ``ValueError``).
- Neither argument is empty (raises ``ValueError``).

Aliases can also point to other aliases. The resolution follows the chain
transitively until a canonical unit is reached:

.. code-block:: python

    ureg.register_alias("my_angle", "deg")  # "deg" -> "degree"
    Unit("my_angle")  # resolves to "degree"

.. note::
   Aliases registered programmatically via ``register_alias()`` are added to the
   global alias table. They take effect immediately for all subsequent
   ``Unit()`` and ``Quantity()`` calls in the same process. They are not
   persisted across sessions.
