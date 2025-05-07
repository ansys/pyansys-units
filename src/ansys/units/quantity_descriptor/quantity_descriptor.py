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
from enum import Enum

from ansys.units import BaseDimensions, Dimensions


@dataclass(frozen=True)
class QuantityDescriptor:
    """Defines a physical quantity descriptor."""

    name: str  # Human-readable name
    dimension: Dimensions
    si_unit: str  # Preferred SI unit (e.g., "Pa", "m/s", "K")

    def __hash__(self):
        # Use a tuple of the attributes to compute the hash.
        # N.b. `Dimensions` is not directly hashable.
        return hash((self.name, str(self.dimension), self.si_unit))

class QuantityDescriptorCatalog:
    """A catalogue of physical quantity descriptors."""

    _b = BaseDimensions

    PRESSURE = QuantityDescriptor(
        "pressure",
        Dimensions(dimensions={_b.MASS: 1, _b.LENGTH: -1, _b.TIME: -2}),
        "Pa"
    )
    VELOCITY_X = QuantityDescriptor(
        "velocity x",
        Dimensions(dimensions={_b.LENGTH: 1, _b.TIME: -1}),
        "m/s"
    )
    TEMPERATURE = QuantityDescriptor(
        "temperature",
        Dimensions(dimensions={_b.TEMPERATURE: 1}),
        "K"
    )
    # Add more quantities as needed
