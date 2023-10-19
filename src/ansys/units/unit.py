import ansys.units as ansunits
from ansys.units import _base_units, _derived_units, _multipliers


class Unit:
    """
    A class with all unit information for a quantity.

    Parameters
    ----------
    units: str, optional
        Name of the unit or string chain of combined units
    config: dict, optional
        dictionary of unit properties
    dimensions: Dimensions, optional
        An instance of the Dimensions class.
    unit_sys: str, optional
        Define the unit system for base units of dimension,
        default is SI.

    Attributes
    ----------
    name
    si_units
    si_multiplier
    si_offset
    dimensions
    """

    def __init__(
        self,
        units: str = None,
        config: dict = None,
        dimensions: ansunits.Dimensions = None,
        unit_sys: ansunits.UnitSystem = None,
    ):
        if units:
            self._name = units
            _dimensions = self._units_to_dim(units=units)
            self._dimensions = ansunits.Dimensions(_dimensions)
            if dimensions and self._dimensions != dimensions:
                raise UnitError.INCONSISTENT_DIMENSIONS()
            if not self._dimensions.dimensions:
                self._name = ""
        elif dimensions:
            self._dimensions = dimensions
            self._name = self._dim_to_units(dimensions=dimensions, unit_sys=unit_sys)
        else:
            self._name = ""
            self._dimensions = ansunits.Dimensions()

        if not config:
            config = self._get_config(name=self._name)
        if config:
            for key in config:
                setattr(self, f"_{key}", config[key])

        self._si_units, self._si_scaling_factor, self._si_offset = self.si_data(
            units=self.name
        )

    def _get_config(self, name: str) -> dict:
        """
        Retrieve unit configuration from '_base_units' or '_derived_units'.

        Parameters
        ----------
        name : str
            Unit string.
        Returns
        -------
        dict
            Dictionary of extra unit information.
        """
        if name in ansunits._base_units:
            return ansunits._base_units[name]
        if name in ansunits._derived_units:
            return ansunits._derived_units[name]

    def _dim_to_units(
        self,
        dimensions: ansunits.Dimensions,
        unit_sys: ansunits.UnitSystem = None,
    ) -> str:
        """
        Convert a dimensions list into a unit string.

        Parameters
        ----------
        dimensions : Dimensions object
            Instance of Dimension class.

        unit_sys : UnitSystem object, optional
            Unit system for dimensions list.
            Default is SI units.

        Returns
        -------
        str
            Unit string.
        """
        if not unit_sys:
            unit_sys = ansunits.UnitSystem()

        base_units = unit_sys.base_units
        units = ""
        for idx, value in dimensions.dimensions.items():
            if value == 1:
                units += f"{base_units[idx.value]} "
            elif value != 0.0:
                value = int(value) if value % 1 == 0 else value
                units += f"{base_units[idx.value]}^{value} "

        return units.strip()

    def _units_to_dim(
        self, units: str, exponent: float = None, dimensions: dict = None
    ):
        """
        Convert a unit string into a Dimensions instance.

        Parameters
        ----------
        units : str
            Unit string.
        Returns
        -------
        dict
            Dimensions dictionary
        """
        exponent = exponent or 1.0
        dimensions = dimensions or {}
        # Split unit string into terms and parse data associated with individual terms
        for term in units.split(" "):
            _, unit_term, unit_term_exponent = self.filter_unit_term(term)
            unit_term_exponent *= exponent
            # retrieve data associated with base unit
            if unit_term in _base_units:
                idx = _base_units[unit_term]["type"]

                if ansunits.BaseDimensions[idx] in dimensions:
                    dimensions[ansunits.BaseDimensions[idx]] += unit_term_exponent
                else:
                    dimensions[ansunits.BaseDimensions[idx]] = unit_term_exponent

            # Retrieve derived unit composition unit string and SI factor.
            if unit_term in _derived_units:
                # Recursively parse composition unit string

                dimensions = self._units_to_dim(
                    units=_derived_units[unit_term]["composition"],
                    exponent=unit_term_exponent,
                    dimensions=dimensions,
                )

        return dimensions

    def _has_multiplier(self, unit_term: str) -> bool:
        """
        Check if a unit term contains a multiplier.

        Parameters
        ----------
        unit_term : str
            Unit term of the unit string.

        Returns
        -------
        bool
            ``True`` if the unit term contains a multiplier, ``False`` otherwise.
        """
        # Check if the unit term is not an existing base or derived unit.
        return unit_term and not (
            (unit_term in _base_units) or (unit_term in _derived_units)
        )

    def _si_map(self, unit_term: str) -> str:
        """
        Map unit to SI unit equivalent.

        Parameters
        ----------
        unit_term : str
            Unit term of the unit string.

        Returns
        -------
        term : str
            SI unit equivalent.
        """
        # Retrieve type associated with unit term
        unit_term_type = _base_units[unit_term]["type"]

        # Find SI unit with same type as unit term
        for term, term_info in _base_units.items():
            if (
                term_info["type"] == unit_term_type
                and term_info["si_scaling_factor"] == 1.0
            ):
                return term

    def _condense(self, units=str) -> str:
        """
        Condense a unit string by collecting like terms.

        Parameters
        ----------
        units : str
            Unit string to simplify.

        Returns
        -------
        str
            Simplified unit string.
        """
        terms_and_exponents = {}
        units = units.strip()

        # Split unit string into terms and parse data associated with individual terms
        for term in units.split(" "):
            _, unit_term, unit_term_exponent = self.filter_unit_term(term)

            if unit_term in terms_and_exponents:
                terms_and_exponents[unit_term] += unit_term_exponent
            else:
                terms_and_exponents[unit_term] = unit_term_exponent

        units = ""

        # Concatenate unit string
        for term, exponent in terms_and_exponents.items():
            if not (exponent):
                continue
            if exponent == 1.0:
                units += f"{term} "
            else:
                exponent = int(exponent) if exponent % 1 == 0 else exponent
                units += f"{term}^{exponent} "

        return units.rstrip()

    def filter_unit_term(self, unit_term: str) -> tuple:
        """
        Separate multiplier, base, and exponent from a unit term.

        Parameters
        ----------
        unit_term : str
            Unit term of the unit string.

        Returns
        -------
        tuple
            Tuple containing the multiplier, base, and exponent of the unit term.
        """
        multiplier = ""
        exponent = 1.0

        # strip exponent from unit term
        if "^" in unit_term:
            exponent = float(unit_term[unit_term.index("^") + 1 :])
            unit_term = unit_term[: unit_term.index("^")]

        base = unit_term

        # strip multiplier and base from unit term
        has_multiplier = self._has_multiplier(unit_term)
        if has_multiplier:
            for mult in _multipliers:
                if unit_term.startswith(mult):
                    if not self._has_multiplier(unit_term[len(mult) :]):
                        multiplier = mult
                        base = unit_term[len(mult) :]
                        break

        # if we thought it had a multiplier, that's just because the string wasn't
        # a known unit on its own. So if we can't actually find its multiplier then
        # this string is an invalid unit string
        if has_multiplier and not multiplier:
            raise UnitError.UNKNOWN_UNITS(unit_term)
        return multiplier, base, exponent

    def si_data(
        self,
        units: str,
        exponent: float = None,
        si_units: str = None,
        si_scaling_factor: float = None,
    ) -> tuple:
        """
        Compute the SI unit string, SI scaling factor, and SI offset.

        Parameters
        ----------
        units : str
            Unit string representation of the quantity.
        exponent : float, None
            exponent of the unit string.
        si_units : str, None
            SI unit string representation of the quantity.
        si_scaling_factor : float, None
            SI scaling factor of the unit string.

        Returns
        -------
        tuple
            Tuple containing the SI units, SI scaling factor, and SI offset.
        """
        # Initialize default values
        units = units or " "
        exponent = exponent or 1.0
        si_units = si_units or ""
        si_scaling_factor = si_scaling_factor or 1.0
        si_offset = _base_units[units]["si_offset"] if units in _base_units else 0.0

        # Split unit string into terms and parse data associated with individual terms
        for term in units.split(" "):
            unit_multiplier, unit_term, unit_term_exponent = self.filter_unit_term(term)

            unit_term_exponent *= exponent

            si_scaling_factor *= (
                _multipliers[unit_multiplier] ** unit_term_exponent
                if unit_multiplier
                else 1.0
            )

            # Retrieve data associated with base unit
            if unit_term in _base_units:
                if unit_term_exponent == 1.0:
                    si_units += f" {self._si_map(unit_term)}"
                elif unit_term_exponent != 0.0:
                    si_units += f" {self._si_map(unit_term)}^{unit_term_exponent}"

                si_scaling_factor *= (
                    _base_units[unit_term]["si_scaling_factor"] ** unit_term_exponent
                )

            # Retrieve derived unit composition unit string and SI scaling factor
            elif unit_term in _derived_units:
                si_scaling_factor *= (
                    _derived_units[unit_term]["factor"] ** unit_term_exponent
                )

                # Recursively parse composition unit string
                si_units, si_scaling_factor, _ = self.si_data(
                    units=_derived_units[unit_term]["composition"],
                    exponent=unit_term_exponent,
                    si_units=si_units,
                    si_scaling_factor=si_scaling_factor,
                )

        return self._condense(si_units), si_scaling_factor, si_offset

    @property
    def name(self):
        """Unit String."""
        return self._name

    @property
    def si_units(self):
        """The SI unit."""
        return self._si_units

    @property
    def si_scaling_factor(self):
        """The scaling factor used in SI conversion calculations."""
        return self._si_scaling_factor

    @property
    def si_offset(self):
        """The offset used in SI conversion calculations."""
        return self._si_offset

    @property
    def dimensions(self):
        """Dimensions object."""
        return self._dimensions

    def __str__(self):
        returned_string = ""
        attrs = self.__dict__
        for key in attrs:
            returned_string += f"{key}: {attrs[key]}\n"
        return returned_string

    def __repr__(self):
        returned_string = ""
        attrs = self.__dict__
        for key in attrs:
            returned_string += f"{key}: {attrs[key]}\n"
        return returned_string

    def __mul__(self, __value):
        if isinstance(__value, Unit):
            new_dimensions = self.dimensions * __value.dimensions
            return Unit(dimensions=new_dimensions)

        if isinstance(__value, (float, int)):
            return ansunits.Quantity(value=__value, units=self)

    def __rmul__(self, __value):
        return self.__mul__(__value)

    def __truediv__(self, __value):
        if isinstance(__value, Unit):
            new_dimensions = self.dimensions / __value.dimensions
            return Unit(dimensions=new_dimensions)

    def __pow__(self, __value):
        new_dimensions = self.dimensions**__value
        return Unit(dimensions=new_dimensions)

    def __eq__(self, other_unit):
        for attr, value in self.__dict__.items():
            try:
                if getattr(other_unit, attr) != value:
                    return False
            except:
                return False
        return True


class UnitError(ValueError):
    """Custom dimensions errors."""

    def __init__(self, err):
        super().__init__(err)

    @classmethod
    def INCONSISTENT_DIMENSIONS(
        cls,
    ):
        """Return in case of excessive parameters."""
        return cls("Units dimensions do not match given dimensions.")

    @classmethod
    def UNKNOWN_UNITS(cls, unit: str):
        return cls(f"`{unit}` is an unknown or unconfigured unit.")
