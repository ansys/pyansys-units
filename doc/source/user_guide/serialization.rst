.. _serialization:

=============
Serialization
=============

PyAnsys Units can save quantities and units to dictionaries, JSON, strings, and
pickle files, and restore them.

Dictionaries
------------

``to_dict()`` returns built-in Python types only. Array values become nested lists,
and extra fields given to the ``Quantity`` constructor are kept:

.. code:: python

    from ansys.units import Quantity, Unit

    q = Quantity([1.0, 2.0], "m s^-1", source="sensor")
    data = q.to_dict()  # {'value': [1.0, 2.0], 'units': 'm s^-1', 'source': 'sensor'}
    Quantity.from_dict(data)  # Quantity ([1. 2.], "m s^-1")

    Unit("kg m^-3").to_dict()  # {'units': 'kg m^-3'}
    Unit.from_dict({"units": "kg m^-3"})  # Unit("kg m^-3")

JSON
----

``Quantity`` works as a field in `Pydantic <https://docs.pydantic.dev/>`_ models,
which use the same dictionary format:

.. code:: python

    from pydantic import BaseModel, ConfigDict
    from ansys.units import Quantity


    class Measurement(BaseModel):
        # Keep NaN and infinity, which are written as null by default.
        model_config = ConfigDict(ser_json_inf_nan="constants")

        length: Quantity


    text = Measurement(length=Quantity(2.0, "m")).model_dump_json()
    Measurement.model_validate_json(text).length  # Quantity (2.0, "m")

Without Pydantic, use the ``json`` module with ``to_dict()`` and ``from_dict()``:

.. code:: python

    import json
    from ansys.units import Quantity

    text = json.dumps(Quantity(2.0, "m").to_dict())
    Quantity.from_dict(json.loads(text))  # Quantity (2.0, "m")

Strings
-------

``Quantity.from_string()`` parses the output of ``str(quantity)``:

.. code:: python

    from ansys.units import Quantity

    Quantity.from_string("5.0 m s^-1")  # Quantity (5.0, "m s^-1")
    Quantity.from_string(str(Quantity([1.0, 2.0], "kg")))  # Quantity ([1. 2.], "kg")

NumPy shortens the string of large arrays with ``...``. Such strings can't be
parsed, so use ``to_dict()`` for large arrays.

Pickle
------

Units are pickled by name and resolved again when loaded from a pickle. Pickle
files created with earlier versions of PyAnsys Units can still be loaded.

Custom units
------------

Units are stored by name. Custom units registered with
:meth:`~ansys.units.UnitRegistry.register_unit` are also stored with their
definition, so they can be restored without the registry:

.. code:: python

    from ansys.units import Quantity, UnitRegistry

    ureg = UnitRegistry()
    ureg.register_unit(unit="micron", composition="m", factor=1e-6)

    data = ureg.Quantity(3.0, "micron").to_dict()
    # {'value': 3.0, 'units': 'micron',
    #  'unit_definition': {'composition': 'm', 'factor': 1e-06}}

    Quantity.from_dict(data).to("m")  # Quantity (3e-06, "m")

When loading, a unit name is looked up in this order:

#. The ``registry`` argument of ``from_dict()`` or ``from_string()``.
#. The registry set with ``set_application_registry()``. Loading from a pickle
   also uses this registry.
#. The built-in units.

.. code:: python

    import pickle
    from ansys.units import Quantity, UnitRegistry, set_application_registry

    ureg = UnitRegistry()
    ureg.register_unit(unit="micron", composition="m", factor=1e-6)
    set_application_registry(ureg)

    Quantity.from_string("3.0 micron")  # Quantity (3.0, "micron")
    pickle.loads(pickle.dumps(ureg.Quantity(3.0, "micron")))  # Quantity (3.0, "micron")

If the stored definition of a custom unit differs from the unit with the same name
in the registry, loading raises a ``ConflictingUnitDefinition`` error rather than
returning wrong values. A unit name that can't be resolved raises an
``UnresolvableUnit`` error.
