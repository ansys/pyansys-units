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
from ansys.units import QuantityDescriptor, QuantityDescriptorCatalog, MappingConversionStrategy


def test_create_descriptors():
    vel = QuantityDescriptor("velocity", None, None)
    assert vel.name == "velocity"

def test_descriptor_strategies():
    
    class JapaneseAPIStrategy(MappingConversionStrategy):
        _mapping = {
            QuantityDescriptorCatalog.PRESSURE: "atsuryoku",
            QuantityDescriptorCatalog.TEMPERATURE: "ondo",
        }

    assert JapaneseAPIStrategy().to_string(QuantityDescriptorCatalog.PRESSURE) == "atsuryoku"
    assert JapaneseAPIStrategy().to_string(QuantityDescriptorCatalog.TEMPERATURE) == "ondo"

    with pytest.raises(ValueError):
        JapaneseAPIStrategy().to_string(QuantityDescriptorCatalog.VELOCITY_X)
        
    assert JapaneseAPIStrategy().to_quantity("atsuryoku") == QuantityDescriptorCatalog.PRESSURE
    assert JapaneseAPIStrategy().to_quantity("ondo") == QuantityDescriptorCatalog.TEMPERATURE

    assert JapaneseAPIStrategy().to_quantity("x-houkou-no-sokudo") is None

def test_extend_descriptor_catalog():
    catalog = QuantityDescriptorCatalog()
    setattr(catalog, "FORCE", QuantityDescriptor("force", None, "N"))
    assert catalog.FORCE.name == "force"
