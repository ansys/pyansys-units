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
Low-level unit string parsing helpers.

This module is intentionally a leaf module: it only depends on
``ansys.units._constants`` and ``ansys.units.base_dimensions``. Both
``ansys.units.unit`` and ``ansys.units.systems`` depend on it, so keeping it
free of any dependency on those two modules avoids a circular import between
them.
"""

from __future__ import annotations

from collections.abc import Mapping

from ansys.units._constants import _aliases, _base_units, _derived_units, _multipliers
from ansys.units.base_dimensions import BaseDimensions


def _multiplier_check(unit_term: str) -> bool:
    """
    Check if a unit term contains a multiplier.

    Parameters
    ----------
    unit_term : str
        Unit term of the unit string.

    Returns
    -------
    bool
        ``True`` if the unit term contains a multiplier, ``False`` otherwise.
    """
    # Check if the unit term is not an existing base or derived unit.
    return bool(
        unit_term
        and not (
            (unit_term in _base_units)
            or (unit_term in _derived_units)
            or (unit_term in _aliases)
        )
    )


def _filter_unit_term(unit_term: str) -> tuple[str, str, float]:
    """
    Separate multiplier, base, and exponent from a unit term.

    Parameters
    ----------
    unit_term : str
        Unit term of the unit string.

    Returns
    -------
    tuple
        Tuple containing the multiplier, base, and exponent of the unit term.
    """
    multiplier = ""
    exponent = 1.0

    # strip exponent from unit term
    if "^" in unit_term:
        exponent = float(unit_term[unit_term.index("^") + 1 :])
        unit_term = unit_term[: unit_term.index("^")]

    base = unit_term

    # Resolve alias to canonical unit name before multiplier detection
    while unit_term in _aliases:
        unit_term = _aliases[unit_term]
    base = unit_term

    # strip multiplier and base from unit term
    has_multiplier = _multiplier_check(unit_term)
    if has_multiplier:
        for mult in _multipliers:
            if unit_term.startswith(mult):
                if not _multiplier_check(unit_term[len(mult) :]):
                    multiplier = mult
                    base = unit_term[len(mult) :]
                    break

    # if we thought it had a multiplier, that's just because the string wasn't
    # a known unit on its own. So if we can't actually find its multiplier then
    # this string is an invalid unit string
    if has_multiplier and not multiplier:
        raise UnconfiguredUnit(unit_term)
    return multiplier, base, exponent


def _units_to_dim(
    units: str,
    exponent: float = 1.0,
    dimensions: Mapping[
        BaseDimensions, float
    ] = {},  # pyright: ignore[reportCallInDefaultInitializer]
) -> dict[BaseDimensions, float]:
    """
    Convert a unit string into a Dimensions instance.

    Parameters
    ----------
    units : str
        Unit string.
    Returns
    -------
    dict
        Dimensions dictionary
    """
    dimensions = dict(dimensions)
    # Split unit string into terms and parse data associated with individual terms
    for term in units.split(" "):
        _, unit_term, unit_term_exponent = _filter_unit_term(term)
        unit_term_exponent *= exponent
        # retrieve data associated with base unit
        if unit_term in _base_units:
            idx = _base_units[unit_term]["type"]

            if BaseDimensions[idx] in dimensions:
                dimensions[BaseDimensions[idx]] += unit_term_exponent
            else:
                dimensions[BaseDimensions[idx]] = unit_term_exponent
        # Retrieve derived unit composition unit string and SI factor.
        elif unit_term in _derived_units:
            # Recursively parse composition unit string

            dimensions = _units_to_dim(
                units=_derived_units[unit_term]["composition"],
                exponent=unit_term_exponent,
                dimensions=dimensions,
            )
        elif _:
            raise UnconfiguredUnit(_)

    return dimensions


class UnconfiguredUnit(ValueError):
    """Raised when the specified unit is unconfigured."""

    def __init__(self, unit):
        super().__init__(f"`{unit}` is an unconfigured unit.")
