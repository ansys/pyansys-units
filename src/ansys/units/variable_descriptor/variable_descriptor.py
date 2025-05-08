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
    for key, descriptor in _generated.items():
        locals()[key] = descriptor

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
        if hasattr(cls, variable):
            raise ValueError(
                f"Variable name '{variable}' already exists in VariableCatalog. "
                "Please choose a unique name."
            )
        transformed_name = _validate_and_transform_variable(variable)
        setattr(cls, variable, VariableDescriptor(transformed_name, dimension))


# Add custom descriptors
_D = QuantityDimensions
variables = [
    # pressure
    ("ABSOLUTE_PRESSURE", _D.PRESSURE),
    ("DYNAMIC_PRESSURE", _D.PRESSURE),
    # ("STATIC_PRESSURE", _D.PRESSURE),
    ("TOTAL_PRESSURE", _D.PRESSURE),
    ("PRESSURE_COEFFICIENT", Dimensions()),
    # velocity
    ("AXIAL_VELOCITY", _D.VELOCITY),
    ("CELL_CONVECTIVE_COURANT_NUMBER", Dimensions()),
    ("CELL_REYNOLDS_NUMBER", Dimensions()),
    # The dominant meaning of helicity comes from
    # particle physics where it is dimensionless.
    # In CFD, where it has a different
    # meaning, it usually has dimension L^2T^-2.
    # In Fluent it is LT^-2.
    ("FLUENT_FLUID_HELICITY", _D.ACCELERATION),
    # Lambda 2 criterion is documented as dimensionless
    # but is T^-2 in Fluent.
    ("FLUENT_LAMBDA_2_CRITERION", _D.TIME**-2),
    ("MESH_VELOCITY", _D.VELOCITY),
    ("MESH_VELOCITY_MAG", _D.VELOCITY),
    ("MESH_VELOCITY_X", _D.VELOCITY),
    ("MESH_VELOCITY_Y", _D.VELOCITY),
    ("MESH_VELOCITY_Z", _D.VELOCITY),
    # What Fluent calls the raw Q-criterion (to distinguish from
    # normalized) is just the Q-criterion so we omit the raw part.
    ("Q_CRITERION", _D.TIME**-2),
    ("Q_CRITERION_NORMALIZED", Dimensions()),
    ("RADIAL_VELOCITY", _D.VELOCITY),
    ("TANGENTIAL_VELOCITY", _D.VELOCITY),
    ("VELOCITY_ANGLE", _D.ANGLE),
    ("VELOCITY_MAGNITUDE", _D.VELOCITY),
    ("VELOCITY_X", _D.VELOCITY),
    ("VELOCITY_Y", _D.VELOCITY),
    ("VELOCITY_Z", _D.VELOCITY),
    ("VORTICITY", _D.TIME**-1),
    ("VORTICITY_MAG", _D.TIME**-1),
    ("VORTICITY_X", _D.TIME**-1),
    ("VORTICITY_Y", _D.TIME**-1),
    ("VORTICITY_Z", _D.TIME**-1),
    # density
    ("FLUENT_FLUID_DENSITY_ALL", _D.DENSITY),
    # properties
    # consider moving to the quantity_dimensions.
    ("PRANDTL_NUMBER", Dimensions()),
    # turbulence
    ("EFFECTIVE_PRANDTL_NUMBER", Dimensions()),
    ("EFFECTIVE_THERMAL_CONDUCTIVITY", _D.THERMAL_CONDUCTIVITY),
    ("EFFECTIVE_VISCOSITY", _D.DYNAMIC_VISCOSITY),
    ("PRODUCTION_OF_K", _D.MASS * _D.LENGTH**-1 * _D.TIME**-3),
    ("SPECIFIC_DISSIPATION_RATE", _D.TIME**-1),
    ("TURBULENT_DISSIPATION_RATE", _D.LENGTH**2 * _D.TIME**3),
    ("TURBULENT_INTENSITY", Dimensions()),
    ("TURBULENT_VISCOSITY", _D.DYNAMIC_VISCOSITY),
    ("TURBULENT_VISCOSITY_RATIO", Dimensions()),
    ("TURBULENT_REYNOLDS_NUMBER", Dimensions()),
    ("TURBULENT_KINETIC_ENERGY", _D.LENGTH**2 * _D.TIME**-2),
    ("WALL_Y_PLUS", Dimensions()),
    ("WALL_Y_STAR", Dimensions()),
    # wall fluxes
    (
        "SURFACE_HEAT_TRANSFER_COEFFICIENT",
        _D.POWER * _D.LENGTH**-2 * _D.TEMPERATURE**-1,
    ),
    ("SKIN_FRICTION_COEFFICIENT", Dimensions()),
    ("SURFACE_HEAT_FLUX", _D.HEAT_FLUX_DENSITY),
    ("SURFACE_NUSSELT_NUMBER", Dimensions()),
    ("SURFACE_STANTON_NUMBER", Dimensions()),
    (
        "WALL_ADJACENT_HEAT_TRANSFER_COEFFICIENT",
        _D.POWER * _D.LENGTH**-2 * _D.TEMPERATURE**-1,
    ),
    ("WALL_SHEAR_STRESS", _D.STRESS),
    ("WALL_SHEAR_STRESS_MAG", _D.STRESS),
    ("WALL_SHEAR_STRESS_X", _D.STRESS),
    ("WALL_SHEAR_STRESS_Y", _D.STRESS),
    ("WALL_SHEAR_STRESS_Z", _D.STRESS),
    (
        "Y_PLUS_BASED_HEAT_TRANSFER_COEFFICIENT",
        _D.POWER * _D.LENGTH**-2 * _D.TEMPERATURE**-1,
    ),
    # residuals
    ("MASS_IMBALANCE", _D.MASS * _D.TIME**-1),
    # derivatives
    ("PRESSURE_HESSIAN_INDICATOR", Dimensions()),
    ("STRAIN_RATE", _D.TIME**-1),
    ("DVELOCITY_DX", _D.TIME**-1),
    ("DVELOCITY_DX_MAG", _D.TIME**-1),
    ("DVELOCITY_DX_X", _D.TIME**-1),
    ("DVELOCITY_DX_Y", _D.TIME**-1),
    ("DVELOCITY_DX_Z", _D.TIME**-1),
    ("DVELOCITY_DY", _D.TIME**-1),
    ("DVELOCITY_DY_MAG", _D.TIME**-1),
    ("DVELOCITY_DY_X", _D.TIME**-1),
    ("DVELOCITY_DY_Y", _D.TIME**-1),
    ("DVELOCITY_DY_Z", _D.TIME**-1),
    ("DVELOCITY_DZ", _D.TIME**-1),
    ("DVELOCITY_DZ_MAG", _D.TIME**-1),
    ("DVELOCITY_DZ_X", _D.TIME**-1),
    ("DVELOCITY_DZ_Y", _D.TIME**-1),
    ("DVELOCITY_DZ_Z", _D.TIME**-1),
    # thermodynamics
    ("SPECIFIC_ENTHALPY", _D.ENTHALPY / _D.MASS),
    ("SPECIFIC_ENTROPY", _D.ENTROPY / _D.MASS),
    ("SPECIFIC_INTERNAL_ENERGY", _D.ENERGY / _D.MASS),
    ("SPECIFIC_TOTAL_ENERGY", _D.ENERGY / _D.MASS),
    # mesh
    ("ABSOLUTE_ANGULAR_COORDINATE", _D.ANGLE),
    ("ANGULAR_COORDINATE", _D.ANGLE),
    ("ANISOTROPIC_ADAPTION_CELLS", Dimensions()),
    ("AXIAL_COORDINATE", _D.LENGTH),
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
    ("COORDINATE", _D.LENGTH),
    ("COORDINATE_MAG", _D.LENGTH),
    ("COORDINATE_X", _D.LENGTH),
    ("COORDINATE_Y", _D.LENGTH),
    ("COORDINATE_Z", _D.LENGTH),
    ("RADIAL_COORDINATE", _D.LENGTH),
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

for name, dimension in variables:
    VariableCatalog.add(name, dimension)
