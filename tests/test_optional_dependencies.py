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
"""
Tests for behaviour when optional dependencies or package metadata are missing.

Each test executes a fresh copy of a real module file under a private name while
selected imports are blocked. The real, already imported modules are unaffected.
"""

import builtins
import importlib.metadata
import importlib.util
import io
import os
import sys
from types import ModuleType

import pytest

import ansys.units
import ansys.units.quantity


def _load_copy(module: ModuleType, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, module.__file__)
    copy = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(copy)
    return copy


@pytest.fixture
def quantity_without_optional_dependencies(monkeypatch):
    for blocked in ("numpy", "pydantic_core", "matplotlib.units"):
        monkeypatch.setitem(sys.modules, blocked, None)
    return _load_copy(ansys.units.quantity, "_quantity_without_optional_deps")


def test_quantity_without_numpy(quantity_without_optional_dependencies):
    module = quantity_without_optional_dependencies
    assert module._array is None

    # Scalars work without NumPy.
    q = module.Quantity(2.0, "m")
    assert module.get_si_value(q) == 2.0

    # Lists and arrays require NumPy.
    with pytest.raises(module.NumPyRequired, match="install NumPy"):
        module.Quantity([1.0, 2.0], "m")

    # A non-float value can't be converted to SI without NumPy.
    q._value = [1.0]
    with pytest.raises(ValueError, match="numpy"):
        module.get_si_value(q)


def test_quantity_without_pydantic(quantity_without_optional_dependencies):
    module = quantity_without_optional_dependencies
    assert module._core_schema is None
    with pytest.raises(module.PydanticRequired, match="pip install"):
        module.Quantity.__get_pydantic_core_schema__(module.Quantity, None)


def test_quantity_without_matplotlib(quantity_without_optional_dependencies):
    module = quantity_without_optional_dependencies
    assert module._ai is None
    assert module._ci is object
    # The converter is kept in a local registry instead of Matplotlib's.
    assert list(module._registry) == [module.Quantity]


def test_package_init_fallbacks(monkeypatch):
    """Missing metadata, a bundled README, and a missing pandas extension."""

    def missing_version(name):
        raise importlib.metadata.PackageNotFoundError(name)

    readme = os.path.normpath(
        os.path.join(os.path.dirname(ansys.units.__file__), "docs", "README.rst")
    )
    real_exists, real_open = os.path.exists, builtins.open

    def fake_exists(path):
        return True if os.path.normpath(path) == readme else real_exists(path)

    def fake_open(path, *args, **kwargs):
        if isinstance(path, str) and os.path.normpath(path) == readme:
            return io.StringIO("Bundled README")
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr(importlib.metadata, "version", missing_version)
    monkeypatch.setattr(os.path, "exists", fake_exists)
    monkeypatch.setattr(builtins, "open", fake_open)
    monkeypatch.setitem(sys.modules, "ansys.units.extensions.pandas_extension", None)

    package = _load_copy(ansys.units, "_ansys_units_init_copy")

    assert package.__version__ == "script-running"
    assert package.__doc__ == "Bundled README"
    assert "QuantityArray" not in package.__all__
    assert "Quantity" in package.__all__
