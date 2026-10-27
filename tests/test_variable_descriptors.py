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

from typing import Any, final

import pytest
from typing_extensions import override

from ansys.units import (
    ConversionStrategy,
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


def test_catalog_all_groups_descriptors_by_subcategory():
    groups = VariableCatalog.all()
    assert VariableCatalog.PRESSURE in groups["main"]
    assert set(groups) >= {"main", "fluent", "mesh"}
    assert all(isinstance(d, VariableDescriptor) for d in groups["fluent"])


def test_catalog_add_to_new_subcategory():
    VariableCatalog.add("TEST_ONLY_SPEED", QuantityDimensions.VELOCITY, "test_only")
    try:
        assert VariableCatalog.test_only.TEST_ONLY_SPEED.name == "test_only_speed"
        assert VariableCatalog.test_only.__doc__.startswith("Dictionary")
        assert "test_only" in VariableCatalog.all()

        with pytest.raises(ValueError, match="already exists in the 'test_only'"):
            VariableCatalog.add(
                "TEST_ONLY_SPEED", QuantityDimensions.VELOCITY, "test_only"
            )
    finally:
        delattr(VariableCatalog, "test_only")


def test_catalog_add_validates_name():
    with pytest.raises(ValueError, match="uppercase"):
        VariableCatalog.add("lowercase_name", QuantityDimensions.VELOCITY)
    with pytest.raises(ValueError, match="already exists in the 'main'"):
        VariableCatalog.add("PRESSURE", QuantityDimensions.PRESSURE)


def test_mapping_strategy_passes_through_matching_types():
    @final
    class Strategy(MappingConversionStrategy):
        _mapping = {VariableCatalog.PRESSURE: "p"}

    strategy = Strategy()
    assert strategy.to_string("already a string") == "already a string"
    assert strategy.to_string(None) is None
    assert (
        strategy.to_variable_descriptor(VariableCatalog.PRESSURE)
        is VariableCatalog.PRESSURE
    )


def test_conversion_strategy_is_abstract():
    with pytest.raises(TypeError):
        ConversionStrategy()

    @final
    class Delegating(ConversionStrategy):
        """Strategy that calls the abstract base implementations."""

        @override
        def to_string(self, variable: Any) -> Any:
            return super().to_string(variable)

        @override
        def to_variable_descriptor(self, variable: Any) -> Any:
            return super().to_variable_descriptor(variable)

        @override
        def supports(self, variable: Any) -> Any:
            return super().supports(variable)

    strategy = Delegating()
    assert strategy.to_string(VariableCatalog.PRESSURE) is None
    assert strategy.to_variable_descriptor("p") is None
    assert strategy.supports(VariableCatalog.PRESSURE) is None
