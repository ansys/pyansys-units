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
from typing import Generic, Literal, final

from typing_extensions import TypeVar

from ansys.units import BaseDimensions
from ansys.units.dimensions import Dimensions
from ansys.units.quantity_dimensions import QuantityDimensions


class QuantityKind(Enum):
    """Enumeration for variable dimensionality."""

    SCALAR = "scalar"
    VECTOR = "vector"


QuantityKindT = TypeVar(
    "QuantityKindT", bound=QuantityKind, default=QuantityKind, covariant=True
)


@dataclass(frozen=True)
class VariableDescriptor(Generic[QuantityKindT]):
    """Defines a physical quantity variable descriptor."""

    dimension: Dimensions
    name: str = field(init=False)

    def __hash__(self) -> int:
        return hash((self.name, str(self.dimension)))

    def __set_name__(self, _, name: str) -> None:
        object.__setattr__(self, "name", name.lower())


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


@final
class VariableCatalog:
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
        descriptor = VariableDescriptor(dimension)
        descriptor.__set_name__(target, variable)
        setattr(target, variable, descriptor)

    # region autogenerated variables
    ABSOLUTE_PRESSURE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    ABSORBANCE = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    ABSORBED_DOSE_RATE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -3.0})
    )
    ACCELERATION = VariableDescriptor[Literal[_Q.VECTOR]](
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    ACCELERATION_MAGNITUDE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    ACCELERATION_X = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    ACCELERATION_Y = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    ACCELERATION_Z = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    ACOUSTICAL_ABSORPTION = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    ACTION = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -1.0})
    )
    ANGLE = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({_B.ANGLE: 1.0}))
    ANGULAR_ACCELERATION = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.TIME: -2.0})
    )
    ANGULAR_MOMENTUM = VariableDescriptor[Literal[_Q.VECTOR]](
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -1.0})
    )
    ANGULAR_MOMENTUM_MAGNITUDE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -1.0})
    )
    ANGULAR_MOMENTUM_X = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -1.0})
    )
    ANGULAR_MOMENTUM_Y = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -1.0})
    )
    ANGULAR_MOMENTUM_Z = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -1.0})
    )
    ANGULAR_VELOCITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.TIME: -1.0})
    )
    AREA = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({_B.LENGTH: 2.0}))
    AREA_DENSITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -2.0})
    )
    ATOMIC_MASS = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({_B.MASS: 1.0}))
    ATOMIC_NUMBER = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    ATTENUATION_COEFFICIENT = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: -1.0})
    )
    AXIAL_VELOCITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    BIREFRINGENCE = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    BULK_MODULUS = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    CAPACITANCE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: -1.0, _B.LENGTH: -2.0, _B.TIME: 4.0, _B.CURRENT: 2.0})
    )
    CATALYTIC_EFFICIENCY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 3.0, _B.CHEMICAL_AMOUNT: -1.0, _B.TIME: -1.0})
    )
    CELL_REYNOLDS_NUMBER = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    CHEMICAL_AMOUNT = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.CHEMICAL_AMOUNT: 1.0})
    )
    COEFFICIENT_OF_RESTITUTION = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    COLOR = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    COMPRESSIBILITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: -1.0, _B.LENGTH: 1.0, _B.TIME: 2.0})
    )
    COMPRESSIVE_STRENGTH = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    CONVECTIVE_COURANT_NUMBER = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    CORROSION_RESISTANCE = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    CREEP = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({_B.TIME: -1.0}))
    CURIE_TEMPERATURE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.TEMPERATURE: 1.0})
    )
    CURRENT = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({_B.CURRENT: 1.0}))
    DENSITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -3.0})
    )
    DIAMAGNETISM = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    DIELECTRIC_CONSTANT = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    DIELECTRIC_STRENGTH = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -3.0, _B.CURRENT: -1.0})
    )
    DUCTILITY = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    DURABILITY = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    DYNAMIC_PRESSURE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    DYNAMIC_VISCOSITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -1.0})
    )
    EFFECTIVE_PRANDTL_NUMBER = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    EFFECTIVE_THERMAL_CONDUCTIVITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 1.0, _B.MASS: 1.0, _B.TIME: -3.0, _B.TEMPERATURE: -1.0})
    )
    EFFECTIVE_VISCOSITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -1.0})
    )
    ELASTICITY = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    ELECTRICAL_CAPACITANCE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: -1.0, _B.LENGTH: -2.0, _B.TIME: 4.0, _B.CURRENT: 2.0})
    )
    ELECTRICAL_CONDUCTANCE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: -1.0, _B.LENGTH: -2.0, _B.TIME: 3.0, _B.CURRENT: 2.0})
    )
    ELECTRICAL_CONDUCTIVITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: -1.0, _B.LENGTH: -3.0, _B.TIME: 3.0, _B.CURRENT: 2.0})
    )
    ELECTRICAL_IMPEDANCE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0, _B.TIME: -3.0, _B.CURRENT: -2.0})
    )
    ELECTRICAL_INDUCTANCE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0, _B.TIME: -2.0, _B.CURRENT: -2.0})
    )
    ELECTRICAL_POTENTIAL = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0, _B.TIME: -3.0, _B.CURRENT: -1.0})
    )
    ELECTRICAL_REACTANCE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0, _B.TIME: -3.0, _B.CURRENT: -2.0})
    )
    ELECTRICAL_RESISTANCE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0, _B.TIME: -3.0, _B.CURRENT: -2.0})
    )
    ELECTRICAL_RESISTIVITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 3.0, _B.TIME: -3.0, _B.CURRENT: -2.0})
    )
    ELECTRIC_CHARGE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.TIME: 1.0, _B.CURRENT: 1.0})
    )
    ELECTRIC_SUSCEPTIBILITY = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    ELECTROCALORIC_COEFFICIENT = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions(
            {
                _B.TEMPERATURE: 1.0,
                _B.MASS: -1.0,
                _B.LENGTH: -2.0,
                _B.TIME: 3.0,
                _B.CURRENT: 1.0,
            }
        )
    )
    ELECTROSTRICTION = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    ELECTRO_OPTIC_EFFECT = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    EMISSIVITY = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    ENERGY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    ENERGY_DENSITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: -1.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    ENERGY_FLUX_DENSITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.TIME: -3.0})
    )
    ENTHALPY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    ENTROPY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0, _B.TEMPERATURE: -1.0})
    )
    FATIGUE_LIMIT = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    FLEXURAL_MODULUS = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    FLEXURAL_STRENGTH = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    FORCE = VariableDescriptor[Literal[_Q.VECTOR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    FORCE_MAGNITUDE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    FORCE_X = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    FORCE_Y = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    FORCE_Z = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    FRACTURE_TOUGHNESS = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.TIME: -2.0})
    )
    FREQUENCY = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({_B.TIME: -1.0}))
    FREQUENCY_DRIFT = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.TIME: -2.0})
    )
    FRICTION_COEFFICIENT = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    FUEL_EFFICIENCY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: -2.0})
    )
    HALF_LIFE = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({_B.TIME: 1.0}))
    HALL_COEFFICIENT = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 3.0, _B.CURRENT: -1.0, _B.TIME: -1.0})
    )
    HARDNESS = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    HEAT_CAPACITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0, _B.TEMPERATURE: -1.0})
    )
    HEAT_FLUX_DENSITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.TIME: -3.0})
    )
    HEAT_OF_VAPORIZATION = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    HYGROSCOPY = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    HYSTERESIS = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    ILLUMINANCE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LIGHT: 1.0, _B.SOLID_ANGLE: 1.0, _B.LENGTH: -2.0})
    )
    INTERNAL_ENERGY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    JERK = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -3.0})
    )
    KINEMATIC_VISCOSITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -1.0})
    )
    LENGTH = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({_B.LENGTH: 1.0}))
    LIGHT = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({_B.LIGHT: 1.0}))
    LINEAR_MASS_DENSITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0})
    )
    LUMINANCE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LIGHT: 1.0, _B.LENGTH: -2.0})
    )
    LUMINOSITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LIGHT: 1.0, _B.SOLID_ANGLE: 1.0})
    )
    LUMINOUS_EXPOSURE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LIGHT: 1.0, _B.SOLID_ANGLE: 1.0, _B.LENGTH: -2.0, _B.TIME: 1.0})
    )
    LUMINOUS_FLUX = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LIGHT: 1.0, _B.SOLID_ANGLE: 1.0})
    )
    MAGNETIC_FLUX = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0, _B.TIME: -2.0, _B.CURRENT: -1.0})
    )
    MAGNETIC_INDUCTION = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.TIME: -2.0, _B.CURRENT: -1.0})
    )
    MAGNETIC_PERMEABILITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 1.0, _B.MASS: 1.0, _B.TIME: -2.0, _B.CURRENT: -2.0})
    )
    MAGNETIC_VECTOR_POTENTIAL = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 1.0, _B.MASS: 1.0, _B.TIME: -2.0, _B.CURRENT: -1.0})
    )
    MAGNETOCALORIC_COEFFICIENT = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.TEMPERATURE: 1.0, _B.MASS: -1.0, _B.TIME: 2.0, _B.CURRENT: 1.0})
    )
    MAGNETOELECTRIC_POLARIZABILITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: -1.0, _B.TIME: -1.0})
    )
    MAGNETORESISTANCE = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    MAGNETOSTRICTION = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    MAGNETOTHERMOELECTRIC_POWER = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -1.0, _B.TEMPERATURE: -1.0})
    )
    MALLEABILITY = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    MASS = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({_B.MASS: 1.0}))
    MASS_CONTROL = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.TIME: -3.0})
    )
    MASS_DIFFUSIVITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -1.0})
    )
    MASS_FLOW_RATE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.TIME: -1.0})
    )
    MAXIMUM_ENERGY_PRODUCT = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: -1.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    MELTING_POINT = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.TEMPERATURE: 1.0})
    )
    MESH_VELOCITY = VariableDescriptor[Literal[_Q.VECTOR]](
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MESH_VELOCITY_MAGNITUDE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MESH_VELOCITY_X = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MESH_VELOCITY_Y = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MESH_VELOCITY_Z = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MOLALITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.CHEMICAL_AMOUNT: 1.0, _B.MASS: -1.0})
    )
    MOLARITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.CHEMICAL_AMOUNT: 1.0, _B.LENGTH: -3.0})
    )
    MOLAR_ENERGY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions(
            {_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0, _B.CHEMICAL_AMOUNT: -1.0}
        )
    )
    MOLAR_ENTROPY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions(
            {
                _B.LENGTH: 2.0,
                _B.MASS: 1.0,
                _B.TIME: -2.0,
                _B.TEMPERATURE: -1.0,
                _B.CHEMICAL_AMOUNT: -1.0,
            }
        )
    )
    MOLAR_HEAT_CAPACITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions(
            {
                _B.LENGTH: 2.0,
                _B.MASS: 1.0,
                _B.TIME: -2.0,
                _B.TEMPERATURE: -1.0,
                _B.CHEMICAL_AMOUNT: -1.0,
            }
        )
    )
    MOLAR_MASS = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.CHEMICAL_AMOUNT: -1.0})
    )
    MOLAR_VOLUME = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 3.0, _B.CHEMICAL_AMOUNT: -1.0})
    )
    MOMENTUM = VariableDescriptor[Literal[_Q.VECTOR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MOMENTUM_MAGNITUDE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MOMENTUM_X = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MOMENTUM_Y = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MOMENTUM_Z = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MOMENT_OF_INERTIA = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0})
    )
    NERNST_COEFFICIENT = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -1.0, _B.TEMPERATURE: -1.0})
    )
    NEUTRON_CROSS_SECTION = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0})
    )
    NORMALIZED_Q_CRITERION = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    OPTICAL_ACTIVITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 1.0, _B.MASS: -1.0})
    )
    PERMEABILITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 1.0, _B.MASS: 1.0, _B.TIME: -2.0, _B.CURRENT: -2.0})
    )
    PERMITTIVITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: -1.0, _B.LENGTH: -3.0, _B.TIME: 4.0, _B.CURRENT: 2.0})
    )
    PH = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    PHOTOELASTICITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: -1.0, _B.LENGTH: 1.0, _B.TIME: 2.0})
    )
    PHOTOSENSITIVITY = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    PIEZOELECTRIC_CONSTANTS = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -1.0, _B.CURRENT: -1.0})
    )
    PIEZOMAGNETISM = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.CURRENT: -1.0, _B.LENGTH: 1.0})
    )
    PLASTICITY = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    POISSON_RATIO = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    POSITION = VariableDescriptor[Literal[_Q.VECTOR]](Dimensions({_B.LENGTH: 1.0}))
    POSITION_MAGNITUDE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 1.0})
    )
    POSITION_X = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({_B.LENGTH: 1.0}))
    POSITION_Y = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({_B.LENGTH: 1.0}))
    POSITION_Z = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({_B.LENGTH: 1.0}))
    POWER = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -3.0})
    )
    PRANDTL_NUMBER = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    PRESSURE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    PRESSURE_COEFFICIENT = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    PRODUCTION_OF_TURBULENT_KINETIC_ENERGY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -3.0})
    )
    PYROELECTRICITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.CURRENT: 1.0, _B.LENGTH: -2.0, _B.TEMPERATURE: -1.0})
    )
    PYROMAGNETIC_COEFFICIENT = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions(
            {_B.MASS: 1.0, _B.TIME: -2.0, _B.CURRENT: -1.0, _B.TEMPERATURE: -1.0}
        )
    )
    Q_CRITERION = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({_B.TIME: -2.0}))
    RADIAL_VELOCITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    RADIANCE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.TIME: -3.0, _B.SOLID_ANGLE: -1.0})
    )
    RADIANT_EXPOSURE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.TIME: -2.0})
    )
    RADIANT_INTENSITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -3.0, _B.SOLID_ANGLE: -1.0})
    )
    REACTIVITY = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    REFLECTIVITY = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    REFRACTIVE_INDEX = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    RELATIVE_ATOMIC_MASS = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    RESILIENCE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    SCATTERING = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    SEEBECK_COEFFICIENT = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions(
            {
                _B.MASS: 1.0,
                _B.LENGTH: 2.0,
                _B.TIME: -3.0,
                _B.CURRENT: -1.0,
                _B.TEMPERATURE: -1.0,
            }
        )
    )
    SHEAR_MODULUS = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    SHEAR_STRENGTH = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    SKIN_FRICTION_COEFFICIENT = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    SLIP = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    SNAP = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -4.0})
    )
    SOLID_ANGLE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.SOLID_ANGLE: 1.0})
    )
    SOUND_REFLECTION = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    SOUND_TRANSFER = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    SPECIFIC_ACTIVITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: -1.0, _B.TIME: -1.0})
    )
    SPECIFIC_ANGULAR_MOMENTUM = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -1.0})
    )
    SPECIFIC_DISSIPATION_RATE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.TIME: -1.0})
    )
    SPECIFIC_ENERGY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    SPECIFIC_ENTHALPY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    SPECIFIC_ENTROPY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0, _B.TEMPERATURE: -1.0})
    )
    SPECIFIC_HEAT_CAPACITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0, _B.TEMPERATURE: -1.0})
    )
    SPECIFIC_INTERNAL_ENERGY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    SPECIFIC_INTERNAL_SURFACE_AREA = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: -1.0})
    )
    SPECIFIC_MODULUS = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    SPECIFIC_STRENGTH = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    SPECIFIC_TOTAL_ENERGY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    SPECIFIC_TOTAL_ENTHALPY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    SPECIFIC_VOLUME = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 3.0, _B.MASS: -1.0})
    )
    SPECIFIC_WEIGHT = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -2.0, _B.TIME: -2.0})
    )
    SPECTRAL_INTENSITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 1.0, _B.MASS: 1.0, _B.TIME: -3.0, _B.SOLID_ANGLE: -1.0})
    )
    SPECTRAL_IRRADIANCE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: -1.0, _B.MASS: 1.0, _B.TIME: -3.0})
    )
    SPECTRAL_POWER = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 1.0, _B.MASS: 1.0, _B.TIME: -3.0})
    )
    SPEED_OF_SOUND = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    SPIN_HALL_EFFECT = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0, _B.TIME: -3.0, _B.CURRENT: -2.0})
    )
    STANDARD_ATOMIC_WEIGHT = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    STATIC_PRESSURE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    STRAIN_RATE = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({_B.TIME: -1.0}))
    STRESS = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    SURFACE_ENERGY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.TIME: -2.0})
    )
    SURFACE_HEAT_FLUX = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.TIME: -3.0})
    )
    SURFACE_HEAT_TRANSFER_COEFFICIENT = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.TIME: -3.0, _B.TEMPERATURE: -1.0})
    )
    SURFACE_NUSSELT_NUMBER = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    SURFACE_ROUGHNESS = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 1.0})
    )
    SURFACE_STANTON_NUMBER = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    SURFACE_TENSION = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.TIME: -2.0})
    )
    TANGENTIAL_VELOCITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    TEMPERATURE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.TEMPERATURE: 1.0})
    )
    TEMPERATURE_DIFFERENCE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.TEMPERATURE_DIFFERENCE: 1.0})
    )
    TEMPERATURE_GRADIENT = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.TEMPERATURE: 1.0, _B.LENGTH: -1.0})
    )
    TENSILE_STRENGTH = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    THERMAL_CONDUCTIVITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 1.0, _B.MASS: 1.0, _B.TIME: -3.0, _B.TEMPERATURE: -1.0})
    )
    THERMAL_DIFFUSIVITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -1.0})
    )
    THERMAL_EXPANSION_COEFFICIENT = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.TEMPERATURE: -1.0})
    )
    THERMAL_RESISTANCE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.TEMPERATURE: 1.0, _B.LENGTH: -2.0, _B.MASS: -1.0, _B.TIME: 3.0})
    )
    THIRD_ORDER_ELASTICITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    TIME = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({_B.TIME: 1.0}))
    TORQUE = VariableDescriptor[Literal[_Q.VECTOR]](
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    TORQUE_MAGNITUDE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    TORQUE_X = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    TORQUE_Y = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    TORQUE_Z = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    TOTAL_ENERGY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    TOTAL_PRESSURE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    TOTAL_TEMPERATURE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.TEMPERATURE: 1.0})
    )
    TOUGHNESS = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: -1.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    TRANSMITTANCE = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    TURBULENT_DISSIPATION_RATE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.TIME: 3.0})
    )
    TURBULENT_INTENSITY = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    TURBULENT_KINETIC_ENERGY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    TURBULENT_REYNOLDS_NUMBER = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    TURBULENT_VISCOSITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -1.0})
    )
    TURBULENT_VISCOSITY_RATIO = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    VAPOR_PRESSURE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    VELOCITY = VariableDescriptor[Literal[_Q.VECTOR]](
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    VELOCITY_MAGNITUDE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    VELOCITY_X = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    VELOCITY_Y = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    VELOCITY_Z = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    VISCOSITY = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -1.0})
    )
    VOLUME = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({_B.LENGTH: 3.0}))
    VOLUMETRIC_FLOW = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.LENGTH: 3.0, _B.TIME: -1.0})
    )
    VOLUME_FRACTION = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    VORTICITY = VariableDescriptor[Literal[_Q.VECTOR]](Dimensions({_B.TIME: -1.0}))
    VORTICITY_MAGNITUDE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.TIME: -1.0})
    )
    VORTICITY_X = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({_B.TIME: -1.0}))
    VORTICITY_Y = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({_B.TIME: -1.0}))
    VORTICITY_Z = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({_B.TIME: -1.0}))
    WALL_ADJACENT_HEAT_TRANSFER_COEFFICIENT = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.TIME: -3.0, _B.TEMPERATURE: -1.0})
    )
    WALL_ADJACENT_TEMPERATURE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.TEMPERATURE: 1.0})
    )
    WALL_SHEAR_STRESS = VariableDescriptor[Literal[_Q.VECTOR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    WALL_SHEAR_STRESS_MAGNITUDE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    WALL_SHEAR_STRESS_X = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    WALL_SHEAR_STRESS_Y = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    WALL_SHEAR_STRESS_Z = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    WALL_TEMPERATURE = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.TEMPERATURE: 1.0})
    )
    WALL_TEMPERATURE_THIN = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.TEMPERATURE: 1.0})
    )
    WALL_Y_PLUS = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    WALL_Y_STAR = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({}))
    WAVENUMBER = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions({_B.LENGTH: -1.0}))
    YANK = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -3.0})
    )
    YIELD_STRENGTH = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    YOUNG_MODULUS = VariableDescriptor[Literal[_Q.SCALAR]](
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )

    @final
    class fluent:
        """Dictionary of variable descriptors for fluent-related quantities."""

        HELICITY = VariableDescriptor[Literal[_Q.SCALAR]](_D.ACCELERATION)
        LAMBDA_2_CRITERION = VariableDescriptor[Literal[_Q.SCALAR]](_D.TIME**-2)
        DENSITY_ALL = VariableDescriptor[Literal[_Q.SCALAR]](_D.DENSITY)
        Y_PLUS_BASED_HEAT_TRANSFER_COEFFICIENT = VariableDescriptor[Literal[_Q.SCALAR]](
            _D.POWER * _D.LENGTH**-2 * _D.TEMPERATURE**-1
        )
        TOTAL_ENTHALPY_DEVIATION = VariableDescriptor[Literal[_Q.SCALAR]](
            _D.SPECIFIC_ENTHALPY
        )
        MASS_IMBALANCE = VariableDescriptor[Literal[_Q.SCALAR]](_D.MASS * _D.TIME**-1)
        PRESSURE_HESSIAN_INDICATOR = VariableDescriptor[Literal[_Q.SCALAR]](
            Dimensions()
        )
        VELOCITY_ANGLE = VariableDescriptor[Literal[_Q.SCALAR]](_D.ANGLE)
        DVELOCITY_DX = VariableDescriptor[Literal[_Q.SCALAR]](_D.TIME**-1)
        DVELOCITY_DX_MAGNITUDE = VariableDescriptor[Literal[_Q.SCALAR]](_D.TIME**-1)
        DVELOCITY_DX_X = VariableDescriptor[Literal[_Q.SCALAR]](_D.TIME**-1)
        DVELOCITY_DX_Y = VariableDescriptor[Literal[_Q.SCALAR]](_D.TIME**-1)
        DVELOCITY_DX_Z = VariableDescriptor[Literal[_Q.SCALAR]](_D.TIME**-1)
        DVELOCITY_DY = VariableDescriptor[Literal[_Q.SCALAR]](_D.TIME**-1)
        DVELOCITY_DY_MAGNITUDE = VariableDescriptor[Literal[_Q.SCALAR]](_D.TIME**-1)
        DVELOCITY_DY_X = VariableDescriptor[Literal[_Q.SCALAR]](_D.TIME**-1)
        DVELOCITY_DY_Y = VariableDescriptor[Literal[_Q.SCALAR]](_D.TIME**-1)
        DVELOCITY_DY_Z = VariableDescriptor[Literal[_Q.SCALAR]](_D.TIME**-1)
        DVELOCITY_DZ = VariableDescriptor[Literal[_Q.SCALAR]](_D.TIME**-1)
        DVELOCITY_DZ_MAGNITUDE = VariableDescriptor[Literal[_Q.SCALAR]](_D.TIME**-1)
        DVELOCITY_DZ_X = VariableDescriptor[Literal[_Q.SCALAR]](_D.TIME**-1)
        DVELOCITY_DZ_Y = VariableDescriptor[Literal[_Q.SCALAR]](_D.TIME**-1)
        DVELOCITY_DZ_Z = VariableDescriptor[Literal[_Q.SCALAR]](_D.TIME**-1)
        VOLUME_FRACTION_PRIMARY_PHASE = VariableDescriptor[Literal[_Q.SCALAR]](
            _D.VOLUME_FRACTION
        )
        VOLUME_FRACTION_SECONDARY_PHASE = VariableDescriptor[Literal[_Q.SCALAR]](
            _D.VOLUME_FRACTION
        )

    @final
    class mesh:
        """Dictionary of variable descriptors for mesh-related quantities."""

        ANISOTROPIC_ADAPTION_CELLS = VariableDescriptor[Literal[_Q.SCALAR]](
            Dimensions()
        )
        BOUNDARY_CELL_DISTANCE = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions())
        BOUNDARY_LAYER_CELLS = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions())
        BOUNDARY_NORMAL_DISTANCE = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions())
        BOUNDARY_VOLUME_DISTANCE = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions())
        CELL_EQUIANGLE_SKEW = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions())
        CELL_EQUIVOLUME_SKEW = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions())
        CELL_PARENT_INDEX = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions())
        CELL_REFINE_LEVEL = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions())
        CELL_VOLUME = VariableDescriptor[Literal[_Q.SCALAR]](_D.VOLUME)
        CELL_VOLUME_CHANGE = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions())
        ELEMENT_ASPECT_RATIO = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions())
        ELEMENT_WALL_DISTANCE = VariableDescriptor[Literal[_Q.SCALAR]](_D.LENGTH)
        FACE_AREA_MAGNITUDE = VariableDescriptor[Literal[_Q.SCALAR]](_D.AREA)
        FACE_HANDEDNESS = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions())
        INTERFACE_OVERLAP_FRACTION = VariableDescriptor[Literal[_Q.SCALAR]](
            Dimensions()
        )
        MARK_POOR_ELEMENTS = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions())
        SMOOTHED_CELL_REFINE_LEVEL = VariableDescriptor[Literal[_Q.SCALAR]](
            Dimensions()
        )
        X_FACE_AREA = VariableDescriptor[Literal[_Q.SCALAR]](_D.AREA)
        Y_FACE_AREA = VariableDescriptor[Literal[_Q.SCALAR]](_D.AREA)
        Z_FACE_AREA = VariableDescriptor[Literal[_Q.SCALAR]](_D.AREA)
        ACTIVE_CELL_PARTITION = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions())
        CELL_ELEMENT_TYPE = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions())
        CELL_ID = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions())
        CELL_WEIGHT = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions())
        CELL_ZONE_INDEX = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions())
        CELL_ZONE_TYPE = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions())
        PARTITION_NEIGHBOURS = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions())
        STORED_CELL_PARTITION = VariableDescriptor[Literal[_Q.SCALAR]](Dimensions())

    # endregion


# Add custom descriptors
VariableCatalog.add("STORED_CELL_PARTITIION", Dimensions(), "mesh")  # deprecated typo
