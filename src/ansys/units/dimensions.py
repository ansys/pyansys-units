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
"""Provides the ``Dimensions`` class."""

from __future__ import annotations

from collections.abc import Generator, Mapping

from ansys.units.base_dimensions import BaseDimensions


class Dimensions:
    """
    A representation of an arbitrary number of dimensions, where each dimension is a
    pair consisting of a base dimension and exponent.

    A dictionary of ``BaseDimensions`` and exponent is required
    for a non-dimensionless object.

    If any keys are duplicated in ``copy_from`` and ``dimensions`` then the
    associated values from ``dimensions`` are used.

    Parameters
    ----------
    dimensions : dict, optional
        Dictionary of {``BaseDimensions``: exponent, ...}.
    system : UnitSystem, optional
        The unit system for the dimensions.
    copy_from : Dimensions, optional
        A previous instance of Dimensions.
    """

    def __init__(
        self,
        dimensions: Mapping[BaseDimensions, float] | None = None,
        copy_from: Dimensions | None = None,
    ):
        dimensions = dimensions or {}
        self._dimensions: dict[BaseDimensions, float] = {
            **(copy_from._dimensions if copy_from else {}),
            **(dimensions),
        }

        for x, y in dimensions.items():
            if not isinstance(x, BaseDimensions):
                raise IncorrectDimensions()
            if y == 0:
                del self._dimensions[x]

    def _to_string(self):
        """
        Creates a string representation of the dimensions.

        Returns
        -------
        str
            A string version of the dimensions.
        """
        return str({x.name: y for x, y in self})

    def __str__(self) -> str:
        return self._to_string()

    def __repr__(self) -> str:
        return self._to_string()

    def __iter__(self) -> Generator[tuple[BaseDimensions, float]]:
        yield from self._dimensions.items()

    def __mul__(self, other: Dimensions) -> Dimensions:
        results = self._dimensions.copy()
        for dim, value in other:
            if dim in results:
                results[dim] += value
            else:
                results[dim] = value
        return Dimensions(results)

    def __truediv__(self, other: Dimensions) -> Dimensions:
        results = self._dimensions.copy()
        for dim, value in other:
            if dim in results:
                results[dim] -= value
            else:
                results[dim] = -value
        return Dimensions(results)

    def __pow__(self, __value: float) -> Dimensions:
        results = self._dimensions.copy()
        for item in self:
            results[item[0]] *= __value
        return Dimensions(results)

    def __eq__(self, __value: object) -> bool:
        return (
            isinstance(__value, Dimensions) and self._dimensions == __value._dimensions
        )

    def __bool__(self):
        return bool(self._dimensions)

    def __getitem__(self, key: str) -> float:
        dimension_name = BaseDimensions[key]
        return self._dimensions[dimension_name]


class IncorrectDimensions(ValueError):
    """Raised on initialization if a dimension is not of type ``BaseDimensions``."""

    def __init__(self):
        super().__init__("The `dimensions` key must be a 'BaseDimensions' object")
