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
# This file is @generated

from typing_extensions import final

from ansys.units.base_dimensions import BaseDimensions as _B
from ansys.units.dimensions import Dimensions
from ansys.units.quantity_dimensions import QuantityDimensions as _D
from ansys.units.variable_descriptor.variable_descriptor import (
    ScalarVariableDescriptor,
    VariableCatalogBase,
    VectorVariableDescriptor,
)


@final
class VariableCatalog(VariableCatalogBase):
    """A catalog of variable descriptors."""

    ABSOLUTE_PRESSURE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    ABSORBANCE = ScalarVariableDescriptor(Dimensions({}))
    ABSORBED_DOSE_RATE = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -3.0})
    )
    ACCELERATION = VectorVariableDescriptor(Dimensions({_B.LENGTH: 1.0, _B.TIME: -2.0}))
    ACCELERATION_MAGNITUDE = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    ACCELERATION_X = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    ACCELERATION_Y = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    ACCELERATION_Z = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    ACOUSTICAL_ABSORPTION = ScalarVariableDescriptor(Dimensions({}))
    ACTION = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -1.0})
    )
    ANGLE = ScalarVariableDescriptor(Dimensions({_B.ANGLE: 1.0}))
    ANGULAR_ACCELERATION = ScalarVariableDescriptor(Dimensions({_B.TIME: -2.0}))
    ANGULAR_MOMENTUM = VectorVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -1.0})
    )
    ANGULAR_MOMENTUM_MAGNITUDE = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -1.0})
    )
    ANGULAR_MOMENTUM_X = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -1.0})
    )
    ANGULAR_MOMENTUM_Y = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -1.0})
    )
    ANGULAR_MOMENTUM_Z = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -1.0})
    )
    ANGULAR_VELOCITY = ScalarVariableDescriptor(Dimensions({_B.TIME: -1.0}))
    AREA = ScalarVariableDescriptor(Dimensions({_B.LENGTH: 2.0}))
    AREA_DENSITY = ScalarVariableDescriptor(Dimensions({_B.MASS: 1.0, _B.LENGTH: -2.0}))
    ATOMIC_MASS = ScalarVariableDescriptor(Dimensions({_B.MASS: 1.0}))
    ATOMIC_NUMBER = ScalarVariableDescriptor(Dimensions({}))
    ATTENUATION_COEFFICIENT = ScalarVariableDescriptor(Dimensions({_B.LENGTH: -1.0}))
    AXIAL_VELOCITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    BIREFRINGENCE = ScalarVariableDescriptor(Dimensions({}))
    BULK_MODULUS = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    CAPACITANCE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: -1.0, _B.LENGTH: -2.0, _B.TIME: 4.0, _B.CURRENT: 2.0})
    )
    CATALYTIC_EFFICIENCY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 3.0, _B.CHEMICAL_AMOUNT: -1.0, _B.TIME: -1.0})
    )
    CELL_REYNOLDS_NUMBER = ScalarVariableDescriptor(Dimensions({}))
    CHEMICAL_AMOUNT = ScalarVariableDescriptor(Dimensions({_B.CHEMICAL_AMOUNT: 1.0}))
    COEFFICIENT_OF_RESTITUTION = ScalarVariableDescriptor(Dimensions({}))
    COLOR = ScalarVariableDescriptor(Dimensions({}))
    COMPRESSIBILITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: -1.0, _B.LENGTH: 1.0, _B.TIME: 2.0})
    )
    COMPRESSIVE_STRENGTH = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    CONVECTIVE_COURANT_NUMBER = ScalarVariableDescriptor(Dimensions({}))
    CORROSION_RESISTANCE = ScalarVariableDescriptor(Dimensions({}))
    CREEP = ScalarVariableDescriptor(Dimensions({_B.TIME: -1.0}))
    CURIE_TEMPERATURE = ScalarVariableDescriptor(Dimensions({_B.TEMPERATURE: 1.0}))
    CURRENT = ScalarVariableDescriptor(Dimensions({_B.CURRENT: 1.0}))
    DENSITY = ScalarVariableDescriptor(Dimensions({_B.MASS: 1.0, _B.LENGTH: -3.0}))
    DIAMAGNETISM = ScalarVariableDescriptor(Dimensions({}))
    DIELECTRIC_CONSTANT = ScalarVariableDescriptor(Dimensions({}))
    DIELECTRIC_STRENGTH = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -3.0, _B.CURRENT: -1.0})
    )
    DUCTILITY = ScalarVariableDescriptor(Dimensions({}))
    DURABILITY = ScalarVariableDescriptor(Dimensions({}))
    DYNAMIC_PRESSURE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    DYNAMIC_VISCOSITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -1.0})
    )
    EFFECTIVE_PRANDTL_NUMBER = ScalarVariableDescriptor(Dimensions({}))
    EFFECTIVE_THERMAL_CONDUCTIVITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.MASS: 1.0, _B.TIME: -3.0, _B.TEMPERATURE: -1.0})
    )
    EFFECTIVE_VISCOSITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -1.0})
    )
    ELASTICITY = ScalarVariableDescriptor(Dimensions({}))
    ELECTRICAL_CAPACITANCE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: -1.0, _B.LENGTH: -2.0, _B.TIME: 4.0, _B.CURRENT: 2.0})
    )
    ELECTRICAL_CONDUCTANCE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: -1.0, _B.LENGTH: -2.0, _B.TIME: 3.0, _B.CURRENT: 2.0})
    )
    ELECTRICAL_CONDUCTIVITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: -1.0, _B.LENGTH: -3.0, _B.TIME: 3.0, _B.CURRENT: 2.0})
    )
    ELECTRICAL_IMPEDANCE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0, _B.TIME: -3.0, _B.CURRENT: -2.0})
    )
    ELECTRICAL_INDUCTANCE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0, _B.TIME: -2.0, _B.CURRENT: -2.0})
    )
    ELECTRICAL_POTENTIAL = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0, _B.TIME: -3.0, _B.CURRENT: -1.0})
    )
    ELECTRICAL_REACTANCE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0, _B.TIME: -3.0, _B.CURRENT: -2.0})
    )
    ELECTRICAL_RESISTANCE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0, _B.TIME: -3.0, _B.CURRENT: -2.0})
    )
    ELECTRICAL_RESISTIVITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 3.0, _B.TIME: -3.0, _B.CURRENT: -2.0})
    )
    ELECTRIC_CHARGE = ScalarVariableDescriptor(
        Dimensions({_B.TIME: 1.0, _B.CURRENT: 1.0})
    )
    ELECTRIC_SUSCEPTIBILITY = ScalarVariableDescriptor(Dimensions({}))
    ELECTROCALORIC_COEFFICIENT = ScalarVariableDescriptor(
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
    ELECTROSTRICTION = ScalarVariableDescriptor(Dimensions({}))
    ELECTRO_OPTIC_EFFECT = ScalarVariableDescriptor(Dimensions({}))
    EMISSIVITY = ScalarVariableDescriptor(Dimensions({}))
    ENERGY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    ENERGY_DENSITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: -1.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    ENERGY_FLUX_DENSITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.TIME: -3.0})
    )
    ENTHALPY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    ENTROPY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0, _B.TEMPERATURE: -1.0})
    )
    FATIGUE_LIMIT = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    FLEXURAL_MODULUS = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    FLEXURAL_STRENGTH = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    FORCE = VectorVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    FORCE_MAGNITUDE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    FORCE_X = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    FORCE_Y = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    FORCE_Z = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    FRACTURE_TOUGHNESS = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.TIME: -2.0})
    )
    FREQUENCY = ScalarVariableDescriptor(Dimensions({_B.TIME: -1.0}))
    FREQUENCY_DRIFT = ScalarVariableDescriptor(Dimensions({_B.TIME: -2.0}))
    FRICTION_COEFFICIENT = ScalarVariableDescriptor(Dimensions({}))
    FUEL_EFFICIENCY = ScalarVariableDescriptor(Dimensions({_B.LENGTH: -2.0}))
    HALF_LIFE = ScalarVariableDescriptor(Dimensions({_B.TIME: 1.0}))
    HALL_COEFFICIENT = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 3.0, _B.CURRENT: -1.0, _B.TIME: -1.0})
    )
    HARDNESS = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    HEAT_CAPACITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0, _B.TEMPERATURE: -1.0})
    )
    HEAT_FLUX_DENSITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.TIME: -3.0})
    )
    HEAT_OF_VAPORIZATION = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    HYGROSCOPY = ScalarVariableDescriptor(Dimensions({}))
    HYSTERESIS = ScalarVariableDescriptor(Dimensions({}))
    ILLUMINANCE = ScalarVariableDescriptor(
        Dimensions({_B.LIGHT: 1.0, _B.SOLID_ANGLE: 1.0, _B.LENGTH: -2.0})
    )
    INTERNAL_ENERGY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    JERK = ScalarVariableDescriptor(Dimensions({_B.LENGTH: 1.0, _B.TIME: -3.0}))
    KINEMATIC_VISCOSITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -1.0})
    )
    LENGTH = ScalarVariableDescriptor(Dimensions({_B.LENGTH: 1.0}))
    LIGHT = ScalarVariableDescriptor(Dimensions({_B.LIGHT: 1.0}))
    LINEAR_MASS_DENSITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0})
    )
    LUMINANCE = ScalarVariableDescriptor(Dimensions({_B.LIGHT: 1.0, _B.LENGTH: -2.0}))
    LUMINOSITY = ScalarVariableDescriptor(
        Dimensions({_B.LIGHT: 1.0, _B.SOLID_ANGLE: 1.0})
    )
    LUMINOUS_EXPOSURE = ScalarVariableDescriptor(
        Dimensions({_B.LIGHT: 1.0, _B.SOLID_ANGLE: 1.0, _B.LENGTH: -2.0, _B.TIME: 1.0})
    )
    LUMINOUS_FLUX = ScalarVariableDescriptor(
        Dimensions({_B.LIGHT: 1.0, _B.SOLID_ANGLE: 1.0})
    )
    MAGNETIC_FLUX = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0, _B.TIME: -2.0, _B.CURRENT: -1.0})
    )
    MAGNETIC_INDUCTION = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.TIME: -2.0, _B.CURRENT: -1.0})
    )
    MAGNETIC_PERMEABILITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.MASS: 1.0, _B.TIME: -2.0, _B.CURRENT: -2.0})
    )
    MAGNETIC_VECTOR_POTENTIAL = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.MASS: 1.0, _B.TIME: -2.0, _B.CURRENT: -1.0})
    )
    MAGNETOCALORIC_COEFFICIENT = ScalarVariableDescriptor(
        Dimensions({_B.TEMPERATURE: 1.0, _B.MASS: -1.0, _B.TIME: 2.0, _B.CURRENT: 1.0})
    )
    MAGNETOELECTRIC_POLARIZABILITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: -1.0, _B.TIME: -1.0})
    )
    MAGNETORESISTANCE = ScalarVariableDescriptor(Dimensions({}))
    MAGNETOSTRICTION = ScalarVariableDescriptor(Dimensions({}))
    MAGNETOTHERMOELECTRIC_POWER = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -1.0, _B.TEMPERATURE: -1.0})
    )
    MALLEABILITY = ScalarVariableDescriptor(Dimensions({}))
    MASS = ScalarVariableDescriptor(Dimensions({_B.MASS: 1.0}))
    MASS_CONTROL = ScalarVariableDescriptor(Dimensions({_B.MASS: 1.0, _B.TIME: -3.0}))
    MASS_DIFFUSIVITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -1.0})
    )
    MASS_FLOW_RATE = ScalarVariableDescriptor(Dimensions({_B.MASS: 1.0, _B.TIME: -1.0}))
    MAXIMUM_ENERGY_PRODUCT = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: -1.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    MELTING_POINT = ScalarVariableDescriptor(Dimensions({_B.TEMPERATURE: 1.0}))
    MESH_VELOCITY = VectorVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MESH_VELOCITY_MAGNITUDE = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MESH_VELOCITY_X = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MESH_VELOCITY_Y = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MESH_VELOCITY_Z = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MOLALITY = ScalarVariableDescriptor(
        Dimensions({_B.CHEMICAL_AMOUNT: 1.0, _B.MASS: -1.0})
    )
    MOLARITY = ScalarVariableDescriptor(
        Dimensions({_B.CHEMICAL_AMOUNT: 1.0, _B.LENGTH: -3.0})
    )
    MOLAR_ENERGY = ScalarVariableDescriptor(
        Dimensions(
            {_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0, _B.CHEMICAL_AMOUNT: -1.0}
        )
    )
    MOLAR_ENTROPY = ScalarVariableDescriptor(
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
    MOLAR_HEAT_CAPACITY = ScalarVariableDescriptor(
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
    MOLAR_MASS = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.CHEMICAL_AMOUNT: -1.0})
    )
    MOLAR_VOLUME = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 3.0, _B.CHEMICAL_AMOUNT: -1.0})
    )
    MOMENTUM = VectorVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MOMENTUM_MAGNITUDE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MOMENTUM_X = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MOMENTUM_Y = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MOMENTUM_Z = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    MOMENT_OF_INERTIA = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0})
    )
    NERNST_COEFFICIENT = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -1.0, _B.TEMPERATURE: -1.0})
    )
    NEUTRON_CROSS_SECTION = ScalarVariableDescriptor(Dimensions({_B.LENGTH: 2.0}))
    NORMALIZED_Q_CRITERION = ScalarVariableDescriptor(Dimensions({}))
    OPTICAL_ACTIVITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.MASS: -1.0})
    )
    PERMEABILITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.MASS: 1.0, _B.TIME: -2.0, _B.CURRENT: -2.0})
    )
    PERMITTIVITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: -1.0, _B.LENGTH: -3.0, _B.TIME: 4.0, _B.CURRENT: 2.0})
    )
    PH = ScalarVariableDescriptor(Dimensions({}))
    PHOTOELASTICITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: -1.0, _B.LENGTH: 1.0, _B.TIME: 2.0})
    )
    PHOTOSENSITIVITY = ScalarVariableDescriptor(Dimensions({}))
    PIEZOELECTRIC_CONSTANTS = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -1.0, _B.CURRENT: -1.0})
    )
    PIEZOMAGNETISM = ScalarVariableDescriptor(
        Dimensions({_B.CURRENT: -1.0, _B.LENGTH: 1.0})
    )
    PLASTICITY = ScalarVariableDescriptor(Dimensions({}))
    POISSON_RATIO = ScalarVariableDescriptor(Dimensions({}))
    POSITION = VectorVariableDescriptor(Dimensions({_B.LENGTH: 1.0}))
    POSITION_MAGNITUDE = ScalarVariableDescriptor(Dimensions({_B.LENGTH: 1.0}))
    POSITION_X = ScalarVariableDescriptor(Dimensions({_B.LENGTH: 1.0}))
    POSITION_Y = ScalarVariableDescriptor(Dimensions({_B.LENGTH: 1.0}))
    POSITION_Z = ScalarVariableDescriptor(Dimensions({_B.LENGTH: 1.0}))
    POWER = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -3.0})
    )
    PRANDTL_NUMBER = ScalarVariableDescriptor(Dimensions({}))
    PRESSURE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    PRESSURE_COEFFICIENT = ScalarVariableDescriptor(Dimensions({}))
    PRODUCTION_OF_TURBULENT_KINETIC_ENERGY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -3.0})
    )
    PYROELECTRICITY = ScalarVariableDescriptor(
        Dimensions({_B.CURRENT: 1.0, _B.LENGTH: -2.0, _B.TEMPERATURE: -1.0})
    )
    PYROMAGNETIC_COEFFICIENT = ScalarVariableDescriptor(
        Dimensions(
            {_B.MASS: 1.0, _B.TIME: -2.0, _B.CURRENT: -1.0, _B.TEMPERATURE: -1.0}
        )
    )
    Q_CRITERION = ScalarVariableDescriptor(Dimensions({_B.TIME: -2.0}))
    RADIAL_VELOCITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    RADIANCE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.TIME: -3.0, _B.SOLID_ANGLE: -1.0})
    )
    RADIANT_EXPOSURE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.TIME: -2.0})
    )
    RADIANT_INTENSITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -3.0, _B.SOLID_ANGLE: -1.0})
    )
    REACTIVITY = ScalarVariableDescriptor(Dimensions({}))
    REFLECTIVITY = ScalarVariableDescriptor(Dimensions({}))
    REFRACTIVE_INDEX = ScalarVariableDescriptor(Dimensions({}))
    RELATIVE_ATOMIC_MASS = ScalarVariableDescriptor(Dimensions({}))
    RESILIENCE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    SCATTERING = ScalarVariableDescriptor(Dimensions({}))
    SEEBECK_COEFFICIENT = ScalarVariableDescriptor(
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
    SHEAR_MODULUS = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    SHEAR_STRENGTH = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    SKIN_FRICTION_COEFFICIENT = ScalarVariableDescriptor(Dimensions({}))
    SLIP = ScalarVariableDescriptor(Dimensions({}))
    SNAP = ScalarVariableDescriptor(Dimensions({_B.LENGTH: 1.0, _B.TIME: -4.0}))
    SOLID_ANGLE = ScalarVariableDescriptor(Dimensions({_B.SOLID_ANGLE: 1.0}))
    SOUND_REFLECTION = ScalarVariableDescriptor(Dimensions({}))
    SOUND_TRANSFER = ScalarVariableDescriptor(Dimensions({}))
    SPECIFIC_ACTIVITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: -1.0, _B.TIME: -1.0})
    )
    SPECIFIC_ANGULAR_MOMENTUM = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -1.0})
    )
    SPECIFIC_DISSIPATION_RATE = ScalarVariableDescriptor(Dimensions({_B.TIME: -1.0}))
    SPECIFIC_ENERGY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    SPECIFIC_ENTHALPY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    SPECIFIC_ENTROPY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0, _B.TEMPERATURE: -1.0})
    )
    SPECIFIC_HEAT_CAPACITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0, _B.TEMPERATURE: -1.0})
    )
    SPECIFIC_INTERNAL_ENERGY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    SPECIFIC_INTERNAL_SURFACE_AREA = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: -1.0})
    )
    SPECIFIC_MODULUS = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    SPECIFIC_STRENGTH = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    SPECIFIC_TOTAL_ENERGY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    SPECIFIC_TOTAL_ENTHALPY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    SPECIFIC_VOLUME = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 3.0, _B.MASS: -1.0})
    )
    SPECIFIC_WEIGHT = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -2.0, _B.TIME: -2.0})
    )
    SPECTRAL_INTENSITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.MASS: 1.0, _B.TIME: -3.0, _B.SOLID_ANGLE: -1.0})
    )
    SPECTRAL_IRRADIANCE = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: -1.0, _B.MASS: 1.0, _B.TIME: -3.0})
    )
    SPECTRAL_POWER = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.MASS: 1.0, _B.TIME: -3.0})
    )
    SPEED_OF_SOUND = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    SPIN_HALL_EFFECT = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0, _B.TIME: -3.0, _B.CURRENT: -2.0})
    )
    STANDARD_ATOMIC_WEIGHT = ScalarVariableDescriptor(Dimensions({}))
    STATIC_PRESSURE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    STRAIN_RATE = ScalarVariableDescriptor(Dimensions({_B.TIME: -1.0}))
    STRESS = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    SURFACE_ENERGY = ScalarVariableDescriptor(Dimensions({_B.MASS: 1.0, _B.TIME: -2.0}))
    SURFACE_HEAT_FLUX = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.TIME: -3.0})
    )
    SURFACE_HEAT_TRANSFER_COEFFICIENT = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.TIME: -3.0, _B.TEMPERATURE: -1.0})
    )
    SURFACE_NUSSELT_NUMBER = ScalarVariableDescriptor(Dimensions({}))
    SURFACE_ROUGHNESS = ScalarVariableDescriptor(Dimensions({_B.LENGTH: 1.0}))
    SURFACE_STANTON_NUMBER = ScalarVariableDescriptor(Dimensions({}))
    SURFACE_TENSION = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.TIME: -2.0})
    )
    TANGENTIAL_VELOCITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    TEMPERATURE = ScalarVariableDescriptor(Dimensions({_B.TEMPERATURE: 1.0}))
    TEMPERATURE_DIFFERENCE = ScalarVariableDescriptor(
        Dimensions({_B.TEMPERATURE_DIFFERENCE: 1.0})
    )
    TEMPERATURE_GRADIENT = ScalarVariableDescriptor(
        Dimensions({_B.TEMPERATURE: 1.0, _B.LENGTH: -1.0})
    )
    TENSILE_STRENGTH = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    THERMAL_CONDUCTIVITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.MASS: 1.0, _B.TIME: -3.0, _B.TEMPERATURE: -1.0})
    )
    THERMAL_DIFFUSIVITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -1.0})
    )
    THERMAL_EXPANSION_COEFFICIENT = ScalarVariableDescriptor(
        Dimensions({_B.TEMPERATURE: -1.0})
    )
    THERMAL_RESISTANCE = ScalarVariableDescriptor(
        Dimensions({_B.TEMPERATURE: 1.0, _B.LENGTH: -2.0, _B.MASS: -1.0, _B.TIME: 3.0})
    )
    THIRD_ORDER_ELASTICITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    TIME = ScalarVariableDescriptor(Dimensions({_B.TIME: 1.0}))
    TORQUE = VectorVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    TORQUE_MAGNITUDE = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    TORQUE_X = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    TORQUE_Y = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    TORQUE_Z = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    TOTAL_ENERGY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    TOTAL_PRESSURE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    TOTAL_TEMPERATURE = ScalarVariableDescriptor(Dimensions({_B.TEMPERATURE: 1.0}))
    TOUGHNESS = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: -1.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    TRANSMITTANCE = ScalarVariableDescriptor(Dimensions({}))
    TURBULENT_DISSIPATION_RATE = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: 3.0})
    )
    TURBULENT_INTENSITY = ScalarVariableDescriptor(Dimensions({}))
    TURBULENT_KINETIC_ENERGY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    TURBULENT_REYNOLDS_NUMBER = ScalarVariableDescriptor(Dimensions({}))
    TURBULENT_VISCOSITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -1.0})
    )
    TURBULENT_VISCOSITY_RATIO = ScalarVariableDescriptor(Dimensions({}))
    VAPOR_PRESSURE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    VELOCITY = VectorVariableDescriptor(Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0}))
    VELOCITY_MAGNITUDE = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    VELOCITY_X = ScalarVariableDescriptor(Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0}))
    VELOCITY_Y = ScalarVariableDescriptor(Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0}))
    VELOCITY_Z = ScalarVariableDescriptor(Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0}))
    VISCOSITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -1.0})
    )
    VOLUME = ScalarVariableDescriptor(Dimensions({_B.LENGTH: 3.0}))
    VOLUMETRIC_FLOW = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 3.0, _B.TIME: -1.0})
    )
    VOLUME_FRACTION = ScalarVariableDescriptor(Dimensions({}))
    VORTICITY = VectorVariableDescriptor(Dimensions({_B.TIME: -1.0}))
    VORTICITY_MAGNITUDE = ScalarVariableDescriptor(Dimensions({_B.TIME: -1.0}))
    VORTICITY_X = ScalarVariableDescriptor(Dimensions({_B.TIME: -1.0}))
    VORTICITY_Y = ScalarVariableDescriptor(Dimensions({_B.TIME: -1.0}))
    VORTICITY_Z = ScalarVariableDescriptor(Dimensions({_B.TIME: -1.0}))
    WALL_ADJACENT_HEAT_TRANSFER_COEFFICIENT = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.TIME: -3.0, _B.TEMPERATURE: -1.0})
    )
    WALL_ADJACENT_TEMPERATURE = ScalarVariableDescriptor(
        Dimensions({_B.TEMPERATURE: 1.0})
    )
    WALL_SHEAR_STRESS = VectorVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    WALL_SHEAR_STRESS_MAGNITUDE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    WALL_SHEAR_STRESS_X = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    WALL_SHEAR_STRESS_Y = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    WALL_SHEAR_STRESS_Z = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    WALL_TEMPERATURE = ScalarVariableDescriptor(Dimensions({_B.TEMPERATURE: 1.0}))
    WALL_TEMPERATURE_THIN = ScalarVariableDescriptor(Dimensions({_B.TEMPERATURE: 1.0}))
    WALL_Y_PLUS = ScalarVariableDescriptor(Dimensions({}))
    WALL_Y_STAR = ScalarVariableDescriptor(Dimensions({}))
    WAVENUMBER = ScalarVariableDescriptor(Dimensions({_B.LENGTH: -1.0}))
    YANK = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -3.0})
    )
    YIELD_STRENGTH = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    YOUNG_MODULUS = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )

    @final
    class fluent:
        """Dictionary of variable descriptors for fluent-related quantities."""

        HELICITY = ScalarVariableDescriptor(_D.ACCELERATION)
        LAMBDA_2_CRITERION = ScalarVariableDescriptor(_D.TIME**-2)
        DENSITY_ALL = ScalarVariableDescriptor(_D.DENSITY)
        Y_PLUS_BASED_HEAT_TRANSFER_COEFFICIENT = ScalarVariableDescriptor(
            _D.POWER * _D.LENGTH**-2 * _D.TEMPERATURE**-1
        )
        TOTAL_ENTHALPY_DEVIATION = ScalarVariableDescriptor(_D.SPECIFIC_ENTHALPY)
        MASS_IMBALANCE = ScalarVariableDescriptor(_D.MASS * _D.TIME**-1)
        PRESSURE_HESSIAN_INDICATOR = ScalarVariableDescriptor(Dimensions())
        VELOCITY_ANGLE = ScalarVariableDescriptor(_D.ANGLE)
        DVELOCITY_DX = ScalarVariableDescriptor(_D.TIME**-1)
        DVELOCITY_DX_MAGNITUDE = ScalarVariableDescriptor(_D.TIME**-1)
        DVELOCITY_DX_X = ScalarVariableDescriptor(_D.TIME**-1)
        DVELOCITY_DX_Y = ScalarVariableDescriptor(_D.TIME**-1)
        DVELOCITY_DX_Z = ScalarVariableDescriptor(_D.TIME**-1)
        DVELOCITY_DY = ScalarVariableDescriptor(_D.TIME**-1)
        DVELOCITY_DY_MAGNITUDE = ScalarVariableDescriptor(_D.TIME**-1)
        DVELOCITY_DY_X = ScalarVariableDescriptor(_D.TIME**-1)
        DVELOCITY_DY_Y = ScalarVariableDescriptor(_D.TIME**-1)
        DVELOCITY_DY_Z = ScalarVariableDescriptor(_D.TIME**-1)
        DVELOCITY_DZ = ScalarVariableDescriptor(_D.TIME**-1)
        DVELOCITY_DZ_MAGNITUDE = ScalarVariableDescriptor(_D.TIME**-1)
        DVELOCITY_DZ_X = ScalarVariableDescriptor(_D.TIME**-1)
        DVELOCITY_DZ_Y = ScalarVariableDescriptor(_D.TIME**-1)
        DVELOCITY_DZ_Z = ScalarVariableDescriptor(_D.TIME**-1)
        VOLUME_FRACTION_PRIMARY_PHASE = ScalarVariableDescriptor(_D.VOLUME_FRACTION)
        VOLUME_FRACTION_SECONDARY_PHASE = ScalarVariableDescriptor(_D.VOLUME_FRACTION)

    @final
    class mesh:
        """Dictionary of variable descriptors for mesh-related quantities."""

        ANISOTROPIC_ADAPTION_CELLS = ScalarVariableDescriptor(Dimensions())
        BOUNDARY_CELL_DISTANCE = ScalarVariableDescriptor(Dimensions())
        BOUNDARY_LAYER_CELLS = ScalarVariableDescriptor(Dimensions())
        BOUNDARY_NORMAL_DISTANCE = ScalarVariableDescriptor(Dimensions())
        BOUNDARY_VOLUME_DISTANCE = ScalarVariableDescriptor(Dimensions())
        CELL_EQUIANGLE_SKEW = ScalarVariableDescriptor(Dimensions())
        CELL_EQUIVOLUME_SKEW = ScalarVariableDescriptor(Dimensions())
        CELL_PARENT_INDEX = ScalarVariableDescriptor(Dimensions())
        CELL_REFINE_LEVEL = ScalarVariableDescriptor(Dimensions())
        CELL_VOLUME = ScalarVariableDescriptor(_D.VOLUME)
        CELL_VOLUME_CHANGE = ScalarVariableDescriptor(Dimensions())
        ELEMENT_ASPECT_RATIO = ScalarVariableDescriptor(Dimensions())
        ELEMENT_WALL_DISTANCE = ScalarVariableDescriptor(_D.LENGTH)
        FACE_AREA_MAGNITUDE = ScalarVariableDescriptor(_D.AREA)
        FACE_HANDEDNESS = ScalarVariableDescriptor(Dimensions())
        INTERFACE_OVERLAP_FRACTION = ScalarVariableDescriptor(Dimensions())
        MARK_POOR_ELEMENTS = ScalarVariableDescriptor(Dimensions())
        SMOOTHED_CELL_REFINE_LEVEL = ScalarVariableDescriptor(Dimensions())
        X_FACE_AREA = ScalarVariableDescriptor(_D.AREA)
        Y_FACE_AREA = ScalarVariableDescriptor(_D.AREA)
        Z_FACE_AREA = ScalarVariableDescriptor(_D.AREA)
        ACTIVE_CELL_PARTITION = ScalarVariableDescriptor(Dimensions())
        CELL_ELEMENT_TYPE = ScalarVariableDescriptor(Dimensions())
        CELL_ID = ScalarVariableDescriptor(Dimensions())
        CELL_WEIGHT = ScalarVariableDescriptor(Dimensions())
        CELL_ZONE_INDEX = ScalarVariableDescriptor(Dimensions())
        CELL_ZONE_TYPE = ScalarVariableDescriptor(Dimensions())
        PARTITION_NEIGHBOURS = ScalarVariableDescriptor(Dimensions())
        STORED_CELL_PARTITION = ScalarVariableDescriptor(Dimensions())
        STORED_CELL_PARTITIION = ScalarVariableDescriptor(Dimensions())
