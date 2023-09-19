import ansys.units as ansunits
from ansys.units.utils import filter_unit_term


class Unit:
    """
    Initializes a Unit. Contains all the unit information.

    Parameters
    ----------
    Name: str,
        Name of the unit or string chain of combined units
    Config: dict
        dictionary of unit properties
    Dimensions: list
        A list of length 9 to describe all base units.
    Unit System: str
        Define the unit system for base units of dimension,
        default is SI.

    Methods
    -------

    Returns
    -------
    Unit
        Unit instance.
    """

    def __init__(
        self,
        units: str = None,
        config: dict = None,
        dimensions: list = None,
        unit_sys: str = None,
    ):
        if units and dimensions:
            raise UnitError.EXCESSIVE_PARAMETERS()

        if units:
            self._name = units
            dimensions = self._units_to_dim(units=units)
            self._dimensions = ansunits.Dimensions(dimensions)
        elif len(dimensions) > self.max_dim_len():
            raise UnitError.EXCESSIVE_DIMENSIONS(len(dimensions))
        else:
            self._dimensions = ansunits.Dimensions(dimensions)
            self._name = self._dim_to_units(dimensions=dimensions, unit_sys=unit_sys)

        if not config:
            config = self._get_config(self._name)
        if "type" not in config:
            config.update({"type": self._get_config(self._name)["type"]})
        for key in config:
            setattr(self, f"_{key}", config[key])

    def _get_config(self, name: str) -> dict:
        if name in ansunits._fundamental_units:
            return ansunits._fundamental_units[name]

        if name in ansunits._derived_units:
            type = {"type": ansunits._QuantityType.derived}
            return dict(**type, **ansunits._derived_units[name])

        return {"type": ansunits._QuantityType.composite}

    def _dim_to_units(self, dimensions: list, unit_sys: list = None) -> str:
        """
        Convert a dimensions list into a unit string.

        Parameters
        ----------
        dimensions : list
            List of unit dimensions.

        unit_sys : list
            Optional unit system for dimensions list.
            default is SI units

        Returns
        -------
        str
            Unit string representation of the dimensions.
        """
        # Ensure dimensions list contains 10 terms
        dimensions = [
            float(dim)
            for dim in dimensions + ((self.max_dim_len() - len(dimensions)) * [0])
        ]
        units = ""
        if isinstance(unit_sys, ansunits.UnitSystem):
            unit_sys = unit_sys.base_units
        else:
            unit_sys = unit_sys or "SI"
            unit_sys = ansunits._unit_systems[unit_sys]
        # Define unit term and associated value from dimension with dimensions list
        for idx, dim in enumerate(dimensions):
            if dim == 1.0:
                units += f"{unit_sys[idx]} "
            elif dim != 0.0:
                dim = int(dim) if dim % 1 == 0 else dim
                units += f"{unit_sys[idx]}^{dim} "

        return units.strip()

    def _units_to_dim(
        self, units: str, power: float = None, dimensions: list = None
    ) -> ansunits.Dimensions:
        """
        Convert a unit string into a Dimensions instance.

        Parameters
        ----------
        units : str
            Unit string of quantity.
        power : float
            Power of unit string.
        Returns
        -------
        Dimensions
            Dimensions instance.
        """
        power = power or 1.0
        dimensions = dimensions or [0.0] * self.max_dim_len()

        # Split unit string into terms and parse data associated with individual terms
        for term in units.split(" "):
            _, unit_term, unit_term_power = filter_unit_term(term)

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
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def dimensions(self):
        return self._dimensions

    @staticmethod
    def max_dim_len():
        """Maximum number of elements within a dimensions list."""
        return 10

    def __str__(self):
        returned_string = ""
        attrs = self.__dict__
        for key in attrs:
            returned_string += f"{key}: {attrs[key]}\n"
        return returned_string

    def __mul__(self, __value):
        if isinstance(__value, Unit):
            new_dimensions = self.dimensions + __value.dimensions
            return Unit(dimensions=new_dimensions)

        if isinstance(__value, (float, int)):
            return ansunits.Quantity(value=__value, units=self)

    def __rmul__(self, __value):
        return self.__mul__(__value)

    def __truediv__(self, __value):
        if isinstance(__value, Unit):
            new_dimensions = self.dimensions - __value.dimensions
            return Unit(dimensions=new_dimensions)

    def __pow__(self, __value):
        new_dimensions = self.dimensions * __value
        return Unit(dimensions=new_dimensions)


class UnitError(ValueError):
    """Custom dimensions errors."""

    def __init__(self, err):
        super().__init__(err)

    @classmethod
    def EXCESSIVE_PARAMETERS(cls):
        """Return in case of excessive parameters."""
        return cls(
            "Unit only accepts 1 of the following parameters: (units) or (dimensions)."
        )

    @classmethod
    def EXCESSIVE_DIMENSIONS(cls, len):
        """Return in case of excessive dimensions."""
        return cls(
            f"The `dimensions` argument must contain 9 values or less, currently there are {len}."
        )
