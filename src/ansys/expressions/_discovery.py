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
Discovery: what values are legal in the current context.

The builder's per-parameter slots (see :mod:`._slots`) ask a :class:`Discovery` object
which locations, named expressions, and variables are available. Products implement this
protocol on top of their own data sources (for example a live session).
:class:`StaticDiscovery` is used when there is no data source: it is permissive and
driven by the dialect.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from ansys.variable_descriptor import VariableDescriptor

from ._dialect import Dialect


@runtime_checkable
class Discovery(Protocol):
    """Answers which values are legal in the current context."""

    def location_names(self) -> list[str]:
        """Return the available location names (surfaces, zones, ...)."""
        ...

    def named_expression_names(self) -> list[str]:
        """Return the names of named expressions that are in scope."""
        ...

    def variable_descriptors(self) -> list[VariableDescriptor]:
        """Return the variable descriptors available in the current context."""
        ...

    def is_variable_supported(self, descriptor: VariableDescriptor) -> bool:
        """Return ``True`` if ``descriptor`` is usable in the current context."""
        ...


class StaticDiscovery:
    """
    Discovery without a live data source.

    Parameters
    ----------
    dialect :
        Dialect that determines which variables are supported.
    locations :
        Known location names. Empty means "unknown", which slots treat
        permissively.
    named_expressions :
        Known named-expression names. Empty means "unknown".
    """

    _dialect: Dialect
    _locations: list[str]
    _named_expressions: list[str]

    def __init__(
        self,
        dialect: Dialect,
        locations: Sequence[str] = (),
        named_expressions: Sequence[str] = (),
    ) -> None:
        self._dialect = dialect
        self._locations = list(locations)
        self._named_expressions = list(named_expressions)

    def location_names(self) -> list[str]:
        """Return the known location names."""
        return list(self._locations)

    def named_expression_names(self) -> list[str]:
        """Return the known named-expression names."""
        return list(self._named_expressions)

    def variable_descriptors(self) -> list[VariableDescriptor]:
        """Return every descriptor the dialect supports."""
        return self._dialect.supported_variables()

    def is_variable_supported(self, descriptor: VariableDescriptor) -> bool:
        """Return ``True`` if the dialect can render ``descriptor``."""
        return self._dialect.supports_variable(descriptor)
