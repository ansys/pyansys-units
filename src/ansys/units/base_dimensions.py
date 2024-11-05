# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
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
Provides the ``BaseDimensions`` class.

Supplies all valid base dimensions used in dimensional analysis.

Used as dictionary keys for defining a `Dimensions` object.
"""

from enum import Enum
import os

_base_dims = {
    "MASS": 0,
    "LENGTH": 1,
    "TIME": 2,
    "TEMPERATURE": 3,
    "TEMPERATURE_DIFFERENCE": 4,
    "CHEMICAL_AMOUNT": 5,
    "LIGHT": 6,
    "CURRENT": 7,
}

_base_dims_with_angle = {
    "MASS": 0,
    "LENGTH": 1,
    "TIME": 2,
    "TEMPERATURE": 3,
    "TEMPERATURE_DIFFERENCE": 4,
    "CHEMICAL_AMOUNT": 5,
    "LIGHT": 6,
    "CURRENT": 7,
    "ANGLE": 8,
    "SOLID_ANGLE": 9,
}

BaseDimensions = Enum(
    "BaseDimensions",
    (
        _base_dims_with_angle
        if os.getenv("PYANSYS_UNITS_ANGLE_AS_DIMENSION")
        else _base_dims
    ),
)
