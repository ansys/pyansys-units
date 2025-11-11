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
# This file is @generated

from typing import Literal

UnitKey = Literal[
    "kg",
    "g",
    "lb",
    "lbm",
    "slug",
    "m",
    "cm",
    "ft",
    "inch",
    "in",
    "s",
    "A",
    "mol",
    "slugmol",
    "cd",
    "sr",
    "radian",
    "degree",
    "K",
    "C",
    "F",
    "R",
    "delta_K",
    "delta_C",
    "delta_F",
    "delta_R",
    "N",
    "Pa",
    "W",
    "J",
    "V",
    "farad",
    "H",
    "S",
    "Wb",
    "T",
    "dyne",
    "erg",
    "h",
    "pdl",
    "psi",
    "lbf",
    "psf",
    "ohm",
    "Hz",
    "l",
    "gal",
    "BTU",
    "cal",
    "coulomb",
]

MassKey = Literal[
    "kg",
    "g",
    "lb",
    "lbm",
    "slug",
]

LengthKey = Literal[
    "m",
    "cm",
    "ft",
    "inch",
    "in",
]

TimeKey = Literal["s",]

CurrentKey = Literal["A",]

ChemicalAmountKey = Literal[
    "mol",
    "slugmol",
]

LightKey = Literal["cd",]

SolidAngleKey = Literal["sr",]

AngleKey = Literal[
    "radian",
    "degree",
]

TemperatureKey = Literal[
    "K",
    "C",
    "F",
    "R",
]

TemperatureDifferenceKey = Literal[
    "delta_K",
    "delta_C",
    "delta_F",
    "delta_R",
]

QuantityKey = Literal[
    "Mass",
    "Length",
    "Time",
    "Temperature",
    "Current",
    "SubstanceAmount",
    "Light",
    "Angle",
    "SolidAngle",
    "Acceleration",
    "AngularAcceleration",
    "AngularVelocity",
    "Area",
    "Compressibility",
    "Concentration",
    "DecayConstant",
    "Density",
    "DynamicViscosity",
    "ElectricCharge",
    "ElectricChargeDensity",
    "ElectricCurrentDensity",
    "ElectricCurrentSource",
    "ElectricFluxDensity",
    "Enthalpy",
    "Force",
    "ForceDensity",
    "Frequency",
    "HeatFlux",
    "HeatGeneration",
    "HeatTransferCoefficient",
    "Impulse",
    "MagneticFieldIntensity",
    "MassFlowRate",
    "MassFlux",
    "MolarConcentration",
    "MolarEnergy",
    "MolarEnthalpy",
    "MolarEntropy",
    "MolarMass",
    "MolarVolume",
    "Moment",
    "MomentOfInertiaOfArea",
    "MomentOfInertiaOfMass",
    "Momentum",
    "Pressure",
    "ShearStrain",
    "ShearStrainRate",
    "SpecificConcentration",
    "SpecificEnergy",
    "SpecificEnthalpy",
    "SpecificEntropy",
    "SpecificFlameSurfaceDensity",
    "SpecificHeatCapacity",
    "SpecificVolume",
    "Stiffness",
    "Strain",
    "SurfaceChargeDensity",
    "SurfaceForceDensity",
    "SurfacePowerDensity",
    "SurfaceTension",
    "TemperatureGradient",
    "ThermalCapacitance",
    "ThermalConductance",
    "ThermalConductivity",
    "ThermalContactResistance",
    "ThermalExpansionCoefficient",
    "Torque",
    "Velocity",
    "Volume",
    "VolumetricFlowRate",
]

BaseUnit = Literal[
    "MASS",
    "LENGTH",
    "TIME",
    "TEMPERATURE",
    "TEMPERATURE_DIFFERENCE",
    "ANGLE",
    "CHEMICAL_AMOUNT",
    "LIGHT",
    "CURRENT",
    "SOLID_ANGLE",
]

Systems = Literal[
    "SI",
    "CGS",
    "BT",
]
