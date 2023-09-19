"""Provides the ``Dimension`` class."""
import ansys.units as ansunits


class Dimensions:
    """
    Initializes a ``Dimensions`` object using a dictionary or dimensions list.

    Parameters
    ----------
    dimensions : dictionary, list
        Dictionary of dimensions from the dimensions_order or list.

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
        if len(dimensions_container) > Dimensions.max_dim_len():
            raise DimensionsError.EXCESSIVE_DIMENSIONS()

        if isinstance(dimensions_container, dict):
            for dim in dimensions_container:
                if dim in ansunits._dimension_order:
                    private_dim = f"_{dim.lower().replace(' ','_')}"
                    setattr(self, private_dim, dimensions_container[dim])
                else:
                    raise DimensionsError.INCORRECT_DIMENSIONS()
        else:
            for idx, attr in enumerate(self.__dict__):
                if idx < len(dimensions_container):
                    setattr(self, attr, dimensions_container[idx])

    @property
    def short_dictionary(self):
        short_dictionary = {}
        attrs = self.__dict__
        for attr in attrs:
            attr_name = attr[1:]
            attr_value = getattr(self, attr)
            if attr_value != 0:
                short_dictionary.update({attr_name: attr_value})
        return short_dictionary

    @property
    def short_list(self):
        short_list = []
        attrs = self.__dict__
        for attr in attrs:
            attr_value = getattr(self, attr)
            if attr_value != 0:
                short_list.append(attr_value)
        return short_list

    @property
    def full_list(self):
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

    def __str__(self):
        return str(self.full_list)

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

    def __mul__(self, __value):
        new_dim = [i * 5 for i in self.all]
        return Dimensions(new_dim)


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
            f"The `dimensions` must only contain values from {ansunits._dimension_order}"
        )
