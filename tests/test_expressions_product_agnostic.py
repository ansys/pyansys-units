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

"""
Guard: ``ansys.expressions`` must stay product-agnostic.

It may only depend on the lower layers of this distribution and must not mention any
product; product-specific behavior is supplied through a ``Dialect``.
"""

import ast
from pathlib import Path

import pytest

import ansys.expressions

_SOURCES = sorted(Path(ansys.expressions.__file__).parent.glob("*.py"))
_ALLOWED = ("ansys.units", "ansys.variable_descriptor")


def _absolute_imports(tree: ast.AST) -> list[str]:
    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.level == 0:
            modules.append(node.module or "")
        elif isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
    return modules


@pytest.mark.parametrize("source", _SOURCES, ids=lambda p: p.name)
def test_only_lower_layers_are_imported(source: Path):
    tree = ast.parse(source.read_text(encoding="utf-8"))
    for module in _absolute_imports(tree):
        if module.startswith("ansys"):
            assert module.startswith(_ALLOWED), f"{source.name} imports {module}"


@pytest.mark.parametrize("source", _SOURCES, ids=lambda p: p.name)
def test_no_product_names(source: Path):
    assert "fluent" not in source.read_text(encoding="utf-8").lower()
