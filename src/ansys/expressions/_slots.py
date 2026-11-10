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

"""Per-parameter slot accessors.

For a registered signature ``area_ave(expression, locations)``, users can
introspect what values are legal for each slot *before* filling it::

    inv = builder.reductions.area_ave
    inv.expression.variables.allowed_values()   # catalog entries
    inv.expression.named.allowed_values()       # in-scope named exprs
    inv.locations.allowed_values()              # location names
    inv.locations.is_allowed("inlet1")

Each :class:`SlotAccessor` is created by the builder based on the
:class:`~._registry.Param`'s kind.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import cast

from typing_extensions import override

from ansys.variable_descriptor import VariableDescriptor

from ._ast import Kind
from ._discovery import Discovery
from ._registry import Param


class SlotAccessor:
    """Base class for per-slot discovery helpers."""

    _param: Param
    _discovery: Discovery

    def __init__(self, param: Param, discovery: Discovery) -> None:
        self._param = param
        self._discovery = discovery

    @property
    def name(self) -> str:
        """Name of the parameter this slot represents."""
        return self._param.name

    @property
    def kind(self) -> Kind:
        """Expected :class:`~._ast.Kind` for this slot."""
        return self._param.kind

    def allowed_values(self) -> list[object]:  # pragma: no cover - abstract
        """Return the list of values permitted for this slot."""
        raise NotImplementedError

    def is_allowed(self, value: object) -> bool:
        """Return ``True`` if ``value`` is a permitted value for this slot."""
        return value in self.allowed_values()

    @override
    def __repr__(self) -> str:
        return f"<slot {self.name!r}: {self.kind.value}>"


# --------------------------------------------------------------------------- #
# Location slot                                                               #
# --------------------------------------------------------------------------- #


class LocationSlot(SlotAccessor):
    """Accessor for a :attr:`Kind.LOCATION_LIST` parameter."""

    @override
    def allowed_values(self) -> list[object]:
        """Return the available location names."""
        return list(self._discovery.location_names())

    @override
    def is_allowed(self, value: object) -> bool:
        """
        Return ``True`` if ``value`` names available locations.

        When no location names are known, any string (or list of strings) is accepted.
        """
        names = self._discovery.location_names()
        if isinstance(value, str):
            return not names or value in names
        if isinstance(value, (list, tuple)):
            items = cast(Sequence[object], value)
            return all(isinstance(v, str) and (not names or v in names) for v in items)
        return False


# --------------------------------------------------------------------------- #
# Scalar-expression slot                                                      #
# --------------------------------------------------------------------------- #


class _VariablesSubSlot:
    """Sub-namespace: catalog variables accepted by the scalar slot."""

    _discovery: Discovery

    def __init__(self, discovery: Discovery) -> None:
        self._discovery = discovery

    def allowed_values(self) -> list[VariableDescriptor]:
        """Return the variable descriptors available in the current context."""
        return self._discovery.variable_descriptors()

    def is_allowed(self, value: object) -> bool:
        """Return ``True`` if ``value`` is a supported :class:`VariableDescriptor`."""
        if isinstance(value, VariableDescriptor):
            return self._discovery.is_variable_supported(value)
        return False


class _NamedExprSubSlot:
    """Sub-namespace: in-scope named expressions accepted by the scalar slot."""

    _discovery: Discovery

    def __init__(self, discovery: Discovery) -> None:
        self._discovery = discovery

    def allowed_values(self) -> list[str]:
        """Return names of named expressions currently in scope."""
        return self._discovery.named_expression_names()

    def is_allowed(self, value: object) -> bool:
        """Return ``True`` if ``value`` is an in-scope named expression name."""
        if not isinstance(value, str):
            return False
        names = self.allowed_values()
        # Permissive when the names are unknown: we can't verify.
        return not names or value in names


class ScalarSlot(SlotAccessor):
    """
    Accessor for a :attr:`Kind.SCALAR` parameter.

    Exposes segregated sub-slots (``.variables``, ``.named``) plus an agglomerated
    :meth:`allowed_values` view.
    """

    variables: _VariablesSubSlot
    named: _NamedExprSubSlot

    def __init__(self, param: Param, discovery: Discovery) -> None:
        super().__init__(param, discovery)
        self.variables = _VariablesSubSlot(discovery)
        self.named = _NamedExprSubSlot(discovery)

    @override
    def allowed_values(self) -> list[object]:
        """Return variable descriptors followed by named-expression names."""
        return [*self.variables.allowed_values(), *self.named.allowed_values()]

    @override
    def is_allowed(self, value: object) -> bool:
        """Return ``True`` if either sub-slot accepts ``value``."""
        return self.variables.is_allowed(value) or self.named.is_allowed(value)


# --------------------------------------------------------------------------- #
# Factory                                                                     #
# --------------------------------------------------------------------------- #


_SLOTS: dict[Kind, type[SlotAccessor]] = {
    Kind.LOCATION_LIST: LocationSlot,
    Kind.SCALAR: ScalarSlot,
}


def make_slot(param: Param, discovery: Discovery) -> SlotAccessor:
    """Return the appropriate :class:`SlotAccessor` for ``param``."""
    cls = _SLOTS.get(param.kind, SlotAccessor)
    return cls(param, discovery)
