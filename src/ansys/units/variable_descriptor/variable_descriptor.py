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

This module provides a structured, extensible way to represent variables based on
physical quantities (e.g., pressure, velocity) independently of any product-specific
naming conventions.
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


def _build_variable_descriptors_from_dimensions() -> dict[str, VariableDescriptor]:
    """
    Generate a dictionary of variable descriptors from QuantityDimensions.

    This function iterates over all uppercase attributes in QuantityDimensions and
    creates VariableDescriptor instances for each valid dimension.
    """
    catalog = {}
    for attr_name in dir(QuantityDimensions):
        dimension = getattr(QuantityDimensions, attr_name)
        if isinstance(dimension, Dimensions):
            catalog[attr_name] = VariableDescriptor(
                name=_validate_and_transform_variable(attr_name), dimension=dimension
            )
    return catalog


class VariableCatalog:
    """A catalog of variable descriptors."""

    # Load from generator
    _generated = _build_variable_descriptors_from_dimensions()

    # Inject generated descriptors as class attributes
    for _key, _descriptor in _generated.items():
        locals()[_key] = _descriptor

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
        # Validate and transform the variable name
        transformed_name = _validate_and_transform_variable(variable)

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
        setattr(target, variable, VariableDescriptor(transformed_name, dimension))


# Add custom descriptors
_D = QuantityDimensions
fluent_variables = [
    # velocity
    # The dominant meaning of helicity comes from
    # particle physics where it is dimensionless.
    # In CFD, where it has a different
    # meaning, it usually has dimension L^2 T^-2.
    # In Fluent it is L T^-2.
    ("HELICITY", _D.ACCELERATION),
    # Lambda 2 criterion is documented as dimensionless
    # but is T^-2 in Fluent.
    ("LAMBDA_2_CRITERION", _D.TIME**-2),
    ("DENSITY_ALL", _D.DENSITY),
    (
        "Y_PLUS_BASED_HEAT_TRANSFER_COEFFICIENT",
        _D.POWER * _D.LENGTH**-2 * _D.TEMPERATURE**-1,
    ),
    ("TOTAL_ENTHALPY_DEVIATION", _D.SPECIFIC_ENTHALPY),
    # residuals
    ("MASS_IMBALANCE", _D.MASS * _D.TIME**-1),
    # derivatives
    ("PRESSURE_HESSIAN_INDICATOR", Dimensions()),
    ("VELOCITY_ANGLE", _D.ANGLE),
    ("DVELOCITY_DX", _D.TIME**-1),
    ("DVELOCITY_DX_MAGNITUDE", _D.TIME**-1),
    ("DVELOCITY_DX_X", _D.TIME**-1),
    ("DVELOCITY_DX_Y", _D.TIME**-1),
    ("DVELOCITY_DX_Z", _D.TIME**-1),
    ("DVELOCITY_DY", _D.TIME**-1),
    ("DVELOCITY_DY_MAGNITUDE", _D.TIME**-1),
    ("DVELOCITY_DY_X", _D.TIME**-1),
    ("DVELOCITY_DY_Y", _D.TIME**-1),
    ("DVELOCITY_DY_Z", _D.TIME**-1),
    ("DVELOCITY_DZ", _D.TIME**-1),
    ("DVELOCITY_DZ_MAGNITUDE", _D.TIME**-1),
    ("DVELOCITY_DZ_X", _D.TIME**-1),
    ("DVELOCITY_DZ_Y", _D.TIME**-1),
    ("DVELOCITY_DZ_Z", _D.TIME**-1),
]

for name, dimension in fluent_variables:
    VariableCatalog.add(name, dimension, "fluent")


mesh_variables = [
    # mesh
    ("ANISOTROPIC_ADAPTION_CELLS", Dimensions()),
    ("BOUNDARY_CELL_DISTANCE", Dimensions()),
    ("BOUNDARY_LAYER_CELLS", Dimensions()),
    ("BOUNDARY_NORMAL_DISTANCE", Dimensions()),
    ("BOUNDARY_VOLUME_DISTANCE", Dimensions()),
    ("CELL_EQUIANGLE_SKEW", Dimensions()),
    ("CELL_EQUIVOLUME_SKEW", Dimensions()),
    ("CELL_PARENT_INDEX", Dimensions()),
    ("CELL_REFINE_LEVEL", Dimensions()),
    ("CELL_VOLUME", _D.VOLUME),
    ("CELL_VOLUME_CHANGE", Dimensions()),
    ("ELEMENT_ASPECT_RATIO", Dimensions()),
    ("ELEMENT_WALL_DISTANCE", _D.LENGTH),
    ("FACE_AREA_MAGNITUDE", _D.AREA),
    ("FACE_HANDEDNESS", Dimensions()),
    ("INTERFACE_OVERLAP_FRACTION", Dimensions()),
    ("MARK_POOR_ELEMENTS", Dimensions()),
    ("SMOOTHED_CELL_REFINE_LEVEL", Dimensions()),
    ("X_FACE_AREA", _D.AREA),
    ("Y_FACE_AREA", _D.AREA),
    ("Z_FACE_AREA", _D.AREA),
    # cell info
    ("ACTIVE_CELL_PARTITION", Dimensions()),
    ("CELL_ELEMENT_TYPE", Dimensions()),
    ("CELL_ID", Dimensions()),
    ("CELL_WEIGHT", Dimensions()),
    ("CELL_ZONE_INDEX", Dimensions()),
    ("CELL_ZONE_TYPE", Dimensions()),
    ("PARTITION_NEIGHBOURS", Dimensions()),
    ("STORED_CELL_PARTITIION", Dimensions()),
]

for name, dimension in mesh_variables:
    VariableCatalog.add(name, dimension, "mesh")
