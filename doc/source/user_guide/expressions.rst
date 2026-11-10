.. _expressions:

Expressions
===========

The ``ansys.expressions`` package builds, parses, and renders unit-aware expression
trees in a product-agnostic way. It builds on ``ansys.units`` and
``ansys.variable_descriptor`` and is installed with the ``ansys-units`` distribution.

Expression trees store neutral data only. For example, a variable node stores its
``VariableDescriptor`` rather than a product-specific name. Everything that differs
between products is supplied by a ``Dialect``:

- ``naming``: a ``ConversionStrategy`` that converts variable descriptors to and from
  the product's variable names.
- ``functions``: a ``FunctionRegistry`` of the functions the product's expression
  language provides, organized in groups.

``DEFAULT_DIALECT`` names variables by their catalog name (for example
``absolute_pressure``) and provides no functions.

Define a dialect
----------------

.. code-block:: python

    from ansys.expressions import (
        Dialect,
        ExpressionBuilder,
        FunctionRegistry,
        Kind,
        Param,
        Signature,
    )
    from ansys.variable_descriptor import MappingConversionStrategy, VariableCatalog


    class MyNames(MappingConversionStrategy):
        _mapping = {
            VariableCatalog.ABSOLUTE_PRESSURE: "P",
            VariableCatalog.TEMPERATURE: "T",
        }


    functions = FunctionRegistry()
    functions.register(
        "reductions",
        Signature(
            "AreaAve",
            "area_ave",
            (Param("expression", Kind.SCALAR), Param("locations", Kind.LOCATION_LIST)),
        ),
    )

    dialect = Dialect("my_product", naming=MyNames(), functions=functions)

Build and render expressions
----------------------------

Function groups registered in the dialect are available as builder attributes. Python
operators compose expressions, and ``str()`` renders them with the dialect they were
built with.

.. code-block:: python

    builder = ExpressionBuilder(dialect)

    dp = builder.reductions.area_ave(
        VariableCatalog.ABSOLUTE_PRESSURE, ["inlet"]
    ) - builder.reductions.area_ave(VariableCatalog.ABSOLUTE_PRESSURE, ["outlet"])

    str(dp)  # "(AreaAve(P,['inlet']) - AreaAve(P,['outlet']))"
    dp.render()  # same as str(dp)

Expressions built for different dialects cannot be combined.

Parse expressions
-----------------

``parse`` converts an expression string back into a tree, resolving variable and
function names through a dialect:

.. code-block:: python

    from ansys.expressions import parse

    tree = parse("AreaAve(P,['inlet']) * 2", dialect)
    str(tree)  # "(AreaAve(P,['inlet']) * 2)"

Discover legal values
---------------------

Each function parameter exposes the values that are legal in the current context. The
values come from a ``Discovery`` object. ``StaticDiscovery`` is used by default; products
can implement the ``Discovery`` protocol on top of a live session.

.. code-block:: python

    from ansys.expressions import StaticDiscovery

    builder = ExpressionBuilder(dialect, StaticDiscovery(dialect, locations=["inlet"]))
    builder.reductions.area_ave.locations.allowed_values()  # ["inlet"]
    builder.reductions.area_ave.locations.is_allowed("outlet")  # False
