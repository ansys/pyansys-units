.. _variable_descriptor:

Variable Descriptors
====================

The ``ansys.units.variable_descriptor`` subpackage defines interfaces and implementations for representing physical quantities in a product-agnostic, unit-aware way. These descriptors serve as the foundation for communicating quantity metadata across Ansys systems and external APIs.

Overview
--------

A **VariableDescriptor** encapsulates information about a physical quantity, such as:

- Its name (for example, ``VELOCITY``, ``FORCE``)
- Its associated dimensionality (via ``QuantityDimensions``)
- Optional metadata for display, categorization, or mapping to domain-specific naming schemes

These descriptors are immutable and hashable, making them suitable as keys in mappings and registries.

The subpackage also defines **conversion strategies** that translate between ``VariableDescriptor`` objects and external string representations (such as Fluent variable names).

Main Classes
------------

VariableDescriptor
~~~~~~~~~~~~~~~~~~

.. autoclass:: ansys.units.variable_descriptor.variable_descriptor.VariableDescriptor
   :members:
   :undoc-members:
   :show-inheritance:

Represents a single named physical quantity, including its dimensional signature.

VariableCatalog
~~~~~~~~~~~~~~~

.. autoclass:: ansys.units.variable_descriptor.variable_descriptor.VariableCatalog
   :members:
   :undoc-members:
   :show-inheritance:

A registry of predefined ``VariableDescriptor`` instances for commonly used quantities. These are typically accessed directly by name, such as ``VariableCatalog``.``PRESSURE``.

ConversionStrategy
~~~~~~~~~~~~~~~~~~

.. autoclass:: ansys.units.variable_descriptor.strategy.ConversionStrategy
   :members:
   :undoc-members:
   :show-inheritance:

An abstract base class for strategies that convert ``VariableDescriptor`` objects to and from external string representations.

MappingConversionStrategy
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ansys.units.variable_descriptor.strategy.MappingConversionStrategy
   :members:
   :undoc-members:
   :show-inheritance:

A reusable base class for implementing conversion strategies based on a simple mapping dictionary. Useful for integrating with systems like Fluent, CFX, or external APIs.

Example
-------

This example demonstrates converting a descriptor to a Fluent-style variable name using a custom strategy.

.. code-block:: python

    from ansys.units.variable_descriptor import VariableCatalog
    from ansys.fluent.core.variable_strategies import FluentSVarNamingStrategy

    descriptor = VariableCatalog.VELOCITY
    strategy = FluentSVarNamingStrategy()

    print(strategy.to_string(descriptor))  # for example, "SV_VELOCITY"

You can also define your own mappings for custom naming schemes by subclassing ``MappingConversionStrategy``.

Use Cases
---------

- Abstracting physical quantities from product-specific naming
- Providing consistent and validated input/output definitions
- Bridging Ansys APIs, user interfaces, and internal computation frameworks
