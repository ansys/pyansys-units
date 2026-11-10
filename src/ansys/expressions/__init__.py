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
Product-agnostic, unit-aware expression trees.

This package may depend on :mod:`ansys.variable_descriptor` and :mod:`ansys.units`, but
neither of those packages may depend on it, and it must not depend on any product.
Product-specific details (variable names and the available functions) are supplied
through a :class:`Dialect`.

The package is organized in layers:

* :mod:`._ast` -- typed, immutable expression tree.
* :mod:`._registry` -- declarative function signatures and registries.
* :mod:`._dialect` -- product-specific naming and functions.
* :mod:`._parser` -- expression string to tree.
* :mod:`._discovery` / :mod:`._slots` -- legal values for builder parameters.
* :mod:`.builder` -- user-facing, discoverable facade.

Example
-------

.. code-block:: python

    from ansys.expressions import (
        Dialect,
        ExpressionBuilder,
        FunctionRegistry,
        Kind,
        Param,
        Signature,
    )
    from ansys.variable_descriptor import VariableCatalog as V

    functions = FunctionRegistry()
    functions.register(
        "reductions",
        Signature(
            "AreaAve",
            "area_ave",
            (Param("expression", Kind.SCALAR), Param("locations", Kind.LOCATION_LIST)),
        ),
    )
    builder = ExpressionBuilder(Dialect("my_product", functions=functions))

    expr = builder.reductions.area_ave(V.ABSOLUTE_PRESSURE, ["inlet"]) * 2
    str(expr)  # "(AreaAve(absolute_pressure,['inlet']) * 2)"
"""

from ansys.units import __version__ as __version__

from ._ast import (
    BinOp,
    BooleanExpr,
    Call,
    Compare,
    Expr,
    KeywordArg,
    Kind,
    Literal,
    LocationList,
    Operand,
    Quantity,
    RawName,
    RenderDialect,
    ScalarExpr,
    UnaryOp,
    Variable,
    VectorExpr,
    common_dialect,
)
from ._dialect import DEFAULT_DIALECT, DescriptorNameStrategy, Dialect
from ._discovery import Discovery, StaticDiscovery
from ._parser import parse
from ._registry import FunctionRegistry, Param, Signature, make_call
from ._slots import LocationSlot, ScalarSlot, SlotAccessor
from .builder import ExpressionBuilder, FunctionGroup, FunctionInvoker
from .errors import ExpressionBuildError

__all__ = [
    "BinOp",
    "BooleanExpr",
    "Call",
    "Compare",
    "DEFAULT_DIALECT",
    "DescriptorNameStrategy",
    "Dialect",
    "Discovery",
    "Expr",
    "ExpressionBuildError",
    "ExpressionBuilder",
    "FunctionGroup",
    "FunctionInvoker",
    "FunctionRegistry",
    "KeywordArg",
    "Kind",
    "Literal",
    "LocationList",
    "LocationSlot",
    "Operand",
    "Param",
    "Quantity",
    "RawName",
    "RenderDialect",
    "ScalarExpr",
    "ScalarSlot",
    "Signature",
    "SlotAccessor",
    "StaticDiscovery",
    "UnaryOp",
    "Variable",
    "VectorExpr",
    "common_dialect",
    "make_call",
    "parse",
]
