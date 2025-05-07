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
Defines the core QuantityDescriptor class and predefined quantities.

This module provides a structured, extensible way to represent physical quantities
(e.g., pressure, velocity) independently of any product-specific naming conventions.
"""

from dataclasses import dataclass

from ansys.units.base_dimensions import BaseDimensions
from ansys.units.dimensions import Dimensions
from ansys.units.quantity_dimensions import QuantityDimensions


@dataclass(frozen=True)
class QuantityDescriptor:
    """Defines a physical quantity descriptor."""

    name: str
    dimension: Dimensions

    def __hash__(self):
        return hash((self.name, str(self.dimension)))


def _build_quantity_descriptors_from_dimensions() -> dict[str, QuantityDescriptor]:
    catalog = {}
    for attr_name in dir(QuantityDimensions):
        if not attr_name.isupper():
            continue
        dimension = getattr(QuantityDimensions, attr_name)
        if isinstance(dimension, Dimensions):
            catalog[attr_name] = QuantityDescriptor(
                name=attr_name.lower(), dimension=dimension
            )
    return catalog


class QuantityCatalog:
    """A catalogue of physical quantity descriptors."""

    # Load from generator
    _generated = _build_quantity_descriptors_from_dimensions()

    # Inject generated descriptors as class attributes
    for key, descriptor in _generated.items():
        locals()[key] = descriptor

    # Add custom descriptors (e.g., velocity components)
    VELOCITY_X = QuantityDescriptor("velocity x", QuantityDimensions.VELOCITY)
    VELOCITY_Y = QuantityDescriptor("velocity y", QuantityDimensions.VELOCITY)
    VELOCITY_Z = QuantityDescriptor("velocity z", QuantityDimensions.VELOCITY)

    @classmethod
    def all(cls) -> list[QuantityDescriptor]:
        """Return all defined QuantityDescriptors (excluding internal attributes)."""
        return [v for k, v in cls.__dict__.items() if isinstance(v, QuantityDescriptor)]
