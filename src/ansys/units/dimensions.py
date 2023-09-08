"""Provides the ``Dimension`` class."""
import ansys.units as ansunits


class Dimensions(object):
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

    def __init__(
        self, units: str = None, dimensions: list = None, unit_sys: str = None
    ):
        if units and dimensions:
            raise DimensionsError.EXCESSIVE_PARAMETERS()

        self._units = ansunits.Units
        unit_sys = unit_sys or ansunits._unit_systems["SI"]

        if units is not None:
            self._unit = units
            self._dimensions = self._units_to_dim(units=units)

        if dimensions:
            if len(dimensions) > self.max_dim_len():
                raise DimensionsError.EXCESSIVE_DIMENSIONS(len(dimensions))

            self._dimensions, self._unit = self._dim_to_units(
                dimensions=dimensions, unit_sys=unit_sys
            )

    def _dim_to_units(self, dimensions: list, unit_sys: list) -> str:
        """
        Convert a dimensions list into a unit string.

        Parameters
        ----------
        dimensions : list
            List of unit dimensions.

        unit_sys : list
            Unit system of the dimensions.

        Returns
        -------
        str
            Unit string representation of the dimensions.
        """
        # Ensure dimensions list contains 9 terms
        dimensions = [
            float(dim)
            for dim in dimensions + ((self.max_dim_len() - len(dimensions)) * [0])
        ]
        units = ""

        # Define unit term and associated value from dimension with dimensions list
        for idx, dim in enumerate(dimensions):
            if dim == 1.0:
                units += f" {unit_sys[idx]}"
            elif dim != 0.0:
                dim = int(dim) if dim % 1 == 0 else dim
                units += f" {unit_sys[idx]}^{dim}"

        return dimensions, self._units.condense(units=units)

    def _units_to_dim(
        self, units: str, power: float = None, dimensions: list = None
    ) -> list:
        """
        Convert a unit string into a dimensions list.

        Parameters
        ----------
        units : str
            Unit string of quantity.
        power : float
            Power of unit string.

        Returns
        -------
        list
            Dimensions representation of unit string.
        """
        power = power or 1.0
        dimensions = dimensions or [0.0] * self.max_dim_len()

        # Split unit string into terms and parse data associated with individual terms
        for term in units.split(" "):
            _, unit_term, unit_term_power = self._units.filter_unit_term(term)

            unit_term_power *= power

            # retrieve data associated with fundamental unit
            if unit_term in ansunits._fundamental_units:
                idx = (
                    ansunits._dimension_order[
                        ansunits._fundamental_units[unit_term]["type"]
                    ]
                    - 1
                )
                dimensions[idx] += unit_term_power

            # Retrieve derived unit composition unit string and factor.
            if unit_term in ansunits._derived_units:
                # Recursively parse composition unit string
                dimensions = self._units_to_dim(
                    units=ansunits._derived_units[unit_term]["composition"],
                    power=unit_term_power,
                    dimensions=dimensions,
                )

        return dimensions

    @property
    def units(self):
        """Unit string representation of dimensions."""
        return self._unit

    @property
    def dimensions(self):
        """Dimensions list."""
        return self._dimensions

    @staticmethod
    def max_dim_len():
        """Maximum number of elements within a dimensions list."""
        return 9


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
