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
"""Provides the ``PreferredUnits`` class."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from typing_extensions import Protocol, override

from ansys.units._unit_parsing import _units_to_dim
from ansys.units.base_dimensions import BaseDimensions
from ansys.units.dimensions import Dimensions
from ansys.units.quantity_tables.keys import *  # noqa: F403


class UnitLike(Protocol):
    """Protocol for unit-like objects accepted by ``PreferredUnits``."""

    @property
    def name(self) -> str: ...

    @property
    def dimensions(self) -> Dimensions: ...


PreferredUnit = UnitKey | str | UnitLike
PreferredUnitInput = Sequence[PreferredUnit] | PreferredUnit | None


def _iter_preferred_units(units: PreferredUnitInput) -> Sequence[PreferredUnit]:
    """Return preferred units as a sequence of individual entries."""
    if units is None:
        return []
    if isinstance(units, str):
        return [units]
    if isinstance(units, Sequence):
        return list(units)
    return [units]


def _validate_preferred_unit(
    unit: UnitKey | str | UnitLike,
) -> tuple[str, dict[BaseDimensions, float]]:
    """
    Validate a preferred unit and return its name and dimensions.

    Preferred units are display/conversion targets for derived quantities. They do not
    need to be dimensionally atomic, but they do need to resolve to a valid unit with
    dimensions.
    """
    name = str(getattr(unit, "name", None) or unit)
    try:
        dims_dict = _units_to_dim(units=str(name))
    except Exception:
        raise UnconfiguredPreferredUnit(name) from None

    if not dims_dict:
        raise UnconfiguredPreferredUnit(name)

    return name, dims_dict


class DimensionsKey:
    """Hashable key for matching dimension dictionaries."""

    def __init__(self, dimensions: Mapping[BaseDimensions, float]):
        self._dimensions: tuple[tuple[BaseDimensions, float], ...] = tuple(
            sorted(dimensions.items(), key=lambda item: item[0].name)
        )

    @override
    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, DimensionsKey) and self._dimensions == other._dimensions
        )

    @override
    def __hash__(self) -> int:
        return hash(self._dimensions)


class PreferredUnits:
    """
    An immutable mapping from dimensions to a preferred unit name.

    ``PreferredUnits`` is a conversion policy: it decides which named derived unit,
    such as ``"MPa"``, is emitted instead of an expanded base-unit expression, such as
    ``"tonne mm^-1 s^-2"``, when a quantity is converted through a
    :class:`~ansys.units.systems.UnitSystem`. It is independent of any particular
    ``UnitSystem`` and is passed directly to
    :meth:`~ansys.units.quantity.Quantity.convert`.

        Entries are matched only by dimensions. Quantities with the same dimensions,
        such as torque and energy (both ``M L^2 T^-2``), or stress and energy density
        (both ``M L^-1 T^-2``), share the same preferred-unit entry.

    Parameters
    ----------
    units: optional
        Preferred unit entries: a single unit name, a :class:`~ansys.units.unit.Unit`
        instance, any object with a ``name``, or a sequence of these values.

    Raises
    ------
    UnconfiguredPreferredUnit
        If a unit cannot be resolved to a known, dimensioned unit.
    PreferredUnitAlreadyRegistered
        If two entries would register different units for the same dimensions.

    Examples
    --------
    >>> from ansys.units import PreferredUnits
    >>> prefs = PreferredUnits(["MPa", "N"])
    """

    def __init__(
        self,
        units: PreferredUnitInput = None,
    ):
        by_dimensions: dict[DimensionsKey, str] = {}
        entries: Sequence[PreferredUnit] = _iter_preferred_units(units)

        for entry in entries:
            name, dims_dict = _validate_preferred_unit(entry)
            key = DimensionsKey(dims_dict)
            existing = by_dimensions.get(key)
            if existing is not None and existing != name:
                raise PreferredUnitAlreadyRegistered(existing, name)
            by_dimensions[key] = name

        self._by_dimensions: dict[DimensionsKey, str] = by_dimensions
        self._entries: tuple[PreferredUnit, ...] = tuple(entries)

    def unit_for(
        self,
        dimensions: Dimensions,
    ) -> str | None:
        """
        Return the preferred unit name for dimensions, if one is configured.

        Parameters
        ----------
        dimensions: Dimensions
            Dimensions of the quantity being converted.

        Returns
        -------
        str, optional
            The preferred unit name, or ``None`` if no entry matches.
        """
        return self._by_dimensions.get(DimensionsKey(dict(dimensions)))

    def with_units(
        self,
        units: PreferredUnitInput,
    ) -> PreferredUnits:
        """
        Return a new ``PreferredUnits`` combining these entries with additional ones.

        Parameters
        ----------
        units:
            Additional preferred unit entries, validated atomically together with
            the existing entries.

        Returns
        -------
        PreferredUnits
            A new, independent ``PreferredUnits`` instance.
        """
        return PreferredUnits(list(self._entries) + list(_iter_preferred_units(units)))

    @override
    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, PreferredUnits)
            and self._by_dimensions == other._by_dimensions
        )

    @override
    def __hash__(self) -> int:
        return hash(
            tuple(sorted(self._by_dimensions.items(), key=lambda kv: hash(kv[0])))
        )

    @override
    def __repr__(self) -> str:
        return f"PreferredUnits({list(self._entries)!r})"


def _coerce_preferred_units(  # pyright: ignore[reportUnusedFunction]
    preferred_units: PreferredUnits | PreferredUnitInput,
) -> PreferredUnits | None:
    """Wrap a plain unit, sequence, or ``None`` into a ``PreferredUnits`` instance."""
    if preferred_units is None or isinstance(preferred_units, PreferredUnits):
        return preferred_units
    return PreferredUnits(preferred_units)


class UnconfiguredPreferredUnit(ValueError):
    """Raised when a preferred unit cannot be resolved."""

    def __init__(self, unit: UnitKey | str):
        super().__init__(f"`{unit}` is not a configured unit.")


class PreferredUnitAlreadyRegistered(ValueError):
    """Raised when two preferred units conflict for the same dimensions."""

    def __init__(
        self,
        existing_unit: str,
        conflicting_unit: str,
    ):
        super().__init__(
            " ".join(
                [
                    f"`{existing_unit}` is already configured as the preferred unit for",
                    f"the same dimensions as `{conflicting_unit}`.",
                ]
            )
        )
