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
Defines the core VariableDescriptor class and predefined quantities.

This module provides a structured, extensible way to represent variables based on physical quantities
(e.g., pressure, velocity) independently of any product-specific naming conventions.
"""

from dataclasses import dataclass

from ansys.units.dimensions import Dimensions
from ansys.units.quantity_dimensions import QuantityDimensions


@dataclass(frozen=True)
class VariableDescriptor:
    """Defines a physical quantity variable descriptor."""

    name: str
    dimension: Dimensions

    def __hash__(self):
        return hash((self.name, str(self.dimension)))


def _build_variable_descriptors_from_dimensions() -> dict[str, VariableDescriptor]:
    """
    Generate a dictionary of variable descriptors from QuantityDimensions.

    This function iterates over all uppercase attributes in QuantityDimensions
    and creates VariableDescriptor instances for each valid dimension.
    """
    catalog = {}
    for attr_name in dir(QuantityDimensions):
        if not attr_name.isupper():
            continue
        dimension = getattr(QuantityDimensions, attr_name)
        if isinstance(dimension, Dimensions):
            catalog[attr_name] = VariableDescriptor(
                name=attr_name.lower(), dimension=dimension
            )
    return catalog


class VariableCatalog:
    """A catalog of variable descriptors."""

    # Load from generator
    _generated = _build_variable_descriptors_from_dimensions()

    # Inject generated descriptors as class attributes
    for key, descriptor in _generated.items():
        locals()[key] = descriptor

    # Add custom descriptors (e.g., velocity components)
    VELOCITY_X = VariableDescriptor("velocity x", QuantityDimensions.VELOCITY)
    VELOCITY_Y = VariableDescriptor("velocity y", QuantityDimensions.VELOCITY)
    VELOCITY_Z = VariableDescriptor("velocity z", QuantityDimensions.VELOCITY)

    @classmethod
    def all(cls) -> list[VariableDescriptor]:
        """Return all defined `VariableDescriptor`s (excluding internal attributes)."""
        return [v for k, v in cls.__dict__.items() if isinstance(v, VariableDescriptor)]
    
    @classmethod
    def add(cls, variable: str, dimension: Dimensions) -> None:
        """
        Add a variable to the catalog.

        Parameters
        ----------
        variable : str
            The name of the variable (must be uppercase).
        dimension : Dimensions
            The dimension of the variable.

        Raises
        ------
        ValueError
            The variable name is not uppercase or already exists.
        """
        if not variable.isupper():
            raise ValueError(
                f"Variable names in VariableCatalog must be uppercase. "
                f"Invalid name: '{variable}'."
            )
        if hasattr(cls, variable):
            raise ValueError(
                f"Variable name '{variable}' already exists in VariableCatalog. "
                "Please choose a unique name."
            )
        setattr(
            cls,
            variable,
            VariableDescriptor(variable.lower(), dimension)
        )
