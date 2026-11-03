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

from typing import final

import pytest

from ansys.units import (
    Dimensions,
    MappingConversionStrategy,
    QuantityDimensions,
    VariableCatalog,
    VariableDescriptor,
)


def test_create_descriptors():
    @final
    class _:
        VELOCITY = VariableDescriptor(Dimensions())

    assert _.VELOCITY.name == "velocity"


def test_descriptor_strategies():
    @final
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
    # ignore this is acceptable as most users shouldn't really be dynamically adding these,
    # it's far better to subclass
    assert (
        catalog.WALL_SHEAR_STRESS_2.name  # pyright: ignore[reportAttributeAccessIssue]
        == "wall_shear_stress_2"
    )


def test_get_custom_descriptor_from_catalog():
    catalog = VariableCatalog()
    assert catalog.VELOCITY_Y.name == "velocity_y"


@pytest.mark.parametrize(
    "name",
    [
        "HELICITY",
        "LAMBDA_2_CRITERION",
        "TOTAL_ENTHALPY_DEVIATION",
        "MASS_IMBALANCE",
        "VELOCITY_ANGLE",
        "DVELOCITY_DX",
        "VOLUME_FRACTION_PRIMARY_PHASE",
        "VOLUME_FRACTION_SECONDARY_PHASE",
    ],
)
def test_cfd_variables_moved_to_main_namespace(name: str):
    descriptor = getattr(VariableCatalog, name)
    assert isinstance(descriptor, VariableDescriptor)
    assert descriptor.name == name.lower()


@pytest.mark.parametrize(
    "name",
    [
        "DENSITY_ALL",
        "Y_PLUS_BASED_HEAT_TRANSFER_COEFFICIENT",
        "PRESSURE_HESSIAN_INDICATOR",
    ],
)
def test_removed_fluent_variables_absent(name: str):
    assert not hasattr(VariableCatalog, name)


@pytest.mark.parametrize(
    "name",
    [
        "MESH_CELL_VOLUME",
        "MESH_ELEMENT_WALL_DISTANCE",
        "MESH_FACE_AREA_MAGNITUDE",
        "MESH_STORED_CELL_PARTITION",
    ],
)
def test_mesh_variables_moved_to_main_namespace(name: str):
    descriptor = getattr(VariableCatalog, name)
    assert isinstance(descriptor, VariableDescriptor)
    assert descriptor.name == name.lower()
