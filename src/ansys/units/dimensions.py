"""Provides the ``Dimension`` class."""
import ansys.units as ansunits


class Dimensions:
    """
    Initializes a ``Dimensions`` object using a dimensions list or a unit string.

    Parameters
    ----------
    units : str, None
        Unit string of the quantity.
    dimensions : list, None
        List of the dimensions.
    unit_sys : str, None
        Unit system for creating units.

    Returns
    -------
    Dimensions instance.
    """

    def __init__(self, dimensions_container: (dict[str, float], list[float])):
        self._mass = 0
        self._length = 0
        self._time = 0
        self._temperature = 0
        self._temperature_difference = 0
        self._angle = 0
        self._chemical_amount = 0
        self._light = 0
        self._current = 0
        self._solid_angle = 0
        if isinstance(dimensions_container, dict):
            for dim in dimensions_container:
                if dim in ansunits._dimension_order:
                    private_dim = f"_{dim.lower().replace(' ','_')}"
                    setattr(self, private_dim, dimensions_container[dim])
                else:
                    raise DimensionsError.INCORRECT_DIMENSIONS()
        else:
            for idx, attr in enumerate(self.__dict__):
                setattr(self, attr, dimensions_container[idx])

    @property
    def all(self):
        """Dimensions list."""
        dims = []
        for attr in self.__dict__:
            value = getattr(self, attr)
            dims.append(value)
        return dims

    @staticmethod
    def max_dim_len():
        """Maximum number of elements within a dimensions list."""
        return 10

    def __add__(self, other):
        dim_list = []
        for idx, dim in enumerate(self.all):
            dim_list.append(dim + other.all[idx])
        return Dimensions(dim_list)

    def __sub__(self, other):
        dim_list = []
        for idx, dim in enumerate(self.all):
            dim_list.append(dim - other.all[idx])
        return Dimensions(dim_list)


class DimensionsError(ValueError):
    """Custom dimensions errors."""

    def __init__(self, err):
        super().__init__(err)

    @classmethod
    def EXCESSIVE_PARAMETERS(cls):
        """Return in case of excessive parameters."""
        return cls(
            "Dimensions only accepts 1 of the following parameters: (units) or (dimensions)."
        )

    @classmethod
    def EXCESSIVE_DIMENSIONS(cls, len):
        """Return in case of excessive dimensions."""
        return cls(
            f"The `dimensions` argument must contain 9 values or less, currently there are {len}."
        )

    @classmethod
    def INCORRECT_DIMENSIONS(cls):
        """Return in case of dimensions not in dimension order."""
        return cls(
            f"The `dimensions_container` must only contain values from {ansunits._dimension_order}"
        )
