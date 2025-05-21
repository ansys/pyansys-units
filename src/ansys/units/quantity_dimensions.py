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
Defines immutable objects representing SI base and derived physical dimensions.

This module provides globally defined `Dimensions` instances corresponding to the
seven SI base quantities (e.g., mass, time) and many commonly used derived quantities
(e.g., force, energy, pressure). These dimension definitions are used internally
for dimensional analysis, quantity construction, and validation.

Each dimension is represented as a `Dimensions` object, which captures the
dimensional exponents of base quantities such as mass, length, and time.

This module is not intended for direct modification at runtime. All objects
are statically defined and immutable.

Examples
--------
>>> from ansys.units.dimensions import Dimensions
>>> from ansys.units.quantity_dimensions import QuantityDimensions

>>> force = QuantityDimensions.FORCE
>>> pressure = QuantityDimensions.PRESSURE
>>> pressure == force / QuantityDimensions.AREA
True
"""

from ansys.units.base_dimensions import BaseDimensions
from ansys.units.dimensions import Dimensions

# Local function to convert from a `BaseDimensions` enum object to a `Dimensions` object


def _make_base_dimensions(dimension: BaseDimensions) -> Dimensions:
    return Dimensions(dimensions={dimension: 1.0})


def _expand_vector_quantities(cls):
    angle = _make_base_dimensions(BaseDimensions.ANGLE)
    for name in getattr(cls, "_vector_quantities", []):
        value = getattr(cls, name)
        # cartesian only added by default
        setattr(cls, f"{name}_X", value)
        setattr(cls, f"{name}_Y", value)
        setattr(cls, f"{name}_Z", value)
        # magnitude
        setattr(cls, f"{name}_MAGNITUDE", value)
    return cls


@_expand_vector_quantities
class QuantityDimensions:
    """
    Defines immutable dimension objects for standard physical quantities.

    This class encapsulates SI base dimensions (e.g., MASS, TIME) and
    commonly used derived dimensions (e.g., FORCE, PRESSURE, ENERGY),
    using `Dimensions` instances.

    These objects support arithmetic operations (multiplication, division,
    exponentiation) to enable dimensional composition and analysis.

    All attributes are class-level constants and should be treated as immutable.

    Examples
    --------
    >>> QuantityDimensions.VELOCITY
    Dimensions(dimensions={BaseDimensions.LENGTH: 1.0, BaseDimensions.TIME: -1.0})
    """

    # Dimensions of base quantities
    MASS = _make_base_dimensions(BaseDimensions.MASS)
    LENGTH = _make_base_dimensions(BaseDimensions.LENGTH)
    TIME = _make_base_dimensions(BaseDimensions.TIME)
    TEMPERATURE = _make_base_dimensions(BaseDimensions.TEMPERATURE)
    CHEMICAL_AMOUNT = _make_base_dimensions(BaseDimensions.CHEMICAL_AMOUNT)
    LIGHT = _make_base_dimensions(BaseDimensions.LIGHT)
    CURRENT = _make_base_dimensions(BaseDimensions.CURRENT)

    # Supplementary base quantities
    ANGLE = _make_base_dimensions(BaseDimensions.ANGLE)
    SOLID_ANGLE = _make_base_dimensions(BaseDimensions.SOLID_ANGLE)
    TEMPERATURE_DIFFERENCE = _make_base_dimensions(
        BaseDimensions.TEMPERATURE_DIFFERENCE
    )

    # Dimensions of derived quantities

    # Kinematics and mechanics
    AREA = LENGTH**2
    VOLUME = LENGTH**3
    FREQUENCY = TIME**-1
    VELOCITY = LENGTH / TIME
    ACCELERATION = VELOCITY / TIME
    FORCE = MASS * ACCELERATION
    PRESSURE = FORCE / AREA
    STRESS = PRESSURE
    JERK = LENGTH / TIME**3
    SNAP = LENGTH / TIME**4
    ANGULAR_VELOCITY = TIME**-1
    ANGULAR_ACCELERATION = TIME**-2
    VOLUMETRIC_FLOW = VOLUME / TIME
    MOMENTUM = MASS * VELOCITY
    ANGULAR_MOMENTUM = LENGTH**2 * MASS / TIME
    TORQUE = LENGTH**2 * MASS / TIME**2
    ENERGY = LENGTH**2 * MASS / TIME**2
    POWER = ENERGY / TIME
    DENSITY = MASS / VOLUME
    SPECIFIC_VOLUME = VOLUME / MASS
    ENERGY_DENSITY = ENERGY / VOLUME
    SURFACE_TENSION = FORCE / LENGTH
    KINEMATIC_VISCOSITY = AREA / TIME
    DYNAMIC_VISCOSITY = PRESSURE * TIME
    MASS_FLOW_RATE = MASS / TIME
    MASS_CONTROL = MASS / TIME**3
    FREQUENCY_DRIFT = TIME**-2
    YANK = FORCE / TIME
    WAVENUMBER = LENGTH**-1
    AREA_DENSITY = MASS / AREA
    ACTION = ENERGY * TIME
    SPECIFIC_ENERGY = ENERGY / MASS
    HEAT_FLUX_DENSITY = POWER / AREA
    SURFACE_HEAT_FLUX = HEAT_FLUX_DENSITY
    LINEAR_MASS_DENSITY = MASS / LENGTH
    RADIANCE = POWER / (SOLID_ANGLE * AREA)
    SPECTRAL_POWER = POWER / LENGTH
    ABSORBED_DOSE_RATE = AREA / TIME**3
    FUEL_EFFICIENCY = LENGTH**-2
    SPECTRAL_IRRADIANCE = POWER / VOLUME
    ENERGY_FLUX_DENSITY = POWER / AREA
    COMPRESSIBILITY = PRESSURE**-1
    RADIANT_EXPOSURE = ENERGY / AREA
    MOMENT_OF_INERTIA = MASS * AREA
    SPECIFIC_ANGULAR_MOMENTUM = ANGULAR_MOMENTUM / MASS
    RADIANT_INTENSITY = POWER / SOLID_ANGLE
    SPECTRAL_INTENSITY = POWER / (SOLID_ANGLE * LENGTH)
    STRAIN_RATE = TIME**-1
    AXIAL_VELOCITY = VELOCITY
    RADIAL_VELOCITY = VELOCITY
    TANGENTIAL_VELOCITY = VELOCITY

    # Electromagnetics
    ELECTRIC_CHARGE = TIME * CURRENT
    ELECTRICAL_POTENTIAL = MASS * AREA * TIME**-3 / CURRENT
    ELECTRICAL_CAPACITANCE = MASS**-1 * LENGTH**-2 * TIME**4 * CURRENT**2
    ELECTRICAL_INDUCTANCE = MASS * LENGTH**2 * TIME**-2 * CURRENT**-2
    ELECTRICAL_RESISTANCE = ELECTRICAL_POTENTIAL / CURRENT
    ELECTRICAL_IMPEDANCE = ELECTRICAL_RESISTANCE
    ELECTRICAL_REACTANCE = ELECTRICAL_RESISTANCE
    ELECTRICAL_CONDUCTANCE = ELECTRICAL_RESISTANCE**-1
    MAGNETIC_FLUX = MASS * LENGTH**2 * TIME**-2 * CURRENT**-1
    MAGNETIC_INDUCTION = MASS * TIME**-2 * CURRENT**-1
    MAGNETIC_PERMEABILITY = LENGTH * MASS * TIME**-2 * CURRENT**-2
    MAGNETIC_VECTOR_POTENTIAL = LENGTH * MASS * TIME**-2 * CURRENT**-1

    # Chemistry
    MOLARITY = CHEMICAL_AMOUNT / VOLUME
    MOLAR_VOLUME = VOLUME / CHEMICAL_AMOUNT
    MOLAR_HEAT_CAPACITY = ENERGY / (TEMPERATURE * CHEMICAL_AMOUNT)
    MOLAR_ENTROPY = MOLAR_HEAT_CAPACITY
    MOLAR_ENERGY = ENERGY / CHEMICAL_AMOUNT
    MOLALITY = CHEMICAL_AMOUNT / MASS
    MOLAR_MASS = MASS / CHEMICAL_AMOUNT
    CATALYTIC_EFFICIENCY = VOLUME / (CHEMICAL_AMOUNT * TIME)

    # Photometry
    LUMINOUS_FLUX = LIGHT * SOLID_ANGLE
    ILLUMINANCE = LUMINOUS_FLUX / AREA
    LUMINANCE = LIGHT / AREA
    LUMINOUS_EXPOSURE = ILLUMINANCE * TIME

    # Thermodynamics
    HEAT_CAPACITY = ENERGY / TEMPERATURE
    SPECIFIC_HEAT_CAPACITY = HEAT_CAPACITY / MASS
    THERMAL_CONDUCTIVITY = POWER / (LENGTH * TEMPERATURE)
    THERMAL_RESISTANCE = TEMPERATURE / POWER
    TEMPERATURE_GRADIENT = TEMPERATURE / LENGTH
    ENTHALPY = ENERGY
    ENTROPY = ENERGY / TEMPERATURE
    SPECIFIC_ENTHALPY = ENTHALPY / MASS
    SPECIFIC_ENTROPY = ENTROPY / MASS
    INTERNAL_ENERGY = ENERGY
    TOTAL_ENERGY = ENERGY
    SPECIFIC_TOTAL_ENERGY = TOTAL_ENERGY / MASS
    SPECIFIC_INTERNAL_ENERGY = INTERNAL_ENERGY / MASS
    TOTAL_TEMPERATURE = TEMPERATURE

    # Turbulence
    PRANDTL_NUMBER = Dimensions()
    EFFECTIVE_PRANDTL_NUMBER = Dimensions()
    EFFECTIVE_THERMAL_CONDUCTIVITY = THERMAL_CONDUCTIVITY
    EFFECTIVE_VISCOSITY = DYNAMIC_VISCOSITY
    PRODUCTION_OF_TURBULENT_KINETIC_ENERGY = MASS * LENGTH**-1 * TIME**-3
    SPECIFIC_DISSIPATION_RATE = TIME**-1
    TURBULENT_DISSIPATION_RATE = LENGTH**2 * TIME**3
    TURBULENT_INTENSITY = Dimensions()
    TURBULENT_VISCOSITY = DYNAMIC_VISCOSITY
    TURBULENT_VISCOSITY_RATIO = Dimensions()
    TURBULENT_REYNOLDS_NUMBER = Dimensions()
    TURBULENT_KINETIC_ENERGY = LENGTH**2 * TIME**-2
    WALL_Y_PLUS = Dimensions()
    WALL_Y_STAR = Dimensions()

    # Fluid pressure
    STATIC_PRESSURE = PRESSURE  # equivalent
    ABSOLUTE_PRESSURE = PRESSURE
    DYNAMIC_PRESSURE = PRESSURE
    TOTAL_PRESSURE = PRESSURE
    PRESSURE_COEFFICIENT = Dimensions()

    # Other fluid and related quantities
    VORTICITY = TIME**-1
    CONVECTIVE_COURANT_NUMBER = Dimensions()
    CELL_REYNOLDS_NUMBER = Dimensions()
    Q_CRITERION = TIME**-2
    NORMALIZED_Q_CRITERION = Dimensions()
    MESH_VELOCITY = VELOCITY
    SPECIFIC_TOTAL_ENTHALPY = SPECIFIC_ENTHALPY
    SURFACE_NUSSELT_NUMBER = Dimensions()
    SURFACE_STANTON_NUMBER = Dimensions()
    SKIN_FRICTION_COEFFICIENT = Dimensions()
    SURFACE_HEAT_TRANSFER_COEFFICIENT = POWER * LENGTH**-2 * TEMPERATURE**-1
    WALL_ADJACENT_HEAT_TRANSFER_COEFFICIENT = POWER * LENGTH**-2 * TEMPERATURE**-1
    WALL_TEMPERATURE = TEMPERATURE
    WALL_ADJACENT_TEMPERATURE = TEMPERATURE
    WALL_TEMPERATURE_THIN = TEMPERATURE
    WALL_SHEAR_STRESS = STRESS

    # Coordinates
    POSITION = LENGTH

    # --- Material Properties ---
    # https://en.wikipedia.org/wiki/List_of_materials_properties

    # Acoustical properties
    ACOUSTICAL_ABSORPTION = Dimensions()  # dimensionless (fraction or dB)
    SPEED_OF_SOUND = VELOCITY
    SOUND_REFLECTION = Dimensions()  # dimensionless (coefficient)
    SOUND_TRANSFER = Dimensions()  # dimensionless (coefficient)
    THIRD_ORDER_ELASTICITY = (
        STRESS  # same as stress (Pa), but higher order tensors in practice
    )

    # Atomic properties
    ATOMIC_MASS = MASS
    ATOMIC_NUMBER = Dimensions()  # dimensionless (count)
    RELATIVE_ATOMIC_MASS = Dimensions()  # dimensionless (ratio)
    STANDARD_ATOMIC_WEIGHT = Dimensions()  # dimensionless (ratio)

    # Chemical properties
    CORROSION_RESISTANCE = Dimensions()  # dimensionless (qualitative)
    HYGROSCOPY = Dimensions()  # dimensionless (qualitative)
    PH = Dimensions()  # dimensionless (logarithmic)
    REACTIVITY = Dimensions()  # dimensionless (qualitative)
    SPECIFIC_INTERNAL_SURFACE_AREA = LENGTH**-1  # m^-1
    SURFACE_ENERGY = ENERGY / AREA  # J/m^2
    SURFACE_TENSION = FORCE / LENGTH  # N/m

    # Electrical properties
    CAPACITANCE = ELECTRICAL_CAPACITANCE  # F = s^4·A^2/(kg·m^2)
    DIELECTRIC_CONSTANT = Dimensions()  # dimensionless (relative permittivity)
    DIELECTRIC_STRENGTH = ELECTRICAL_POTENTIAL / LENGTH  # V/m
    ELECTRICAL_RESISTIVITY = ELECTRICAL_RESISTANCE * LENGTH  # Ω·m
    ELECTRICAL_CONDUCTIVITY = ELECTRICAL_RESISTANCE**-1 / LENGTH  # S/m
    ELECTRIC_SUSCEPTIBILITY = Dimensions()  # dimensionless
    ELECTROCALORIC_COEFFICIENT = TEMPERATURE / ELECTRICAL_POTENTIAL  # K/V
    ELECTROSTRICTION = Dimensions()  # dimensionless (strain per E^2)
    MAGNETOELECTRIC_POLARIZABILITY = ELECTRICAL_POTENTIAL / (
        LENGTH * MAGNETIC_FLUX
    )  # V/(m·Wb)
    NERNST_COEFFICIENT = ELECTRICAL_POTENTIAL / (
        TEMPERATURE * MAGNETIC_INDUCTION
    )  # V/(K·T)
    PERMITTIVITY = ELECTRICAL_CAPACITANCE / LENGTH  # F/m
    PIEZOELECTRIC_CONSTANTS = ELECTRICAL_POTENTIAL / LENGTH / STRESS  # V/(m·Pa)
    PYROELECTRICITY = CURRENT / (AREA * TEMPERATURE)  # A/(m^2·K)
    SEEBECK_COEFFICIENT = ELECTRICAL_POTENTIAL / TEMPERATURE  # V/K

    # Magnetic properties
    CURIE_TEMPERATURE = TEMPERATURE
    DIAMAGNETISM = Dimensions()  # dimensionless (susceptibility)
    HALL_COEFFICIENT = LENGTH**3 / (CURRENT * TIME)  # m^3/(A·s)
    HYSTERESIS = Dimensions()  # dimensionless (qualitative)
    MAGNETOSTRICTION = Dimensions()  # dimensionless (strain)
    MAGNETOCALORIC_COEFFICIENT = TEMPERATURE / MAGNETIC_INDUCTION  # K/T
    MAGNETOTHERMOELECTRIC_POWER = ELECTRICAL_POTENTIAL / (
        TEMPERATURE * MAGNETIC_INDUCTION
    )  # V/(K·T)
    MAGNETORESISTANCE = Dimensions()  # dimensionless (ratio)
    MAXIMUM_ENERGY_PRODUCT = ENERGY / VOLUME  # J/m^3
    PERMEABILITY = MAGNETIC_PERMEABILITY  # H/m
    PIEZOMAGNETISM = MAGNETIC_INDUCTION / STRESS  # T/Pa
    PYROMAGNETIC_COEFFICIENT = MAGNETIC_INDUCTION / TEMPERATURE  # T/K
    SPIN_HALL_EFFECT = ELECTRICAL_RESISTANCE  # Ω (spin Hall angle is dimensionless)

    # Mechanical properties
    BULK_MODULUS = PRESSURE  # Pa
    COEFFICIENT_OF_RESTITUTION = Dimensions()  # dimensionless
    COMPRESSIVE_STRENGTH = STRESS  # Pa
    CREEP = STRAIN_RATE  # 1/s
    DUCTILITY = Dimensions()  # dimensionless (percent elongation)
    DURABILITY = Dimensions()  # dimensionless (qualitative)
    ELASTICITY = Dimensions()  # dimensionless (qualitative)
    FATIGUE_LIMIT = STRESS  # Pa
    FLEXURAL_MODULUS = STRESS  # Pa
    FLEXURAL_STRENGTH = STRESS  # Pa
    FRACTURE_TOUGHNESS = ENERGY / AREA  # J/m^2
    FRICTION_COEFFICIENT = Dimensions()  # dimensionless
    HARDNESS = STRESS  # Pa (approximate)
    MALLEABILITY = Dimensions()  # dimensionless (qualitative)
    MASS_DIFFUSIVITY = AREA / TIME  # m^2/s
    PLASTICITY = Dimensions()  # dimensionless (qualitative)
    POISSON_RATIO = Dimensions()  # dimensionless
    RESILIENCE = STRESS  # Pa (energy per volume)
    SHEAR_MODULUS = STRESS  # Pa
    SHEAR_STRENGTH = STRESS  # Pa
    SLIP = Dimensions()  # dimensionless (qualitative)
    SPECIFIC_MODULUS = STRESS / DENSITY  # m^2/s^2
    SPECIFIC_STRENGTH = ENERGY / MASS  # J/kg
    SPECIFIC_WEIGHT = FORCE / VOLUME  # N/m^3
    SURFACE_ROUGHNESS = LENGTH  # m
    TENSILE_STRENGTH = STRESS  # Pa
    TOUGHNESS = ENERGY / VOLUME  # J/m^3
    VISCOSITY = DYNAMIC_VISCOSITY  # Pa·s
    YIELD_STRENGTH = STRESS  # Pa
    YOUNG_MODULUS = STRESS  # Pa

    # Optical properties
    ABSORBANCE = Dimensions()  # dimensionless (logarithmic)
    BIREFRINGENCE = Dimensions()  # dimensionless (difference in refractive index)
    COLOR = Dimensions()  # dimensionless (qualitative)
    ELECTRO_OPTIC_EFFECT = (
        Dimensions()
    )  # dimensionless (change in refractive index per V/m)
    LUMINOSITY = LUMINOUS_FLUX  # lm
    OPTICAL_ACTIVITY = LENGTH / MASS  # m/g (or rad/(g·cm^2))
    PHOTOELASTICITY = STRESS**-1  # 1/Pa
    PHOTOSENSITIVITY = Dimensions()  # dimensionless (qualitative)
    REFLECTIVITY = Dimensions()  # dimensionless (fraction)
    REFRACTIVE_INDEX = Dimensions()  # dimensionless
    SCATTERING = Dimensions()  # dimensionless (cross-section per volume)
    TRANSMITTANCE = Dimensions()  # dimensionless (fraction)

    # Radiological properties
    ATTENUATION_COEFFICIENT = LENGTH**-1  # m^-1
    HALF_LIFE = TIME  # s
    NEUTRON_CROSS_SECTION = LENGTH**2  # m^2
    SPECIFIC_ACTIVITY = (MASS * TIME) ** -1  # Bq/kg

    # Thermal properties
    EMISSIVITY = Dimensions()  # dimensionless
    HEAT_OF_VAPORIZATION = ENERGY / MASS  # J/kg
    MELTING_POINT = TEMPERATURE  # K
    SPECIFIC_HEAT_CAPACITY = SPECIFIC_HEAT_CAPACITY  # J/(kg·K)
    THERMAL_CONDUCTIVITY = THERMAL_CONDUCTIVITY  # W/(m·K)
    THERMAL_DIFFUSIVITY = AREA / TIME  # m^2/s
    THERMAL_EXPANSION_COEFFICIENT = TEMPERATURE**-1  # 1/K
    VAPOR_PRESSURE = PRESSURE  # Pa

    # List of vector quantities. The only impact
    # of not adding a vector quantity here is that
    # the code will not autogenerate attributes
    # <quantity>_X etc for that quantity.
    _vector_quantities = [
        "VELOCITY",
        "ACCELERATION",
        "VORTICITY",
        "POSITION",
        "MESH_VELOCITY",
        "MOMENTUM",
        "ANGULAR_MOMENTUM",
        "TORQUE",
        "FORCE",
        "WALL_SHEAR_STRESS",
    ]
