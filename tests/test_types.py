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
from ansys.units.unit import IncorrectUnits
from ansys.units.variable_descriptor import (
    ScalarVariableDescriptor,
    VectorVariableDescriptor,
)

assert_type(kg, Unit)
assert_type(Quantity([1, 2, 3], "m"), Quantity[npt.NDArray[np.floating]])
assert_type(Quantity(1, "kg") * 1, Quantity[float])
assert_type(Quantity(1, "kg") / 1, Quantity[float])
assert_type(1 / Quantity(1, "kg"), Quantity[float])
assert_type(1 * Quantity(1, "kg"), Quantity[float])

assert_type(1 * m, Quantity[float])
assert_type(1.0 * m, Quantity[float])

assert_type(1 * m + 2 * m, Quantity[float])
assert_type(1 * m - 2 * m, Quantity[float])

q_scalar_a = Quantity(1.0, "m")
q_scalar_b = Quantity(2.0, "m")
assert_type(q_scalar_a.__radd__(q_scalar_b), Quantity[float])
assert_type(q_scalar_a - (q_scalar_b), Quantity[float])
assert_type(q_scalar_a.__rsub__(q_scalar_b), Quantity[float])

q_vec_a = Quantity([1.0, 2.0, 3.0], "m")
q_vec_b = Quantity([4.0, 5.0, 6.0], "m")
assert_type(q_vec_a.__radd__(q_vec_b), Quantity[npt.NDArray[np.floating]])
assert_type(q_vec_a - (q_vec_b), Quantity[npt.NDArray[np.floating]])
assert_type(q_vec_a.__rsub__(q_vec_b), Quantity[npt.NDArray[np.floating]])

try:
    1 * m + 2  # pyright: ignore[reportOperatorIssue]
    2 + 1 * m  # pyright: ignore[reportOperatorIssue]
    1 * m - 2  # pyright: ignore[reportOperatorIssue]
    2 - 1 * m  # pyright: ignore[reportOperatorIssue]
    [1] * m + [2]  # pyright: ignore[reportOperatorIssue]
    [2] + [1] * m  # pyright: ignore[reportOperatorIssue]
    [1] * m - [2]  # pyright: ignore[reportOperatorIssue]
    [2] - [1] * m  # pyright: ignore[reportOperatorIssue]
except IncorrectUnits:
    pass

assert_type([1, 2, 3] * m, Quantity[npt.NDArray[np.floating]])
assert_type([1.0, 2.0, 3.0] * m, Quantity[npt.NDArray[np.floating]])

assert_type(1.225 * kg / m**3, Quantity[float])
assert_type(1.225 * kg / m**3 * [1, 2, 3] * m, Quantity[npt.NDArray[np.floating]])

assert_type(VariableCatalog.ABSOLUTE_PRESSURE, ScalarVariableDescriptor)
assert_type(VariableCatalog.VELOCITY, VectorVariableDescriptor)
