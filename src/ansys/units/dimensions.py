"""Provides the ``Dimensions`` and ``BaseDimensions`` class."""
from enum import Enum


class BaseDimensions(Enum):
    """
    Supplies all valid base dimensions used in dimensional analysis.

    Used as dictionary keys for defining a `Dimensions` object.
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
    """Represents the physical dimensions of a quantity or its units."""

    def __init__(self, dimensions_container: dict[BaseDimensions : int | float] = None):
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

    @property
    def dimensions(self):
        """Dimensions as a dictionary."""
        dims = {x.value: y for x, y in self._dimensions.items()}
        return dict(dims)

    @property
    def single_dimension(self):
        """Get the name of the base dimension."""
        dims = [x.name for x in self._dimensions.keys()]
        if len(dims) != 1:
            raise DimensionsError.MULTIPLE_BASE_DIMENSIONS(dimensions=self)
        return dims[0]

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

    def __mul__(self, other):
        results = self._dimensions.copy()
        for dim, value in other._dimensions.items():
            if dim in results:
                results[dim] += value
            else:
                results[dim] = value
        return Dimensions(results)

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
        temp_dim = self / other
        temp = BaseDimensions.TEMPERATURE
        temp_diff = BaseDimensions.TEMPERATURE_DIFFERENCE
        if temp in temp_dim._dimensions and temp_diff in temp_dim._dimensions:
            if temp_dim._dimensions[temp] == -temp_dim._dimensions[temp_diff]:
                del temp_dim._dimensions[temp_diff]
                del temp_dim._dimensions[temp]
        return not bool(temp_dim.dimensions)

    def __ne__(self, other):
        return not self.__eq__(other)


class DimensionsError(ValueError):
    """Custom dimensions errors."""

    def __init__(self, err):
        super().__init__(err)

    @classmethod
    def INCORRECT_DIMENSIONS(cls):
        """Return in case of dimensions not in dimension order."""
        return cls(f"The `dimensions_container` key must be a 'BaseDimensions' object")

    @classmethod
    def MULTIPLE_BASE_DIMENSIONS(cls, dimensions):
        return cls(f"`{dimensions}` has more than one base dimension.")
