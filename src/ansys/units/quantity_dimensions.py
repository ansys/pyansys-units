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
from ansys.units.dimensions import Dimensions
from ansys.units.quantity_dimensions import QuantityDimensions

force = QuantityDimensions.FORCE
pressure = QuantityDimensions.PRESSURE
pressure == force / QuantityDimensions.AREA
True
"""

from ansys.units.base_dimensions import BaseDimensions
from ansys.units.dimensions import Dimensions

# Local function to convert from a `BaseDimensions` enum object to a `Dimensions` object


def _make_base_dimensions(dimension: BaseDimensions) -> Dimensions:
    return Dimensions(dimensions={dimension: 1.0})


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
