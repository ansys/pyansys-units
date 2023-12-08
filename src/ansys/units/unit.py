from __future__ import annotations

from ansys.units import (
    BaseDimensions,
    Dimensions,
    _api_quantity_map,
    _base_units,
    _derived_units,
    _multipliers,
)


class InconsistentDimensions(ValueError):
    """Provides the error when dimensions are inconsistent."""

    def __init__(self):
        super().__init__("Unit dimensions do not match given dimensions.")


class UnconfiguredUnit(ValueError):
    """Provides the error when the specified unit is unconfigured."""

    def __init__(self, unit):
        super().__init__(f"`{unit}` is an unconfigured unit.")


class IncorrectUnits(ValueError):
    """Provides the error when the specified units are incorrect."""

    def __init__(self, unit1, unit2):
        super().__init__(
            f"`{unit1.si_units}` and '{unit2.si_units}' must match for this operation."
        )


class UnknownMapItem(ValueError):
    """Provides the error when the specified quantity map is undefined in the yaml."""

    def __init__(self, item):
        super().__init__(f"`{item}` is not a valid quantity map item.")


class Unit:
    """
    A class containing the string name and dimensions of a unit.

    Parameters
    ----------
    units: str, optional
        Name of the unit or string chain of combined units
    config: dict, optional
        dictionary of unit properties
    dimensions: Dimensions, optional
        An instance of the Dimensions class.
    system: str, optional
        Define the unit system for base units of dimension,
        default is SI.
    map: dict, optional
        A dictionary of api map keys from the cfg.yaml and exponent values.
    copy_from: Unit, optional
        A previous instance of Unit.

    Attributes
    ----------
    name
    si_units
    si_scaling_factor
    si_offset
    dimensions

    Examples
    --------
    >>> from ansys.units import Unit, Quantity
    >>> fps = Unit("ft s^-1")
    >>> fps.name
    'ft s^-1'
    >>> fps.dimensions
    {'LENGTH': 1.0, 'TIME': -1.0}
    >>> speed = Quantity(value=5, units=fps)
    >>> speed
    Quantity (5.0, "ft s^-1")
    """

    def __init__(
        self,
        units: str = None,
        config: dict = None,
        dimensions: Dimensions = None,
        map: dict = None,
        copy_from: Unit = None,
    ):
        if copy_from:
            if (units) and units != copy_from.name:
                raise InconsistentDimensions()
            units = copy_from.name

        if map:
            units = self._map_to_units(map=map)

        if units:
            self._name = units
            _dimensions = self._units_to_dim(units=units)
            self._dimensions = Dimensions(_dimensions)
            if dimensions and self._dimensions != dimensions:
                raise InconsistentDimensions()
            if not self._dimensions:
                self._name = ""

        elif dimensions:
            self._dimensions = dimensions
            self._name = self._dim_to_units(dimensions=dimensions)
        else:
            self._name = ""
            self._dimensions = Dimensions()

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
        if name in _base_units:
            return _base_units[name]
        if name in _derived_units:
            return _derived_units[name]

    def _dim_to_units(
        self,
        dimensions: Dimensions,
    ) -> str:
        """
        Convert a dimensions list into a unit string.

        Parameters
        ----------
        dimensions : Dimensions object
            Instance of Dimension class.

        Returns
        -------
        str
            Unit string.
        """

        base_units = dimensions.system
        units = ""
        for key, value in dimensions:
            if value == 1:
                units += f"{base_units[key.value]} "
            elif value != 0.0:
                value = int(value) if value % 1 == 0 else value
                units += f"{base_units[key.value]}^{value} "

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

                if BaseDimensions[idx] in dimensions:
                    dimensions[BaseDimensions[idx]] += unit_term_exponent
                else:
                    dimensions[BaseDimensions[idx]] = unit_term_exponent

            # Retrieve derived unit composition unit string and SI factor.
            if unit_term in _derived_units:
                # Recursively parse composition unit string

                dimensions = self._units_to_dim(
                    units=_derived_units[unit_term]["composition"],
                    exponent=unit_term_exponent,
                    dimensions=dimensions,
                )

        return dimensions

    def _map_to_units(self, map: dict) -> str:
        """
        Convert a quantity map into a unit string.

        Parameters
        ----------
        quantity_map : dict[str, int]
            Quantity map to convert to a Unit.

        Returns
        -------
        Unit
            Unit object representation of the quantity map.
        """
        for key in map.keys():
            if key not in _api_quantity_map:
                raise UnknownMapItem(key)

        base_unit = ""

        for key, value in map.items():
            terms = _api_quantity_map[key]
            for term in terms.split(" "):
                multiplier, base, exponent = self.filter_unit_term(term)

                base_unit += f"{multiplier}{base}^{exponent*value}"

        return self._condense(base_unit)

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
            multiplier, unit_term, unit_term_exponent = self.filter_unit_term(term)
            full_term = f"{multiplier}{unit_term}"
            if full_term in terms_and_exponents:
                terms_and_exponents[full_term] += unit_term_exponent
            else:
                terms_and_exponents[full_term] = unit_term_exponent
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

    def _to_string(self):
        """
        Creates a string representation of the unit.

        Returns
        -------
        str
            A string version of the unit.
        """
        returned_string = ""
        attrs = self.__dict__
        for key in attrs:
            returned_string += f"{key}: {attrs[key]}\n"
        return returned_string

    def _new_units(self, __value, op):
        """
        Generate a new units instance depending on mathematical operation.

        Parameters
        ----------
        __value : int | float | Unit
            The given operand.
        op : str
            '*', '/', '**'.

        Returns
        -------
        Unit
            New unit instance.
        """
        new_units = ""
        if op == "**":
            for term in self.name.split(" "):
                multiplier, base, exponent = self.filter_unit_term(term)
                exponent *= __value
                new_units += f"{multiplier}{base}^{exponent} "
        if op == "/":
            new_units = self.name
            for term in __value.name.split(" "):
                multiplier, base, exponent = self.filter_unit_term(term)
                new_units += f" {multiplier}{base}^{exponent*-1}"
        if op == "*":
            new_units = f"{self.name} {__value.name}"

        return Unit(self._condense(new_units))

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
            raise UnconfiguredUnit(unit_term)
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
    def name(self) -> str:
        """The unit string."""
        return self._name

    @property
    def si_units(self) -> str:
        """The unit string in SI units."""
        return self._si_units

    @property
    def si_scaling_factor(self) -> float:
        """The scaling factor used to convert to SI units."""
        return self._si_scaling_factor

    @property
    def si_offset(self) -> float:
        """The offset used to convert to SI units."""
        return self._si_offset

    @property
    def dimensions(self) -> Dimensions:
        """Then units base dimensions."""
        return self._dimensions

    def __str__(self):
        return self._to_string()

    def __repr__(self):
        return self._to_string()

    def __add__(self, __value):
        new_dimensions = self.dimensions + __value.dimensions
        if new_dimensions:
            return Unit(dimensions=new_dimensions)
        if self.dimensions != __value.dimensions:
            raise IncorrectUnits(self, __value)

    def __mul__(self, __value):
        if isinstance(__value, Unit):
            return self._new_units(__value, op="*")

        else:
            return NotImplemented

    def __rmul__(self, __value):
        return self.__mul__(__value)

    def __sub__(self, __value):
        new_dimensions = self.dimensions - __value.dimensions
        if new_dimensions:
            return Unit(dimensions=new_dimensions)
        if self.dimensions != __value.dimensions:
            raise IncorrectUnits(self, __value)

    def __truediv__(self, __value):
        if isinstance(__value, Unit):
            return self._new_units(__value, op="/")

        else:
            return NotImplemented

    def __pow__(self, __value):
        return self._new_units(__value, op="**")

    def __eq__(self, other_unit):
        if not isinstance(other_unit, Unit) and self.name:
            return False
        if isinstance(other_unit, Unit):
            return self.dimensions == other_unit.dimensions
        return True

    def __ne__(self, other_unit):
        return not self.__eq__(other_unit=other_unit)
