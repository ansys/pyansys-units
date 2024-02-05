"""Provides the ``Dimensions`` class."""

from __future__ import annotations

from typing import Union

from ansys.units import BaseDimensions


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
        dimensions: dict[BaseDimensions, Union[int, float]] = None,
        copy_from: Dimensions = None,
    ):
        dimensions = dimensions or {}
        self._dimensions = {
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
        dims = {x.name: y for x, y in self}
        if not dims:
            dims = ""
        return str(dims)

    def __str__(self):
        return self._to_string()

    def __repr__(self):
        return self._to_string()

    def __iter__(self):
        for item in self._dimensions.items():
            yield item

    def __mul__(self, other):
        results = self._dimensions.copy()
        for dim, value in other:
            if dim in results:
                results[dim] += value
            else:
                results[dim] = value
        return Dimensions(results)

    def __truediv__(self, other):
        results = self._dimensions.copy()
        for dim, value in other:
            if dim in results:
                results[dim] -= value
            else:
                results[dim] = -value
        return Dimensions(results)

    def __pow__(self, __value):
        results = self._dimensions.copy()
        for item in self:
            results[item[0]] *= __value
        return Dimensions(results)

    def __eq__(self, __value):
        dims = __value._dimensions.copy()
        for dim, value in self:
            if dim in dims:
                dims[dim] -= value
            else:
                return False
        if [False for v in dims.values() if v != 0]:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __bool__(self):
        return bool(self._dimensions)


class IncorrectDimensions(ValueError):
    """Raised on initialization if a dimension is not of type ``BaseDimensions``."""

    def __init__(self):
        super().__init__("The `dimensions` key must be a 'BaseDimensions' object")
