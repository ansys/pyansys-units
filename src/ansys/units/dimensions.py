"""Provides the ``Dimensions`` and ``BaseDimensions`` class."""
from enum import Enum
from typing import Optional

import ansys.units as ansunits


class BaseDimensions(Enum):
    """
    Supplies all valid base dimensions used in dimensional analysis.

    Used as dictionary keys for defining a `Dimensions` object.

    Attributes
    ----------
    MASS
    LENGTH
    TIME
    TEMPERATURE
    TEMPERATURE_DIFFERENCE
    ANGLE
    CHEMICAL_AMOUNT
    LIGHT
    CURRENT
    SOLID_ANGLE
    """

    MASS = 0
    LENGTH = 1
    TIME = 2
    TEMPERATURE = 3
    TEMPERATURE_DIFFERENCE = 4
    ANGLE = 5
    CHEMICAL_AMOUNT = 6
    LIGHT = 7
    CURRENT = 8
    SOLID_ANGLE = 9


class Dimensions:
    """
    A class which contains the base unit information.

    A dictionary of ``BaseDimensions`` and power is required
    for a non-dimensionless object.

    Parameters
    ----------
    dimensions_container : dict, optional
        Dictionary of {``BaseDimensions``: power, ...}.

    Attributes
    ----------
    dimensions
    """

    def __init__(
        self,
        dimensions_container: Optional[BaseDimensions] = None,
    ):
        """
        Create a ``Dimensions`` object from a dictionary of ``BaseDimensions`` and
        power. Default is dimensionless.

        Parameters
        ----------
        dimensions_container : dict, optional
            Dictionary of {``BaseDimensions``: power, ...}.
        """
        dimensions_container = dimensions_container or {}
        self._dimensions = dimensions_container.copy()
        for x, y in dimensions_container.items():
            if not isinstance(x, BaseDimensions):
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
            temp = {BaseDimensions.TEMPERATURE: 1.0}
            delta_temp = {BaseDimensions.TEMPERATURE_DIFFERENCE: 1.0}
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


class DimensionsError(ValueError):
    """Custom dimensions errors."""

    def __init__(self, err):
        super().__init__(err)

    @classmethod
    def INCORRECT_DIMENSIONS(cls):
        """Return in case of dimensions not in dimension order."""
        return cls(f"The `dimensions_container` key must be a 'BaseDimensions' object")
