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

import pytest

from ansys.units import (
    MappingConversionStrategy,
    QuantityDimensions,
    VariableCatalog,
    VariableDescriptor,
)


def test_create_descriptors():
    vel = VariableDescriptor("velocity", None)
    assert vel.name == "velocity"


def test_descriptor_strategies():

    class JapaneseAPIStrategy(MappingConversionStrategy):
        _mapping = {
            VariableCatalog.PRESSURE: "atsuryoku",
            VariableCatalog.TEMPERATURE: "ondo",
        }

    assert JapaneseAPIStrategy().to_string(VariableCatalog.PRESSURE) == "atsuryoku"
    assert JapaneseAPIStrategy().to_string(VariableCatalog.TEMPERATURE) == "ondo"

    with pytest.raises(ValueError):
        JapaneseAPIStrategy().to_string(VariableCatalog.VELOCITY_X)

    assert (
        JapaneseAPIStrategy().to_variable_descriptor("atsuryoku")
        == VariableCatalog.PRESSURE
    )
    assert (
        JapaneseAPIStrategy().to_variable_descriptor("ondo")
        == VariableCatalog.TEMPERATURE
    )

    assert JapaneseAPIStrategy().to_variable_descriptor("x-houkou-no-sokudo") is None


def test_extend_descriptor_catalog():
    catalog = VariableCatalog()
    catalog.add("WALL_SHEAR_STRESS_2", QuantityDimensions.STRESS)
    assert catalog.WALL_SHEAR_STRESS_2.name == "wall_shear_stress_2"


def test_get_custom_descriptor_from_catalog():
    catalog = VariableCatalog()
    assert catalog.VELOCITY_Y.name == "velocity_y"
