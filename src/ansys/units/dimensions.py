"""Provides the ``Dimensions`` class."""
from __future__ import annotations

from typing import Optional, Union

import ansys.units as ansunits


class Dimensions:
    """
    A composite dimension (or simply dimensions) composed from an arbitrary number of
    dimensions, where each dimension is a pair consisting of a base dimension and
    exponent.

    A dictionary of ``BaseDimensions`` and exponent is required
    for a non-dimensionless object.

    If any keys are duplicated in ``copy_from`` and ``dimensions`` then the
    associated values from ``dimensions`` are used.

    Parameters
    ----------
    dimensions : dict, optional
        Dictionary of {``BaseDimensions``: exponent, ...}.
    copy_from : Dimensions, optional
        A previous instance of Dimensions.
    """

    def __init__(
        self,
        dimensions: dict[ansunits.BaseDimensions, Union[int, float]] = None,
        copy_from: ansunits.Dimensions = None,
    ):
        dimensions = dimensions or {}
        self._dimensions = {
            **(copy_from._dimensions if copy_from else {}),
            **(dimensions),
        }

        for x, y in dimensions.items():
            if not isinstance(x, ansunits.BaseDimensions):
                raise DimensionsError.INCORRECT_DIMENSIONS()
            if y == 0:
                del self._dimensions[x]

    def _temp_precheck(self, dims2, op: str = None) -> Optional[ansunits.Dimensions]:
        """
        Validate dimensions for temperature differences.

        Parameters
        ----------
        dims2 : dimensions
            Dimensions for comparison against current dimensions.
        op : str, optional
            Operation conducted on dimensions. "-"

        Returns
        -------
        Dimensions | None
            Dimensions object for a unit of temperature difference or temperature.
        """
        dims1 = self._dimensions
        if len(dims1) == 1.0 and len(dims2) == 1.0:
            temp = {ansunits.BaseDimensions.TEMPERATURE: 1.0}
            delta_temp = {ansunits.BaseDimensions.TEMPERATURE_DIFFERENCE: 1.0}
            if (dims1 == temp and dims2 == delta_temp) or (
                dims1 == delta_temp and dims2 == temp
            ):
                return ansunits.Dimensions(dimensions=temp)
            if (dims1 == temp and dims2 == temp) and op == "-":
                return ansunits.Dimensions(dimensions=delta_temp)

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

    def __add__(self, __value):
        return self._temp_precheck(dims2=__value._dimensions)

    def __mul__(self, other):
        results = self._dimensions.copy()
        for dim, value in other:
            if dim in results:
                results[dim] += value
            else:
                results[dim] = value
        return Dimensions(results)

    def __sub__(self, __value):
        return self._temp_precheck(dims2=__value._dimensions, op="-")

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

    def __gt__(self, __value):
        if self != __value:
            raise DimensionsError.INCOMPARABLE_DIMENSIONS(self, __value)

    def __ge__(self, __value):
        if self != __value:
            raise DimensionsError.INCOMPARABLE_DIMENSIONS(self, __value)

    def __lt__(self, __value):
        if self != __value:
            raise DimensionsError.INCOMPARABLE_DIMENSIONS(self, __value)

    def __le__(self, __value):
        if self != __value:
            raise DimensionsError.INCOMPARABLE_DIMENSIONS(self, __value)


class DimensionsError(ValueError):
    """Custom dimensions errors."""

    def __init__(self, err):
        super().__init__(err)

    @classmethod
    def INCORRECT_DIMENSIONS(cls):
        """Return in case of dimensions not in dimension order."""
        return cls(f"The `dimensions` key must be a 'BaseDimensions' object")

    @classmethod
    def INCOMPARABLE_DIMENSIONS(cls, dim1, dim2):
        """Return in case of dimensions not being equal."""
        return cls(f"The dimensions `{dim1}` cannot be compared to `{dim2}`")
