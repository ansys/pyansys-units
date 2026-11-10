# Copyright (C) 2023 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

import importlib
import importlib.metadata

import pytest

from ansys.units import __version__


def test_pkg_version():
    # Read from the pyproject.toml
    # major, minor, patch
    read_version = importlib.metadata.version("ansys-units")

    assert __version__ == read_version


@pytest.mark.parametrize(
    "package", ["ansys.units", "ansys.variable_descriptor", "ansys.expressions"]
)
def test_top_level_packages_share_distribution_version(package: str):
    module = importlib.import_module(package)
    assert module.__version__ == importlib.metadata.version("ansys-units")


def test_units_does_not_expose_higher_layers():
    import ansys.units

    for name in (
        "VariableCatalog",
        "VariableDescriptor",
        "ConversionStrategy",
        "MappingConversionStrategy",
        "variable_descriptor",
    ):
        assert not hasattr(ansys.units, name)
