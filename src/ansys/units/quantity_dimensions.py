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

from ansys.units.base_dimensions import BaseDimensions
from ansys.units.dimensions import Dimensions

# Local function to convert from a `BaseDimensions` enum object to a `Dimensions` object

def _make_base_dimensions(dimension: BaseDimensions) -> Dimensions:
    return Dimensions(dimensions={dimension: 1.0})

class QuantityDimensions:

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
    TEMPERATURE_DIFFERENCE = _make_base_dimensions(BaseDimensions.TEMPERATURE_DIFFERENCE)

    # Dimensions of derived quantities
    AREA = LENGTH ** 2
    VOLUME = LENGTH ** 3
    FREQUENCY = TIME ** -1

    # Kinematics and mechanics
    VELOCITY = LENGTH / TIME
    ACCELERATION = VELOCITY / TIME
    FORCE = MASS * ACCELERATION
    PRESSURE = FORCE / AREA
    STRESS = PRESSURE
    JERK = LENGTH / TIME ** 3
    SNAP = LENGTH / TIME ** 4
    ANGULAR_VELOCITY = TIME ** -1
    ANGULAR_ACCELERATION = TIME ** -2
    VOLUMETRIC_FLOW = VOLUME / TIME
    MOMENTUM = MASS * VELOCITY
    ANGULAR_MOMENTUM = LENGTH ** 2 * MASS / TIME
    TORQUE = LENGTH ** 2 * MASS / TIME ** 2
    ENERGY = LENGTH ** 2 * MASS / TIME ** 2
    POWER = ENERGY / TIME
    DENSITY = MASS / VOLUME
    SPECIFIC_VOLUME = VOLUME / MASS
    ENERGY_DENSITY = ENERGY / VOLUME
    SURFACE_TENSION = FORCE / LENGTH
    KINEMATIC_VISCOSITY = AREA / TIME
    DYNAMIC_VISCOSITY = PRESSURE * TIME
    MASS_FLOW_RATE = MASS / TIME
    MASS_CONTROL = MASS / TIME ** 3  # kg⋅m/s^3
    ANGULAR_VELOCITY = TIME ** -1  # rad/s
    ANGULAR_ACCELERATION = TIME ** -2  # rad/s^2
    FREQUENCY_DRIFT = TIME ** -2  # Hz/s
    VOLUMETRIC_FLOW = VOLUME / TIME  # m^3/s
    YANK = FORCE / TIME  # N/s = m⋅kg⋅s^-3
    WAVENUMBER = LENGTH ** -1  # m^-1
    AREA_DENSITY = MASS / AREA  # kg/m^2
    DENSITY = MASS / VOLUME  # kg/m^3
    SPECIFIC_VOLUME = VOLUME / MASS  # m^3/kg
    ACTION = ENERGY * TIME  # J⋅s = m^2⋅kg⋅s^-1
    SPECIFIC_ENERGY = ENERGY / MASS  # J/kg = m^2⋅s^-2
    ENERGY_DENSITY = ENERGY / VOLUME  # J/m^3 = m^-1⋅kg⋅s^-2
    SURFACE_TENSION = FORCE / LENGTH  # N/m = kg⋅s^-2
    HEAT_FLUX_DENSITY = POWER / AREA  # W/m^2 = kg⋅s^-3
    KINEMATIC_VISCOSITY = AREA / TIME  # m^2/s
    DYNAMIC_VISCOSITY = PRESSURE * TIME  # Pa⋅s = m^-1⋅kg⋅s^-1
    LINEAR_MASS_DENSITY = MASS / LENGTH  # kg/m
    MASS_FLOW_RATE = MASS / TIME  # kg/s
    RADIANCE = POWER / (SOLID_ANGLE * AREA)  # W/(sr⋅m^2) = kg⋅s^-3
    SPECTRAL_POWER = POWER / LENGTH  # W/m = m⋅kg⋅s^-3
    ABSORBED_DOSE_RATE = AREA / TIME ** 3  # Gy/s = m^2⋅s^-3
    FUEL_EFFICIENCY = LENGTH ** -2  # m^-2
    SPECTRAL_IRRADIANCE = POWER / VOLUME  # W/m^3 = m^-1⋅kg⋅s^-3
    ENERGY_FLUX_DENSITY = ENERGY / (AREA * TIME)  # J/(m^2⋅s) = kg⋅s^-3
    COMPRESSIBILITY = PRESSURE ** -1  # Pa^-1 = m⋅kg^-1⋅s^2
    RADIANT_EXPOSURE = ENERGY / AREA  # J/m^2 = kg⋅s^-2
    MOMENT_OF_INERTIA = MASS * AREA  # kg⋅m^2
    SPECIFIC_ANGULAR_MOMENTUM = ANGULAR_MOMENTUM / MASS  # N⋅m⋅s/kg = m^2⋅s^-1
    RADIANT_INTENSITY = POWER / SOLID_ANGLE  # W/sr = m^2⋅kg⋅s^-3
    SPECTRAL_INTENSITY = POWER / (SOLID_ANGLE * LENGTH)  # W/(sr⋅m) = m⋅kg⋅s^-3



    # Electromagnetics
    ELECTRIC_CHARGE = TIME * CURRENT
    ELECTRICAL_POTENTIAL = MASS * AREA * TIME ** -3 / CURRENT
    ELECTRICAL_CAPACITANCE = MASS ** -1 * LENGTH ** -2 * TIME ** 4 * CURRENT ** 2
    ELECTRICAL_INDUCTANCE = MASS * LENGTH ** 2 * TIME ** -2 * CURRENT ** -2
    ELECTRICAL_RESISTANCE = ELECTRICAL_POTENTIAL / CURRENT
    ELECTRICAL_IMPEDANCE = ELECTRICAL_RESISTANCE
    ELECTRICAL_REACTANCE = ELECTRICAL_RESISTANCE
    ELECTRICAL_CONDUCTANCE = ELECTRICAL_RESISTANCE ** -1
    MAGNETIC_FLUX = MASS * LENGTH ** 2 * TIME ** -2 * CURRENT ** -1
    MAGNETIC_INDUCTION = MASS * TIME ** -2 * CURRENT ** -1
    MAGNETIC_PERMEABILITY = LENGTH * MASS * TIME ** -2 * CURRENT ** -2
    MAGNETIC_VECTOR_POTENTIAL = LENGTH * MASS * TIME ** -2 * CURRENT ** -1

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
