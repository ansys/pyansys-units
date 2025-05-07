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
    FORCE = MASS * LENGTH / TIME ** 2
    FREQUENCY = TIME ** -1

    # Electromagnetics

    ELECTRIC_CHARGE = TIME * CURRENT
    ELECTRICAL_POTENTIAL = MASS * AREA * TIME ** -3 / CURRENT
    ELECTRICAL_CAPACITANCE = MASS ** -1 * LENGTH ** -2 * TIME ** 4 * CURRENT ** 2
    ELECTRICAL_INDUCTANCE = MASS * LENGTH ** 2 * TIME ** -2 * CURRENT ** -2
    ELECTRICAL_RESISTANCE = ELECTRICAL_POTENTIAL / CURRENT
    ELECTRICAL_IMPEDANCE = ELECTRICAL_RESISTANCE
    ELECTRICAL_REACTANCE = ELECTRICAL_RESISTANCE
    ELECTRICAL_CONDUCTANCE = ELECTRICAL_RESISTANCE ** -1


