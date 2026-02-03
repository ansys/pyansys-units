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

# pyright: reportUnusedExpression=false
import numpy as np
import numpy.typing as npt
from typing_extensions import assert_type

from ansys.units import Quantity, Unit, VariableCatalog
from ansys.units.common import kg, m
from ansys.units.variable_descriptor import (
    ScalarVariableDescriptor,
    VectorVariableDescriptor,
)

assert_type(kg, Unit)
assert_type(Quantity([1, 2, 3], "m"), Quantity[npt.NDArray[np.floating]])

assert_type(1 * m, Quantity[float])
assert_type(1.0 * m, Quantity[float])

assert_type(1 * m + 2 * m, Quantity[float])
assert_type(1 * m - 2 * m, Quantity[float])
1 * m + 2  # pyright: ignore[reportOperatorIssue]

assert_type([1, 2, 3] * m, Quantity[npt.NDArray[np.floating]])
assert_type([1.0, 2.0, 3.0] * m, Quantity[npt.NDArray[np.floating]])

assert_type(1.225 * kg / m**3, Quantity[float])
assert_type(1.225 * kg / m**3 * [1, 2, 3] * m, Quantity[npt.NDArray[np.floating]])

assert_type(VariableCatalog.ABSOLUTE_PRESSURE, ScalarVariableDescriptor)
assert_type(VariableCatalog.VELOCITY, VectorVariableDescriptor)
