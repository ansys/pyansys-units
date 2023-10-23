"""Provides the ``Dimensions`` class."""
from typing import Optional, Union

import ansys.units as ansunits


class Dimensions:
    """
    A composite dimension (or simply dimensions) composed from an arbitrary number of
    fundamental dimensions, where each fundamental dimension is a pair consisting of
    base dimension and exponent.

    A dictionary of ``BaseDimensions`` and exponent is required
    for a non-dimensionless object.

    Parameters
    ----------
    dimensions_container : dict, optional
        Dictionary of {``BaseDimensions``: exponent, ...}.

    Attributes
    ----------
    dimensions
    """

    def __init__(
        self,
        dimensions_container: dict[ansunits.BaseDimensions, Union[int, float]] = None,
    ):
        dimensions_container = dimensions_container or {}
        self._dimensions = dimensions_container.copy()
        for x, y in dimensions_container.items():
            if not isinstance(x, ansunits.BaseDimensions):
                raise DimensionsError.INCORRECT_DIMENSIONS()
            if y == 0:
                del self._dimensions[x]

    def _temp_precheck(self, dims2, op: str = None) -> Optional[str]:
        """
        Validate units for temperature differences.

        Parameters
        ----------
        units : Unit
            Unit for comparison against current units.
        op : str, None
            Operation conducted on units. "-"

        Returns
        -------
        str | None
            Units of temperature difference.
        """
        dims1 = self.dimensions
        if len(dims1) == 1.0 and len(dims2) == 1.0:
            temp = {ansunits.BaseDimensions.TEMPERATURE: 1.0}
            delta_temp = {ansunits.BaseDimensions.TEMPERATURE_DIFFERENCE: 1.0}
            if (dims1 == temp and dims2 == delta_temp) or (
                dims1 == delta_temp and dims2 == temp
            ):
                return ansunits.Dimensions(dimensions_container=temp)
            if (dims1 == temp and dims2 == temp) and op == "-":
                return ansunits.Dimensions(dimensions_container=delta_temp)

    @property
    def dimensions(self):
        """A dictionary representation."""
        return self._dimensions

    def __str__(self):
        dims = {x.name: y for x, y in self._dimensions.items()}
        if not dims:
            dims = ""
        return str(dims)

    def __repr__(self):
        dims = {x.name: y for x, y in self._dimensions.items()}
        if not dims:
            dims = ""
        return str(dims)

    def __add__(self, __value):
        return self._temp_precheck(dims2=__value.dimensions)

    def __mul__(self, other):
        results = self._dimensions.copy()
        for dim, value in other._dimensions.items():
            if dim in results:
                results[dim] += value
            else:
                results[dim] = value
        return Dimensions(results)

    def __sub__(self, __value):
        return self._temp_precheck(dims2=__value.dimensions, op="-")

    def __truediv__(self, other):
        results = self._dimensions.copy()
        for dim, value in other._dimensions.items():
            if dim in results:
                results[dim] -= value
            else:
                results[dim] = -value
        return Dimensions(results)

    def __pow__(self, __value):
        results = self._dimensions.copy()
        for dim in self._dimensions:
            results[dim] *= __value
        return Dimensions(results)

    def __eq__(self, other):
        dims = other.dimensions.copy()
        for dim, value in self.dimensions.items():
            if dim in dims:
                dims[dim] -= value
            else:
                return False
        if sum(dims.values()) == 0:
            return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __bool__(self):
        return bool(self.dimensions)

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
        return cls(f"The `dimensions_container` key must be a 'BaseDimensions' object")

    @classmethod
    def INCOMPARABLE_DIMENSIONS(cls, dim1, dim2):
        """Return in case of dimensions not being equal."""
        return cls(f"The dimensions`{dim1}` cannot be compared to '{dim2}'")
