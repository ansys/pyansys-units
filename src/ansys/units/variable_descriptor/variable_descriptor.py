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

import inspect
from dataclasses import dataclass
from typing import final

from ansys.units import BaseDimensions
from ansys.units.dimensions import Dimensions
from ansys.units.quantity_dimensions import QuantityDimensions


@dataclass(frozen=True)
class VariableDescriptor:
    """Defines a physical quantity variable descriptor."""

    name: str
    dimension: Dimensions

    def __hash__(self) -> int:
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


_D = QuantityDimensions
_B = BaseDimensions


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
        setattr(target, variable, VariableDescriptor(transformed_name, dimension))

    # region autogenerated variables
    ABSOLUTE_PRESSURE = VariableDescriptor(
        "absolute_pressure", Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    ABSORBANCE = VariableDescriptor("absorbance", Dimensions({}))
    ABSORBED_DOSE_RATE = VariableDescriptor(
        "absorbed_dose_rate", Dimensions({_B.LENGTH: 2.0, _B.TIME: -3.0})
    )
    ACCELERATION = VariableDescriptor(
        "acceleration", Dimensions({_B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    ACCELERATION_MAGNITUDE = VariableDescriptor(
        "acceleration_magnitude", Dimensions({_B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    ACCELERATION_X = VariableDescriptor(
        "acceleration_x", Dimensions({_B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    ACCELERATION_Y = VariableDescriptor(
        "acceleration_y", Dimensions({_B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    ACCELERATION_Z = VariableDescriptor(
        "acceleration_z", Dimensions({_B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    ACOUSTICAL_ABSORPTION = VariableDescriptor("acoustical_absorption", Dimensions({}))
    ACTION = VariableDescriptor(
        "action", Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -1.0})
    )
    ANGLE = VariableDescriptor("angle", Dimensions({_B.ANGLE: 1.0}))
    ANGULAR_ACCELERATION = VariableDescriptor(
        "angular_acceleration", Dimensions({_B.TIME: -2.0})
    )
    ANGULAR_MOMENTUM = VariableDescriptor(
        "angular_momentum", Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -1.0})
    )
    ANGULAR_MOMENTUM_MAGNITUDE = VariableDescriptor(
        "angular_momentum_magnitude",
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -1.0}),
    )
    ANGULAR_MOMENTUM_X = VariableDescriptor(
        "angular_momentum_x", Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -1.0})
    )
    ANGULAR_MOMENTUM_Y = VariableDescriptor(
        "angular_momentum_y", Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -1.0})
    )
    ANGULAR_MOMENTUM_Z = VariableDescriptor(
        "angular_momentum_z", Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -1.0})
    )
    ANGULAR_VELOCITY = VariableDescriptor(
        "angular_velocity", Dimensions({_B.TIME: -1.0})
    )
    AREA = VariableDescriptor("area", Dimensions({_B.LENGTH: 2.0}))
    AREA_DENSITY = VariableDescriptor(
        "area_density", Dimensions({_B.MASS: 1.0, _B.LENGTH: -2.0})
    )
    ATOMIC_MASS = VariableDescriptor("atomic_mass", Dimensions({_B.MASS: 1.0}))
    ATOMIC_NUMBER = VariableDescriptor("atomic_number", Dimensions({}))
    ATTENUATION_COEFFICIENT = VariableDescriptor(
        "attenuation_coefficient", Dimensions({_B.LENGTH: -1.0})
    )
    AXIAL_VELOCITY = VariableDescriptor(
        "axial_velocity", Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    BIREFRINGENCE = VariableDescriptor("birefringence", Dimensions({}))
    BULK_MODULUS = VariableDescriptor(
        "bulk_modulus", Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    CAPACITANCE = VariableDescriptor(
        "capacitance",
        Dimensions({_B.MASS: -1.0, _B.LENGTH: -2.0, _B.TIME: 4.0, _B.CURRENT: 2.0}),
    )
    CATALYTIC_EFFICIENCY = VariableDescriptor(
        "catalytic_efficiency",
        Dimensions({_B.LENGTH: 3.0, _B.CHEMICAL_AMOUNT: -1.0, _B.TIME: -1.0}),
    )
    CELL_REYNOLDS_NUMBER = VariableDescriptor("cell_reynolds_number", Dimensions({}))
    CHEMICAL_AMOUNT = VariableDescriptor(
        "chemical_amount", Dimensions({_B.CHEMICAL_AMOUNT: 1.0})
    )
    COEFFICIENT_OF_RESTITUTION = VariableDescriptor(
        "coefficient_of_restitution", Dimensions({})
    )
    COLOR = VariableDescriptor("color", Dimensions({}))
    COMPRESSIBILITY = VariableDescriptor(
        "compressibility", Dimensions({_B.MASS: -1.0, _B.LENGTH: 1.0, _B.TIME: 2.0})
    )
    COMPRESSIVE_STRENGTH = VariableDescriptor(
        "compressive_strength",
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0}),
    )
    CONVECTIVE_COURANT_NUMBER = VariableDescriptor(
        "convective_courant_number", Dimensions({})
    )
    CORROSION_RESISTANCE = VariableDescriptor("corrosion_resistance", Dimensions({}))
    CREEP = VariableDescriptor("creep", Dimensions({_B.TIME: -1.0}))
    CURIE_TEMPERATURE = VariableDescriptor(
        "curie_temperature", Dimensions({_B.TEMPERATURE: 1.0})
    )
    CURRENT = VariableDescriptor("current", Dimensions({_B.CURRENT: 1.0}))
    DENSITY = VariableDescriptor("density", Dimensions({_B.MASS: 1.0, _B.LENGTH: -3.0}))
    DIAMAGNETISM = VariableDescriptor("diamagnetism", Dimensions({}))
    DIELECTRIC_CONSTANT = VariableDescriptor("dielectric_constant", Dimensions({}))
    DIELECTRIC_STRENGTH = VariableDescriptor(
        "dielectric_strength",
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -3.0, _B.CURRENT: -1.0}),
    )
    DUCTILITY = VariableDescriptor("ductility", Dimensions({}))
    DURABILITY = VariableDescriptor("durability", Dimensions({}))
    DYNAMIC_PRESSURE = VariableDescriptor(
        "dynamic_pressure", Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    DYNAMIC_VISCOSITY = VariableDescriptor(
        "dynamic_viscosity", Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -1.0})
    )
    EFFECTIVE_PRANDTL_NUMBER = VariableDescriptor(
        "effective_prandtl_number", Dimensions({})
    )
    EFFECTIVE_THERMAL_CONDUCTIVITY = VariableDescriptor(
        "effective_thermal_conductivity",
        Dimensions({_B.LENGTH: 1.0, _B.MASS: 1.0, _B.TIME: -3.0, _B.TEMPERATURE: -1.0}),
    )
    EFFECTIVE_VISCOSITY = VariableDescriptor(
        "effective_viscosity",
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -1.0}),
    )
    ELASTICITY = VariableDescriptor("elasticity", Dimensions({}))
    ELECTRICAL_CAPACITANCE = VariableDescriptor(
        "electrical_capacitance",
        Dimensions({_B.MASS: -1.0, _B.LENGTH: -2.0, _B.TIME: 4.0, _B.CURRENT: 2.0}),
    )
    ELECTRICAL_CONDUCTANCE = VariableDescriptor(
        "electrical_conductance",
        Dimensions({_B.MASS: -1.0, _B.LENGTH: -2.0, _B.TIME: 3.0, _B.CURRENT: 2.0}),
    )
    ELECTRICAL_CONDUCTIVITY = VariableDescriptor(
        "electrical_conductivity",
        Dimensions({_B.MASS: -1.0, _B.LENGTH: -3.0, _B.TIME: 3.0, _B.CURRENT: 2.0}),
    )
    ELECTRICAL_IMPEDANCE = VariableDescriptor(
        "electrical_impedance",
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0, _B.TIME: -3.0, _B.CURRENT: -2.0}),
    )
    ELECTRICAL_INDUCTANCE = VariableDescriptor(
        "electrical_inductance",
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0, _B.TIME: -2.0, _B.CURRENT: -2.0}),
    )
    ELECTRICAL_POTENTIAL = VariableDescriptor(
        "electrical_potential",
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0, _B.TIME: -3.0, _B.CURRENT: -1.0}),
    )
    ELECTRICAL_REACTANCE = VariableDescriptor(
        "electrical_reactance",
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0, _B.TIME: -3.0, _B.CURRENT: -2.0}),
    )
    ELECTRICAL_RESISTANCE = VariableDescriptor(
        "electrical_resistance",
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0, _B.TIME: -3.0, _B.CURRENT: -2.0}),
    )
    ELECTRICAL_RESISTIVITY = VariableDescriptor(
        "electrical_resistivity",
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 3.0, _B.TIME: -3.0, _B.CURRENT: -2.0}),
    )
    ELECTRIC_CHARGE = VariableDescriptor(
        "electric_charge", Dimensions({_B.TIME: 1.0, _B.CURRENT: 1.0})
    )
    ELECTRIC_SUSCEPTIBILITY = VariableDescriptor(
        "electric_susceptibility", Dimensions({})
    )
    ELECTROCALORIC_COEFFICIENT = VariableDescriptor(
        "electrocaloric_coefficient",
        Dimensions(
            {
                _B.TEMPERATURE: 1.0,
                _B.MASS: -1.0,
                _B.LENGTH: -2.0,
                _B.TIME: 3.0,
                _B.CURRENT: 1.0,
            }
        ),
    )
    ELECTROSTRICTION = VariableDescriptor("electrostriction", Dimensions({}))
    ELECTRO_OPTIC_EFFECT = VariableDescriptor("electro_optic_effect", Dimensions({}))
    EMISSIVITY = VariableDescriptor("emissivity", Dimensions({}))
    ENERGY = VariableDescriptor(
        "energy", Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    ENERGY_DENSITY = VariableDescriptor(
        "energy_density", Dimensions({_B.LENGTH: -1.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    ENERGY_FLUX_DENSITY = VariableDescriptor(
        "energy_flux_density", Dimensions({_B.MASS: 1.0, _B.TIME: -3.0})
    )
    ENTHALPY = VariableDescriptor(
        "enthalpy", Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    ENTROPY = VariableDescriptor(
        "entropy",
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0, _B.TEMPERATURE: -1.0}),
    )
    FATIGUE_LIMIT = VariableDescriptor(
        "fatigue_limit", Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    FLEXURAL_MODULUS = VariableDescriptor(
        "flexural_modulus", Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    FLEXURAL_STRENGTH = VariableDescriptor(
        "flexural_strength", Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    FORCE = VariableDescriptor(
        "force", Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    FORCE_MAGNITUDE = VariableDescriptor(
        "force_magnitude", Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    FORCE_X = VariableDescriptor(
        "force_x", Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    FORCE_Y = VariableDescriptor(
        "force_y", Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    FORCE_Z = VariableDescriptor(
        "force_z", Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    FRACTURE_TOUGHNESS = VariableDescriptor(
        "fracture_toughness", Dimensions({_B.MASS: 1.0, _B.TIME: -2.0})
    )
    FREQUENCY = VariableDescriptor("frequency", Dimensions({_B.TIME: -1.0}))
    FREQUENCY_DRIFT = VariableDescriptor("frequency_drift", Dimensions({_B.TIME: -2.0}))
    FRICTION_COEFFICIENT = VariableDescriptor("friction_coefficient", Dimensions({}))
    FUEL_EFFICIENCY = VariableDescriptor(
        "fuel_efficiency", Dimensions({_B.LENGTH: -2.0})
    )
    HALF_LIFE = VariableDescriptor("half_life", Dimensions({_B.TIME: 1.0}))
    HALL_COEFFICIENT = VariableDescriptor(
        "hall_coefficient",
        Dimensions({_B.LENGTH: 3.0, _B.CURRENT: -1.0, _B.TIME: -1.0}),
    )
    HARDNESS = VariableDescriptor(
        "hardness", Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    HEAT_CAPACITY = VariableDescriptor(
        "heat_capacity",
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0, _B.TEMPERATURE: -1.0}),
    )
    HEAT_FLUX_DENSITY = VariableDescriptor(
        "heat_flux_density", Dimensions({_B.MASS: 1.0, _B.TIME: -3.0})
    )
    HEAT_OF_VAPORIZATION = VariableDescriptor(
        "heat_of_vaporization", Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    HYGROSCOPY = VariableDescriptor("hygroscopy", Dimensions({}))
    HYSTERESIS = VariableDescriptor("hysteresis", Dimensions({}))
    ILLUMINANCE = VariableDescriptor(
        "illuminance", Dimensions({_B.LIGHT: 1.0, _B.SOLID_ANGLE: 1.0, _B.LENGTH: -2.0})
    )
    INTERNAL_ENERGY = VariableDescriptor(
        "internal_energy", Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    JERK = VariableDescriptor("jerk", Dimensions({_B.LENGTH: 1.0, _B.TIME: -3.0}))
    KINEMATIC_VISCOSITY = VariableDescriptor(
        "kinematic_viscosity", Dimensions({_B.LENGTH: 2.0, _B.TIME: -1.0})
    )
    LENGTH = VariableDescriptor("length", Dimensions({_B.LENGTH: 1.0}))
    LIGHT = VariableDescriptor("light", Dimensions({_B.LIGHT: 1.0}))
    LINEAR_MASS_DENSITY = VariableDescriptor(
        "linear_mass_density", Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0})
    )
    LUMINANCE = VariableDescriptor(
        "luminance", Dimensions({_B.LIGHT: 1.0, _B.LENGTH: -2.0})
    )
    LUMINOSITY = VariableDescriptor(
        "luminosity", Dimensions({_B.LIGHT: 1.0, _B.SOLID_ANGLE: 1.0})
    )
    LUMINOUS_EXPOSURE = VariableDescriptor(
        "luminous_exposure",
        Dimensions({_B.LIGHT: 1.0, _B.SOLID_ANGLE: 1.0, _B.LENGTH: -2.0, _B.TIME: 1.0}),
    )
    LUMINOUS_FLUX = VariableDescriptor(
        "luminous_flux", Dimensions({_B.LIGHT: 1.0, _B.SOLID_ANGLE: 1.0})
    )
    MAGNETIC_FLUX = VariableDescriptor(
        "magnetic_flux",
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0, _B.TIME: -2.0, _B.CURRENT: -1.0}),
    )
    MAGNETIC_INDUCTION = VariableDescriptor(
        "magnetic_induction",
        Dimensions({_B.MASS: 1.0, _B.TIME: -2.0, _B.CURRENT: -1.0}),
    )
    MAGNETIC_PERMEABILITY = VariableDescriptor(
        "magnetic_permeability",
        Dimensions({_B.LENGTH: 1.0, _B.MASS: 1.0, _B.TIME: -2.0, _B.CURRENT: -2.0}),
    )
    MAGNETIC_VECTOR_POTENTIAL = VariableDescriptor(
        "magnetic_vector_potential",
        Dimensions({_B.LENGTH: 1.0, _B.MASS: 1.0, _B.TIME: -2.0, _B.CURRENT: -1.0}),
    )
    MAGNETOCALORIC_COEFFICIENT = VariableDescriptor(
        "magnetocaloric_coefficient",
        Dimensions({_B.TEMPERATURE: 1.0, _B.MASS: -1.0, _B.TIME: 2.0, _B.CURRENT: 1.0}),
    )
    MAGNETOELECTRIC_POLARIZABILITY = VariableDescriptor(
        "magnetoelectric_polarizability", Dimensions({_B.LENGTH: -1.0, _B.TIME: -1.0})
    )
    MAGNETORESISTANCE = VariableDescriptor("magnetoresistance", Dimensions({}))
    MAGNETOSTRICTION = VariableDescriptor("magnetostriction", Dimensions({}))
    MAGNETOTHERMOELECTRIC_POWER = VariableDescriptor(
        "magnetothermoelectric_power",
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -1.0, _B.TEMPERATURE: -1.0}),
    )
    MALLEABILITY = VariableDescriptor("malleability", Dimensions({}))
    MASS = VariableDescriptor("mass", Dimensions({_B.MASS: 1.0}))
    MASS_CONTROL = VariableDescriptor(
        "mass_control", Dimensions({_B.MASS: 1.0, _B.TIME: -3.0})
    )
    MASS_DIFFUSIVITY = VariableDescriptor(
        "mass_diffusivity", Dimensions({_B.LENGTH: 2.0, _B.TIME: -1.0})
    )
    MASS_FLOW_RATE = VariableDescriptor(
        "mass_flow_rate", Dimensions({_B.MASS: 1.0, _B.TIME: -1.0})
    )
    MAXIMUM_ENERGY_PRODUCT = VariableDescriptor(
        "maximum_energy_product",
        Dimensions({_B.LENGTH: -1.0, _B.MASS: 1.0, _B.TIME: -2.0}),
    )
    MELTING_POINT = VariableDescriptor(
        "melting_point", Dimensions({_B.TEMPERATURE: 1.0})
    )
    MESH_VELOCITY = VariableDescriptor(
        "mesh_velocity", Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MESH_VELOCITY_MAGNITUDE = VariableDescriptor(
        "mesh_velocity_magnitude", Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MESH_VELOCITY_X = VariableDescriptor(
        "mesh_velocity_x", Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MESH_VELOCITY_Y = VariableDescriptor(
        "mesh_velocity_y", Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MESH_VELOCITY_Z = VariableDescriptor(
        "mesh_velocity_z", Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MOLALITY = VariableDescriptor(
        "molality", Dimensions({_B.CHEMICAL_AMOUNT: 1.0, _B.MASS: -1.0})
    )
    MOLARITY = VariableDescriptor(
        "molarity", Dimensions({_B.CHEMICAL_AMOUNT: 1.0, _B.LENGTH: -3.0})
    )
    MOLAR_ENERGY = VariableDescriptor(
        "molar_energy",
        Dimensions(
            {_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0, _B.CHEMICAL_AMOUNT: -1.0}
        ),
    )
    MOLAR_ENTROPY = VariableDescriptor(
        "molar_entropy",
        Dimensions(
            {
                _B.LENGTH: 2.0,
                _B.MASS: 1.0,
                _B.TIME: -2.0,
                _B.TEMPERATURE: -1.0,
                _B.CHEMICAL_AMOUNT: -1.0,
            }
        ),
    )
    MOLAR_HEAT_CAPACITY = VariableDescriptor(
        "molar_heat_capacity",
        Dimensions(
            {
                _B.LENGTH: 2.0,
                _B.MASS: 1.0,
                _B.TIME: -2.0,
                _B.TEMPERATURE: -1.0,
                _B.CHEMICAL_AMOUNT: -1.0,
            }
        ),
    )
    MOLAR_MASS = VariableDescriptor(
        "molar_mass", Dimensions({_B.MASS: 1.0, _B.CHEMICAL_AMOUNT: -1.0})
    )
    MOLAR_VOLUME = VariableDescriptor(
        "molar_volume", Dimensions({_B.LENGTH: 3.0, _B.CHEMICAL_AMOUNT: -1.0})
    )
    MOMENTUM = VariableDescriptor(
        "momentum", Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MOMENTUM_MAGNITUDE = VariableDescriptor(
        "momentum_magnitude", Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MOMENTUM_X = VariableDescriptor(
        "momentum_x", Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MOMENTUM_Y = VariableDescriptor(
        "momentum_y", Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MOMENTUM_Z = VariableDescriptor(
        "momentum_z", Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MOMENT_OF_INERTIA = VariableDescriptor(
        "moment_of_inertia", Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0})
    )
    NERNST_COEFFICIENT = VariableDescriptor(
        "nernst_coefficient",
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -1.0, _B.TEMPERATURE: -1.0}),
    )
    NEUTRON_CROSS_SECTION = VariableDescriptor(
        "neutron_cross_section", Dimensions({_B.LENGTH: 2.0})
    )
    NORMALIZED_Q_CRITERION = VariableDescriptor(
        "normalized_q_criterion", Dimensions({})
    )
    OPTICAL_ACTIVITY = VariableDescriptor(
        "optical_activity", Dimensions({_B.LENGTH: 1.0, _B.MASS: -1.0})
    )
    PERMEABILITY = VariableDescriptor(
        "permeability",
        Dimensions({_B.LENGTH: 1.0, _B.MASS: 1.0, _B.TIME: -2.0, _B.CURRENT: -2.0}),
    )
    PERMITTIVITY = VariableDescriptor(
        "permittivity",
        Dimensions({_B.MASS: -1.0, _B.LENGTH: -3.0, _B.TIME: 4.0, _B.CURRENT: 2.0}),
    )
    PH = VariableDescriptor("ph", Dimensions({}))
    PHOTOELASTICITY = VariableDescriptor(
        "photoelasticity", Dimensions({_B.MASS: -1.0, _B.LENGTH: 1.0, _B.TIME: 2.0})
    )
    PHOTOSENSITIVITY = VariableDescriptor("photosensitivity", Dimensions({}))
    PIEZOELECTRIC_CONSTANTS = VariableDescriptor(
        "piezoelectric_constants",
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -1.0, _B.CURRENT: -1.0}),
    )
    PIEZOMAGNETISM = VariableDescriptor(
        "piezomagnetism", Dimensions({_B.CURRENT: -1.0, _B.LENGTH: 1.0})
    )
    PLASTICITY = VariableDescriptor("plasticity", Dimensions({}))
    POISSON_RATIO = VariableDescriptor("poisson_ratio", Dimensions({}))
    POSITION = VariableDescriptor("position", Dimensions({_B.LENGTH: 1.0}))
    POSITION_MAGNITUDE = VariableDescriptor(
        "position_magnitude", Dimensions({_B.LENGTH: 1.0})
    )
    POSITION_X = VariableDescriptor("position_x", Dimensions({_B.LENGTH: 1.0}))
    POSITION_Y = VariableDescriptor("position_y", Dimensions({_B.LENGTH: 1.0}))
    POSITION_Z = VariableDescriptor("position_z", Dimensions({_B.LENGTH: 1.0}))
    POWER = VariableDescriptor(
        "power", Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -3.0})
    )
    PRANDTL_NUMBER = VariableDescriptor("prandtl_number", Dimensions({}))
    PRESSURE = VariableDescriptor(
        "pressure", Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    PRESSURE_COEFFICIENT = VariableDescriptor("pressure_coefficient", Dimensions({}))
    PRODUCTION_OF_TURBULENT_KINETIC_ENERGY = VariableDescriptor(
        "production_of_turbulent_kinetic_energy",
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -3.0}),
    )
    PYROELECTRICITY = VariableDescriptor(
        "pyroelectricity",
        Dimensions({_B.CURRENT: 1.0, _B.LENGTH: -2.0, _B.TEMPERATURE: -1.0}),
    )
    PYROMAGNETIC_COEFFICIENT = VariableDescriptor(
        "pyromagnetic_coefficient",
        Dimensions(
            {_B.MASS: 1.0, _B.TIME: -2.0, _B.CURRENT: -1.0, _B.TEMPERATURE: -1.0}
        ),
    )
    Q_CRITERION = VariableDescriptor("q_criterion", Dimensions({_B.TIME: -2.0}))
    RADIAL_VELOCITY = VariableDescriptor(
        "radial_velocity", Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    RADIANCE = VariableDescriptor(
        "radiance", Dimensions({_B.MASS: 1.0, _B.TIME: -3.0, _B.SOLID_ANGLE: -1.0})
    )
    RADIANT_EXPOSURE = VariableDescriptor(
        "radiant_exposure", Dimensions({_B.MASS: 1.0, _B.TIME: -2.0})
    )
    RADIANT_INTENSITY = VariableDescriptor(
        "radiant_intensity",
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -3.0, _B.SOLID_ANGLE: -1.0}),
    )
    REACTIVITY = VariableDescriptor("reactivity", Dimensions({}))
    REFLECTIVITY = VariableDescriptor("reflectivity", Dimensions({}))
    REFRACTIVE_INDEX = VariableDescriptor("refractive_index", Dimensions({}))
    RELATIVE_ATOMIC_MASS = VariableDescriptor("relative_atomic_mass", Dimensions({}))
    RESILIENCE = VariableDescriptor(
        "resilience", Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    SCATTERING = VariableDescriptor("scattering", Dimensions({}))
    SEEBECK_COEFFICIENT = VariableDescriptor(
        "seebeck_coefficient",
        Dimensions(
            {
                _B.MASS: 1.0,
                _B.LENGTH: 2.0,
                _B.TIME: -3.0,
                _B.CURRENT: -1.0,
                _B.TEMPERATURE: -1.0,
            }
        ),
    )
    SHEAR_MODULUS = VariableDescriptor(
        "shear_modulus", Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    SHEAR_STRENGTH = VariableDescriptor(
        "shear_strength", Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    SKIN_FRICTION_COEFFICIENT = VariableDescriptor(
        "skin_friction_coefficient", Dimensions({})
    )
    SLIP = VariableDescriptor("slip", Dimensions({}))
    SNAP = VariableDescriptor("snap", Dimensions({_B.LENGTH: 1.0, _B.TIME: -4.0}))
    SOLID_ANGLE = VariableDescriptor("solid_angle", Dimensions({_B.SOLID_ANGLE: 1.0}))
    SOUND_REFLECTION = VariableDescriptor("sound_reflection", Dimensions({}))
    SOUND_TRANSFER = VariableDescriptor("sound_transfer", Dimensions({}))
    SPECIFIC_ACTIVITY = VariableDescriptor(
        "specific_activity", Dimensions({_B.MASS: -1.0, _B.TIME: -1.0})
    )
    SPECIFIC_ANGULAR_MOMENTUM = VariableDescriptor(
        "specific_angular_momentum", Dimensions({_B.LENGTH: 2.0, _B.TIME: -1.0})
    )
    SPECIFIC_DISSIPATION_RATE = VariableDescriptor(
        "specific_dissipation_rate", Dimensions({_B.TIME: -1.0})
    )
    SPECIFIC_ENERGY = VariableDescriptor(
        "specific_energy", Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    SPECIFIC_ENTHALPY = VariableDescriptor(
        "specific_enthalpy", Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    SPECIFIC_ENTROPY = VariableDescriptor(
        "specific_entropy",
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0, _B.TEMPERATURE: -1.0}),
    )
    SPECIFIC_HEAT_CAPACITY = VariableDescriptor(
        "specific_heat_capacity",
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0, _B.TEMPERATURE: -1.0}),
    )
    SPECIFIC_INTERNAL_ENERGY = VariableDescriptor(
        "specific_internal_energy", Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    SPECIFIC_INTERNAL_SURFACE_AREA = VariableDescriptor(
        "specific_internal_surface_area", Dimensions({_B.LENGTH: -1.0})
    )
    SPECIFIC_MODULUS = VariableDescriptor(
        "specific_modulus", Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    SPECIFIC_STRENGTH = VariableDescriptor(
        "specific_strength", Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    SPECIFIC_TOTAL_ENERGY = VariableDescriptor(
        "specific_total_energy", Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    SPECIFIC_TOTAL_ENTHALPY = VariableDescriptor(
        "specific_total_enthalpy", Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    SPECIFIC_VOLUME = VariableDescriptor(
        "specific_volume", Dimensions({_B.LENGTH: 3.0, _B.MASS: -1.0})
    )
    SPECIFIC_WEIGHT = VariableDescriptor(
        "specific_weight", Dimensions({_B.MASS: 1.0, _B.LENGTH: -2.0, _B.TIME: -2.0})
    )
    SPECTRAL_INTENSITY = VariableDescriptor(
        "spectral_intensity",
        Dimensions({_B.LENGTH: 1.0, _B.MASS: 1.0, _B.TIME: -3.0, _B.SOLID_ANGLE: -1.0}),
    )
    SPECTRAL_IRRADIANCE = VariableDescriptor(
        "spectral_irradiance",
        Dimensions({_B.LENGTH: -1.0, _B.MASS: 1.0, _B.TIME: -3.0}),
    )
    SPECTRAL_POWER = VariableDescriptor(
        "spectral_power", Dimensions({_B.LENGTH: 1.0, _B.MASS: 1.0, _B.TIME: -3.0})
    )
    SPEED_OF_SOUND = VariableDescriptor(
        "speed_of_sound", Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    SPIN_HALL_EFFECT = VariableDescriptor(
        "spin_hall_effect",
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0, _B.TIME: -3.0, _B.CURRENT: -2.0}),
    )
    STANDARD_ATOMIC_WEIGHT = VariableDescriptor(
        "standard_atomic_weight", Dimensions({})
    )
    STATIC_PRESSURE = VariableDescriptor(
        "static_pressure", Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    STRAIN_RATE = VariableDescriptor("strain_rate", Dimensions({_B.TIME: -1.0}))
    STRESS = VariableDescriptor(
        "stress", Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    SURFACE_ENERGY = VariableDescriptor(
        "surface_energy", Dimensions({_B.MASS: 1.0, _B.TIME: -2.0})
    )
    SURFACE_HEAT_FLUX = VariableDescriptor(
        "surface_heat_flux", Dimensions({_B.MASS: 1.0, _B.TIME: -3.0})
    )
    SURFACE_HEAT_TRANSFER_COEFFICIENT = VariableDescriptor(
        "surface_heat_transfer_coefficient",
        Dimensions({_B.MASS: 1.0, _B.TIME: -3.0, _B.TEMPERATURE: -1.0}),
    )
    SURFACE_NUSSELT_NUMBER = VariableDescriptor(
        "surface_nusselt_number", Dimensions({})
    )
    SURFACE_ROUGHNESS = VariableDescriptor(
        "surface_roughness", Dimensions({_B.LENGTH: 1.0})
    )
    SURFACE_STANTON_NUMBER = VariableDescriptor(
        "surface_stanton_number", Dimensions({})
    )
    SURFACE_TENSION = VariableDescriptor(
        "surface_tension", Dimensions({_B.MASS: 1.0, _B.TIME: -2.0})
    )
    TANGENTIAL_VELOCITY = VariableDescriptor(
        "tangential_velocity", Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    TEMPERATURE = VariableDescriptor("temperature", Dimensions({_B.TEMPERATURE: 1.0}))
    TEMPERATURE_DIFFERENCE = VariableDescriptor(
        "temperature_difference", Dimensions({_B.TEMPERATURE_DIFFERENCE: 1.0})
    )
    TEMPERATURE_GRADIENT = VariableDescriptor(
        "temperature_gradient", Dimensions({_B.TEMPERATURE: 1.0, _B.LENGTH: -1.0})
    )
    TENSILE_STRENGTH = VariableDescriptor(
        "tensile_strength", Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    THERMAL_CONDUCTIVITY = VariableDescriptor(
        "thermal_conductivity",
        Dimensions({_B.LENGTH: 1.0, _B.MASS: 1.0, _B.TIME: -3.0, _B.TEMPERATURE: -1.0}),
    )
    THERMAL_DIFFUSIVITY = VariableDescriptor(
        "thermal_diffusivity", Dimensions({_B.LENGTH: 2.0, _B.TIME: -1.0})
    )
    THERMAL_EXPANSION_COEFFICIENT = VariableDescriptor(
        "thermal_expansion_coefficient", Dimensions({_B.TEMPERATURE: -1.0})
    )
    THERMAL_RESISTANCE = VariableDescriptor(
        "thermal_resistance",
        Dimensions({_B.TEMPERATURE: 1.0, _B.LENGTH: -2.0, _B.MASS: -1.0, _B.TIME: 3.0}),
    )
    THIRD_ORDER_ELASTICITY = VariableDescriptor(
        "third_order_elasticity",
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0}),
    )
    TIME = VariableDescriptor("time", Dimensions({_B.TIME: 1.0}))
    TORQUE = VariableDescriptor(
        "torque", Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    TORQUE_MAGNITUDE = VariableDescriptor(
        "torque_magnitude", Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    TORQUE_X = VariableDescriptor(
        "torque_x", Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    TORQUE_Y = VariableDescriptor(
        "torque_y", Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    TORQUE_Z = VariableDescriptor(
        "torque_z", Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    TOTAL_ENERGY = VariableDescriptor(
        "total_energy", Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    TOTAL_PRESSURE = VariableDescriptor(
        "total_pressure", Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    TOTAL_TEMPERATURE = VariableDescriptor(
        "total_temperature", Dimensions({_B.TEMPERATURE: 1.0})
    )
    TOUGHNESS = VariableDescriptor(
        "toughness", Dimensions({_B.LENGTH: -1.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    TRANSMITTANCE = VariableDescriptor("transmittance", Dimensions({}))
    TURBULENT_DISSIPATION_RATE = VariableDescriptor(
        "turbulent_dissipation_rate", Dimensions({_B.LENGTH: 2.0, _B.TIME: 3.0})
    )
    TURBULENT_INTENSITY = VariableDescriptor("turbulent_intensity", Dimensions({}))
    TURBULENT_KINETIC_ENERGY = VariableDescriptor(
        "turbulent_kinetic_energy", Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    TURBULENT_REYNOLDS_NUMBER = VariableDescriptor(
        "turbulent_reynolds_number", Dimensions({})
    )
    TURBULENT_VISCOSITY = VariableDescriptor(
        "turbulent_viscosity",
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -1.0}),
    )
    TURBULENT_VISCOSITY_RATIO = VariableDescriptor(
        "turbulent_viscosity_ratio", Dimensions({})
    )
    VAPOR_PRESSURE = VariableDescriptor(
        "vapor_pressure", Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    VELOCITY = VariableDescriptor(
        "velocity", Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    VELOCITY_MAGNITUDE = VariableDescriptor(
        "velocity_magnitude", Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    VELOCITY_X = VariableDescriptor(
        "velocity_x", Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    VELOCITY_Y = VariableDescriptor(
        "velocity_y", Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    VELOCITY_Z = VariableDescriptor(
        "velocity_z", Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    VISCOSITY = VariableDescriptor(
        "viscosity", Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -1.0})
    )
    VOLUME = VariableDescriptor("volume", Dimensions({_B.LENGTH: 3.0}))
    VOLUMETRIC_FLOW = VariableDescriptor(
        "volumetric_flow", Dimensions({_B.LENGTH: 3.0, _B.TIME: -1.0})
    )
    VOLUME_FRACTION = VariableDescriptor("volume_fraction", Dimensions({}))
    VORTICITY = VariableDescriptor("vorticity", Dimensions({_B.TIME: -1.0}))
    VORTICITY_MAGNITUDE = VariableDescriptor(
        "vorticity_magnitude", Dimensions({_B.TIME: -1.0})
    )
    VORTICITY_X = VariableDescriptor("vorticity_x", Dimensions({_B.TIME: -1.0}))
    VORTICITY_Y = VariableDescriptor("vorticity_y", Dimensions({_B.TIME: -1.0}))
    VORTICITY_Z = VariableDescriptor("vorticity_z", Dimensions({_B.TIME: -1.0}))
    WALL_ADJACENT_HEAT_TRANSFER_COEFFICIENT = VariableDescriptor(
        "wall_adjacent_heat_transfer_coefficient",
        Dimensions({_B.MASS: 1.0, _B.TIME: -3.0, _B.TEMPERATURE: -1.0}),
    )
    WALL_ADJACENT_TEMPERATURE = VariableDescriptor(
        "wall_adjacent_temperature", Dimensions({_B.TEMPERATURE: 1.0})
    )
    WALL_SHEAR_STRESS = VariableDescriptor(
        "wall_shear_stress", Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    WALL_SHEAR_STRESS_MAGNITUDE = VariableDescriptor(
        "wall_shear_stress_magnitude",
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0}),
    )
    WALL_SHEAR_STRESS_X = VariableDescriptor(
        "wall_shear_stress_x",
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0}),
    )
    WALL_SHEAR_STRESS_Y = VariableDescriptor(
        "wall_shear_stress_y",
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0}),
    )
    WALL_SHEAR_STRESS_Z = VariableDescriptor(
        "wall_shear_stress_z",
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0}),
    )
    WALL_TEMPERATURE = VariableDescriptor(
        "wall_temperature", Dimensions({_B.TEMPERATURE: 1.0})
    )
    WALL_TEMPERATURE_THIN = VariableDescriptor(
        "wall_temperature_thin", Dimensions({_B.TEMPERATURE: 1.0})
    )
    WALL_Y_PLUS = VariableDescriptor("wall_y_plus", Dimensions({}))
    WALL_Y_STAR = VariableDescriptor("wall_y_star", Dimensions({}))
    WAVENUMBER = VariableDescriptor("wavenumber", Dimensions({_B.LENGTH: -1.0}))
    YANK = VariableDescriptor(
        "yank", Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -3.0})
    )
    YIELD_STRENGTH = VariableDescriptor(
        "yield_strength", Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    YOUNG_MODULUS = VariableDescriptor(
        "young_modulus", Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )

    @final
    class fluent:
        """Dictionary of variable descriptors for fluent-related quantities."""

        HELICITY = VariableDescriptor("helicity", _D.ACCELERATION)
        LAMBDA_2_CRITERION = VariableDescriptor("lambda_2_criterion", _D.TIME**-2)
        DENSITY_ALL = VariableDescriptor("density_all", _D.DENSITY)
        Y_PLUS_BASED_HEAT_TRANSFER_COEFFICIENT = VariableDescriptor(
            "y_plus_based_heat_transfer_coefficient",
            _D.POWER * _D.LENGTH**-2 * _D.TEMPERATURE**-1,
        )
        TOTAL_ENTHALPY_DEVIATION = VariableDescriptor(
            "total_enthalpy_deviation", _D.SPECIFIC_ENTHALPY
        )
        MASS_IMBALANCE = VariableDescriptor("mass_imbalance", _D.MASS * _D.TIME**-1)
        PRESSURE_HESSIAN_INDICATOR = VariableDescriptor(
            "pressure_hessian_indicator", Dimensions()
        )
        VELOCITY_ANGLE = VariableDescriptor("velocity_angle", _D.ANGLE)
        DVELOCITY_DX = VariableDescriptor("dvelocity_dx", _D.TIME**-1)
        DVELOCITY_DX_MAGNITUDE = VariableDescriptor(
            "dvelocity_dx_magnitude", _D.TIME**-1
        )
        DVELOCITY_DX_X = VariableDescriptor("dvelocity_dx_x", _D.TIME**-1)
        DVELOCITY_DX_Y = VariableDescriptor("dvelocity_dx_y", _D.TIME**-1)
        DVELOCITY_DX_Z = VariableDescriptor("dvelocity_dx_z", _D.TIME**-1)
        DVELOCITY_DY = VariableDescriptor("dvelocity_dy", _D.TIME**-1)
        DVELOCITY_DY_MAGNITUDE = VariableDescriptor(
            "dvelocity_dy_magnitude", _D.TIME**-1
        )
        DVELOCITY_DY_X = VariableDescriptor("dvelocity_dy_x", _D.TIME**-1)
        DVELOCITY_DY_Y = VariableDescriptor("dvelocity_dy_y", _D.TIME**-1)
        DVELOCITY_DY_Z = VariableDescriptor("dvelocity_dy_z", _D.TIME**-1)
        DVELOCITY_DZ = VariableDescriptor("dvelocity_dz", _D.TIME**-1)
        DVELOCITY_DZ_MAGNITUDE = VariableDescriptor(
            "dvelocity_dz_magnitude", _D.TIME**-1
        )
        DVELOCITY_DZ_X = VariableDescriptor("dvelocity_dz_x", _D.TIME**-1)
        DVELOCITY_DZ_Y = VariableDescriptor("dvelocity_dz_y", _D.TIME**-1)
        DVELOCITY_DZ_Z = VariableDescriptor("dvelocity_dz_z", _D.TIME**-1)
        VOLUME_FRACTION_PRIMARY_PHASE = VariableDescriptor(
            "volume_fraction_primary_phase", _D.VOLUME_FRACTION
        )
        VOLUME_FRACTION_SECONDARY_PHASE = VariableDescriptor(
            "volume_fraction_secondary_phase", _D.VOLUME_FRACTION
        )

    @final
    class mesh:
        """Dictionary of variable descriptors for mesh-related quantities."""

        ANISOTROPIC_ADAPTION_CELLS = VariableDescriptor(
            "anisotropic_adaption_cells", Dimensions()
        )
        BOUNDARY_CELL_DISTANCE = VariableDescriptor(
            "boundary_cell_distance", Dimensions()
        )
        BOUNDARY_LAYER_CELLS = VariableDescriptor("boundary_layer_cells", Dimensions())
        BOUNDARY_NORMAL_DISTANCE = VariableDescriptor(
            "boundary_normal_distance", Dimensions()
        )
        BOUNDARY_VOLUME_DISTANCE = VariableDescriptor(
            "boundary_volume_distance", Dimensions()
        )
        CELL_EQUIANGLE_SKEW = VariableDescriptor("cell_equiangle_skew", Dimensions())
        CELL_EQUIVOLUME_SKEW = VariableDescriptor("cell_equivolume_skew", Dimensions())
        CELL_PARENT_INDEX = VariableDescriptor("cell_parent_index", Dimensions())
        CELL_REFINE_LEVEL = VariableDescriptor("cell_refine_level", Dimensions())
        CELL_VOLUME = VariableDescriptor("cell_volume", _D.VOLUME)
        CELL_VOLUME_CHANGE = VariableDescriptor("cell_volume_change", Dimensions())
        ELEMENT_ASPECT_RATIO = VariableDescriptor("element_aspect_ratio", Dimensions())
        ELEMENT_WALL_DISTANCE = VariableDescriptor("element_wall_distance", _D.LENGTH)
        FACE_AREA_MAGNITUDE = VariableDescriptor("face_area_magnitude", _D.AREA)
        FACE_HANDEDNESS = VariableDescriptor("face_handedness", Dimensions())
        INTERFACE_OVERLAP_FRACTION = VariableDescriptor(
            "interface_overlap_fraction", Dimensions()
        )
        MARK_POOR_ELEMENTS = VariableDescriptor("mark_poor_elements", Dimensions())
        SMOOTHED_CELL_REFINE_LEVEL = VariableDescriptor(
            "smoothed_cell_refine_level", Dimensions()
        )
        X_FACE_AREA = VariableDescriptor("x_face_area", _D.AREA)
        Y_FACE_AREA = VariableDescriptor("y_face_area", _D.AREA)
        Z_FACE_AREA = VariableDescriptor("z_face_area", _D.AREA)
        ACTIVE_CELL_PARTITION = VariableDescriptor(
            "active_cell_partition", Dimensions()
        )
        CELL_ELEMENT_TYPE = VariableDescriptor("cell_element_type", Dimensions())
        CELL_ID = VariableDescriptor("cell_id", Dimensions())
        CELL_WEIGHT = VariableDescriptor("cell_weight", Dimensions())
        CELL_ZONE_INDEX = VariableDescriptor("cell_zone_index", Dimensions())
        CELL_ZONE_TYPE = VariableDescriptor("cell_zone_type", Dimensions())
        PARTITION_NEIGHBOURS = VariableDescriptor("partition_neighbours", Dimensions())
        STORED_CELL_PARTITION = VariableDescriptor(
            "stored_cell_partition", Dimensions()
        )

    # endregion


# Add custom descriptors
VariableCatalog.add("STORED_CELL_PARTITIION", Dimensions(), "mesh")  # deprecated typo
