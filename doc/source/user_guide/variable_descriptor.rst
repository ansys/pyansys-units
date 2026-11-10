.. _variable_descriptor:

Variable Descriptors
====================

The ``ansys.variable_descriptor`` package defines interfaces and implementations for representing physical quantities in a product-agnostic, unit-aware way. These descriptors serve as the foundation for communicating quantity metadata across Ansys systems and external APIs. It builds on ``ansys.units`` and is installed with the ``ansys-units`` distribution.

Overview
--------

A **VariableDescriptor** encapsulates information about a physical quantity, such as:

- Its name (for example, ``VELOCITY``, ``FORCE``)
- Its associated dimensionality (via ``QuantityDimensions``)
- Optional metadata for display, categorization, or mapping to domain-specific naming schemes

These descriptors are immutable and hashable, making them suitable as keys in mappings and registries.

The package also defines **conversion strategies** that translate between ``VariableDescriptor`` objects and external string representations (such as the variable names used by a particular solver or file format).

Main Classes
------------

QuantityKind
~~~~~~~~~~~~

.. autoclass:: ansys.variable_descriptor.variable_descriptor.QuantityKind
   :members:
   :undoc-members:
   :show-inheritance:

VariableDescriptor
~~~~~~~~~~~~~~~~~~

.. autoclass:: ansys.variable_descriptor.variable_descriptor.VariableDescriptor
   :members:
   :undoc-members:
   :show-inheritance:

Represents a single named physical quantity, including its dimensional signature.
The kind of quantity (scalar or vector) is indicated by the ``QuantityKind`` enumeration.

.. data:: ansys.variable_descriptor.ScalarVariableDescriptor
   :no-index:

   A type alias for scalar variable descriptors.

.. data:: ansys.variable_descriptor.VectorVariableDescriptor
   :no-index:

   A type alias for vector variable descriptors.

VariableCatalog
~~~~~~~~~~~~~~~

.. autoclass:: ansys.variable_descriptor._generated_variable_descriptor.VariableCatalog
   :members:
   :undoc-members:
   :show-inheritance:

A registry of predefined ``VariableDescriptor`` instances for commonly used quantities. These are typically accessed directly by name, such as ``VariableCatalog``.``PRESSURE``.

ConversionStrategy
~~~~~~~~~~~~~~~~~~

.. autoclass:: ansys.variable_descriptor.strategy.ConversionStrategy
   :members:
   :undoc-members:
   :show-inheritance:

An abstract base class for strategies that convert ``VariableDescriptor`` objects to and from external string representations.

MappingConversionStrategy
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ansys.variable_descriptor.strategy.MappingConversionStrategy
   :members:
   :undoc-members:
   :show-inheritance:

A reusable base class for implementing conversion strategies based on a simple mapping dictionary. Useful for integrating with simulation products, file formats, or external APIs.

Example
-------

This example demonstrates converting descriptors to and from a custom naming scheme by subclassing ``MappingConversionStrategy``.

.. code-block:: python

    from ansys.variable_descriptor import MappingConversionStrategy, VariableCatalog


    class MyNamingStrategy(MappingConversionStrategy):
        _mapping = {
            VariableCatalog.PRESSURE: "p",
            VariableCatalog.VELOCITY: "U",
        }


    strategy = MyNamingStrategy()

    print(strategy.to_string(VariableCatalog.VELOCITY))  # "U"
    print(strategy.to_variable_descriptor("p") == VariableCatalog.PRESSURE)  # True

Applications that need different behavior can subclass ``ConversionStrategy`` directly.

Use Cases
---------

- Abstracting physical quantities from product-specific naming
- Providing consistent and validated input/output definitions
- Bridging Ansys APIs, user interfaces, and internal computation frameworks
