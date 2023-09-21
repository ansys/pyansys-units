"""Provides the ``Dimension`` class."""
from enum import Enum


class BaseDimensions(Enum):
    """Base dimensions."""

    mass = 0
    length = 1
    time = 2
    temperature = 3
    temperature_difference = 4
    angle = 5
    chemical_amount = 6
    light = 7
    current = 8
    solid_angle = 9


class Dimensions:
    """
    Initializes a ``Dimensions`` object using a dictionary or dimensions list.

    Parameters
    ----------
    dimensions_container : dictionary, list, optional
        Dictionary of dimensions from the dimensions_order or list.

    Returns
    -------
    Dimensions instance.
    """

    def __init__(self, dimensions_container: dict[BaseDimensions : int | float] = {}):
        self._dimensions = dimensions_container.copy()
        for x, y in dimensions_container.items():
            if not isinstance(x, BaseDimensions):
                raise DimensionsError.INCORRECT_DIMENSIONS()
            if y == 0:
                del self._dimensions[x]

    @property
    def dimensions(self):
        """Dimensions as dictionary."""
        dims = {x.value: y for x, y in self._dimensions.items()}
        return dims

    @staticmethod
    def max_dim_len():
        """Maximum number of elements within a dimensions list."""
        return 10

    def __str__(self):
        dims = {x.name: y for x, y in self._dimensions.items()}
        return str(dims)

    def __add__(self, other):
        results = self._dimensions.copy()
        for dim, value in other._dimensions.items():
            if dim in results:
                results[dim] += value
            else:
                results[dim] = value
        return Dimensions(results)

    def __sub__(self, other):
        results = self._dimensions.copy()
        for dim, value in other._dimensions.items():
            if dim in results:
                results[dim] -= value
            else:
                results[dim] = -value
        return Dimensions(results)

    def __mul__(self, __value):
        results = self._dimensions.copy()
        for dim in self._dimensions:
            results[dim] *= __value
        return Dimensions(results)

    def __eq__(self, other):
        temp_dim = self - other
        temp = BaseDimensions.temperature
        temp_diff = BaseDimensions.temperature_difference
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
        return cls(f"The `dimensions` must only contain values from 'BaseDimensions'")
