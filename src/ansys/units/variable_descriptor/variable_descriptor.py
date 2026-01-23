# pyright: reportUnannotatedClassAttribute=false

# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
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

This module provides a structured, extensible way to represent variables based on
physical quantities (e.g., pressure, velocity) independently of any product-specific
naming conventions.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Generic, Literal

from typing_extensions import TypeVar

from ansys.units.base_dimensions import BaseDimensions
from ansys.units.dimensions import Dimensions
from ansys.units.quantity_dimensions import QuantityDimensions


class QuantityKind(Enum):
    """Enumeration for :class:`VariableDescriptor`."""

    SCALAR = "scalar"
    VECTOR = "vector"


QuantityKindT = TypeVar(
    "QuantityKindT", bound=QuantityKind, default=QuantityKind, covariant=True
)


@dataclass(frozen=True, unsafe_hash=True)
class VariableDescriptor(Generic[QuantityKindT]):
    """Defines a physical quantity variable descriptor."""

    dimension: Dimensions
    name: str = field(init=False)

    def __set_name__(self, _, name: str) -> None:
        object.__setattr__(self, "name", _validate_and_transform_variable(name))


ScalarVariableDescriptor = VariableDescriptor[
    Literal[QuantityKind.SCALAR]
]  #: Type alias for scalar variables
VectorVariableDescriptor = VariableDescriptor[
    Literal[QuantityKind.VECTOR]
]  #: Type alias for vector variables


def _validate_and_transform_variable(variable: str) -> str:
    """
    Validate and transform a variable name.

    Ensures the variable name is uppercase and returns its lowercase equivalent.

    Parameters
    ----------
    variable : str
        The name of the variable.

    Returns
    -------
    str
        The lowercase equivalent of the variable name.

    Raises
    ------
    ValueError
        If the variable name is not uppercase.
    """
    if not variable.isupper():
        raise ValueError(
            f"Variable names in VariableCatalog must be uppercase. "
            f"Invalid name: '{variable}'."
        )
    return variable.lower()


_D = QuantityDimensions
_B = BaseDimensions
_Q = QuantityKind


class VariableCatalogBase:
    """A catalog of variable descriptors."""

    @classmethod
    def all(cls) -> dict[str, list[VariableDescriptor]]:
        """
        Return all defined
        :class:`~ansys.units.variable_descriptor.variable_descriptor.VariableDescriptor`
        objects, organized by subcategory.

        Returns
        -------
        dict[str, list[VariableDescriptor]]
            A dictionary where keys are subcategory names (or "main" for the top-level catalog)
            and values are lists of :class:`~ansys.units.variable_descriptor.variable_descriptor.VariableDescriptor` instances.
        """  # noqa: E501
        result = {"main": []}

        for key, value in cls.__dict__.items():
            if isinstance(value, VariableDescriptor):
                result["main"].append(value)
            elif (
                isinstance(value, type)
                and issubclass(value, object)
                and value is not object
            ):
                # Collect descriptors from subcategories
                subcategory_name = key
                result[subcategory_name] = [
                    v
                    for k, v in value.__dict__.items()
                    if isinstance(v, VariableDescriptor)
                ]

        return result

    @classmethod
    def add(
        cls, variable: str, dimension: Dimensions, subcategory: str | None = None
    ) -> None:
        """
        Add a variable to the catalog.

        Parameters
        ----------
        variable : str
            The name of the variable (must be uppercase).
        dimension : Dimensions
            The dimension of the variable.
        subcategory: str|None
            The optional subcategory for the variable.

        Raises
        ------
        ValueError
            The variable name is not uppercase or already exists.
        """
        _validate_and_transform_variable(
            variable
        )  # Validate variable name before adding to prevent invalid state

        # Determine the target category (main catalog or subcategory)
        target = cls
        if subcategory:
            # Ensure the subcategory exists as an attribute
            if not hasattr(cls, subcategory):
                # Create the subcategory and assign a docstring
                subcategory_class = type(
                    subcategory,
                    (object,),
                    {
                        "__doc__": (
                            f"Dictionary of variable descriptors for {subcategory}-related "
                            f"quantities."
                        )
                    },
                )
                setattr(cls, subcategory, subcategory_class)
            target = getattr(cls, subcategory)

        # Check if the variable already exists in the target category
        if hasattr(target, variable):
            raise ValueError(
                f"Variable name '{variable}' already exists in the '{subcategory or 'main'}' "
                "catalog. Please choose a unique name."
            )

        # Add the variable to the target category
        descriptor = VariableDescriptor(dimension)
        descriptor.__set_name__(target, variable)
        setattr(target, variable, descriptor)
