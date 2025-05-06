# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
Package initialization for ansys.units.quantity_descriptor.

Exports the QuantityDescriptorCatalog catalog and core interfaces for working with
physical quantities in a product-agnostic way.

Example
-------

.. code-block:: python

    from ansys.units.quantity_descriptor import QuantityDescriptorCatalog
    from ansys.fluent.core.quantity_strategies import FluentSVarStrategy

    quantity = QuantityDescriptorCatalog.PRESSURE
    strategy = FluentSVarStrategy()

    print(strategy.to_string(quantity))
"""

from .quantity_descriptor import QuantityDescriptor, QuantityDescriptorCatalog
from .strategy import ConversionStrategy, MappingConversionStrategy

__all__ = [
    "QuantityDescriptor",
    "QuantityDescriptorCatalog",
    "ConversionStrategy",
    "MappingConversionStrategy",
]
