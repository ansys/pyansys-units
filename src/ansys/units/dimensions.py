"""Provides the ``Dimensions`` class."""
import ansys.units as ansunits


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
        self, dimensions_container: dict[ansunits.BaseDimensions : int | float] = None
    ):
        dimensions_container = dimensions_container or {}
        self._dimensions = dimensions_container.copy()
        for x, y in dimensions_container.items():
            if not isinstance(x, ansunits.BaseDimensions):
                raise DimensionsError.INCORRECT_DIMENSIONS()
            if y == 0:
                del self._dimensions[x]

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
        temp = ansunits.TEMPERATURE
        temp_diff = ansunits.TEMPERATURE_DIFFERENCE
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
