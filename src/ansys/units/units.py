"""Provide the ``Units`` class."""
from typing import Any, Optional, Tuple

import ansys.units as q
from ansys.units._constants import _QuantityType
from ansys.units.quantity import Quantity, QuantityError  # noqa: F401


class Units(object):
    """
    Initializes a ``Units`` object with all unit string manipulation methods.

    Methods
    -------
    filter_unit_term()
        Separate multiplier, base, and power from a unit term.
    si_data()
        Compute the SI unit string, SI multiplier, and SI offset from a unit string of any type.
    si_conversion()
        Perform SI conversion based on the quantity type.
    condense()
        Condense a unit string by collecting like terms.
    get_type()
        Get the type associated with a unit string.

    Returns
    -------
    Units
        Units instance.
    """
    
    def __getattr__(self, attr):
        if attr in [*q._fundamental_units,*q._derived_units]:
            return attr
        else:
            raise QuantityError.UNKNOWN_UNITS(attr)

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
        # Check if the unit term is not an existing fundamental or derived unit.
        return unit_term and not (
            (unit_term in q._fundamental_units) or (unit_term in q._derived_units)
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
        unit_term_type = q._fundamental_units[unit_term]["type"]

        # Find SI unit with same type as unit term
        for term, term_info in q._fundamental_units.items():
            if term_info["type"] == unit_term_type and term_info["factor"] == 1.0:
                return term

    def filter_unit_term(self, unit_term: str) -> tuple:
        """
        Separate multiplier, base, and power from a unit term.

        Parameters
        ----------
        unit_term : str
            Unit term of the unit string.

        Returns
        -------
        tuple
            Tuple containing the multiplier, base, and power of the unit term.
        """
        multiplier = ""
        power = 1.0

        # strip power from unit term
        if "^" in unit_term:
            power = float(unit_term[unit_term.index("^") + 1 :])
            unit_term = unit_term[: unit_term.index("^")]

        base = unit_term

        # strip multiplier and base from unit term
        has_multiplier = self._has_multiplier(unit_term)
        if has_multiplier:
            for mult in q._multipliers:
                if unit_term.startswith(mult):
                    if not self._has_multiplier(unit_term[len(mult) :]):
                        multiplier = mult
                        base = unit_term[len(mult) :]
                        break

        # if we thought it had a multiplier, that's just because the string wasn't
        # a known unit on its own. So if we can't actually find its multiplier then
        # this string is an invalid unit string
        if has_multiplier and not multiplier:
            raise QuantityError.UNKNOWN_UNITS(unit_term)
        return multiplier, base, power
    
    def si_data(
        self,
        units: str,
        power: float = None,
        si_units: str = None,
        si_multiplier: float = None,
    ) -> tuple:
        """
        Compute the SI unit string, SI multiplier, and SI offset.

        Parameters
        ----------
        units : str
            Unit string representation of the quantity.
        power : float, None
            Power of the unit string.
        si_units : str, None
            SI unit string representation of the quantity.
        si_multiplier : float, None
            SI multiplier of the unit string.

        Returns
        -------
        tuple
            Tuple containing the SI units, SI multiplier, and SI offset.
        """
        # Initialize default values
        units = units or " "
        power = power or 1.0
        si_units = si_units or ""
        si_multiplier = si_multiplier or 1.0
        si_offset = (
            q._fundamental_units[units]["offset"]
            if units in q._fundamental_units
            else 0.0
        )

        # Split unit string into terms and parse data associated with individual terms
        for term in units.split(" "):
            unit_multiplier, unit_term, unit_term_power = self.filter_unit_term(term)

            unit_term_power *= power

            si_multiplier *= (
                q._multipliers[unit_multiplier] ** unit_term_power
                if unit_multiplier
                else 1.0
            )

            # Retrieve data associated with fundamental unit
            if unit_term in q._fundamental_units:
                if unit_term_power == 1.0:
                    si_units += f" {self._si_map(unit_term)}"
                elif unit_term_power != 0.0:
                    si_units += f" {self._si_map(unit_term)}^{unit_term_power}"

                si_multiplier *= (
                    q._fundamental_units[unit_term]["factor"] ** unit_term_power
                )

            # Retrieve derived unit composition unit string and factor
            if unit_term in q._derived_units:
                si_multiplier *= (
                    q._derived_units[unit_term]["factor"] ** unit_term_power
                )

                # Recursively parse composition unit string
                si_units, si_multiplier, _ = self.si_data(
                    units=q._derived_units[unit_term]["composition"],
                    power=unit_term_power,
                    si_units=si_units,
                    si_multiplier=si_multiplier,
                )

        return self.condense(si_units), si_multiplier, si_offset

    def condense(self, units: str) -> str:
        """
        Condense a unit string by collecting liketerms.

        Parameters
        ----------
        units : str
            Unit string to simplify.

        Returns
        -------
        str
            Simplified unit string.
        """
        terms_and_powers = {}
        units = units.strip()

        # Split unit string into terms and parse data associated with individual terms
        for term in units.split(" "):
            _, unit_term, unit_term_power = self.filter_unit_term(term)

            if unit_term in terms_and_powers:
                terms_and_powers[unit_term] += unit_term_power
            else:
                terms_and_powers[unit_term] = unit_term_power

        units = ""

        # Concatenate unit string
        for term, power in terms_and_powers.items():
            if not (power):
                continue
            if power == 1.0:
                units += f"{term} "
            else:
                power = int(power) if power % 1 == 0 else power
                units += f"{term}^{power} "

        return units.rstrip()

    def get_type(self, units: str) -> str:
        """
        Get the type associated with the unit string.

        Parameters
        ----------
        units : str
            Unit string of the quantity.

        Returns
        -------
        str
            Type of the quantity.
        """
        if units == "":
            return _QuantityType.no_type

        if units in q._fundamental_units:
            return q._fundamental_units[units]["type"]

        if units in q._derived_units:
            return _QuantityType.derived

        # HACK
        temperature_units_to_search = ("K", "C", "F", "R")
        if any([temp in units for temp in temperature_units_to_search]):
            terms = parse_temperature_units(
                units,
                ignore_exponent=False,
                units_to_search=temperature_units_to_search,
            )
            if any(is_diff for (_, is_diff) in terms):
                return _QuantityType.temperature_difference
            return _QuantityType.temperature

        return _QuantityType.composite


def parse_temperature_units(
    units: str, ignore_exponent: bool, units_to_search: Optional[Tuple[str]] = None
) -> list:
    """
    Parse temperature units and their properties from a given input string.

    Parameters
    ----------
    units : str
        Input string containing the temperature units and terms.
    ignore_exponent : bool
        Whether to ignore the exponent in terms when determining if
        they represent temperature differences.
    units_to_search : [Tuple[str]], None
        Tuple of temperature unit labels to search for. The default is
        ``None``, in which case these unit labels are searched for: ``("K", "C", "F", "R")``.

    Returns
    -------
    list
        List of tuples containing terms and their properties. Each tuple contains:

            - The original term (str)
            - A flag indicating if it represents a temperature difference (bool)
    """
    if units_to_search is None:
        units_to_search = ("K", "C", "F", "R")
    units_out = []
    for term in units.split(" "):
        term_parts = term.split("^")
        label = term_parts[0]
        exponent = term_parts[0] if len(term_parts) > 1 else "0"
        is_temp_diff = (
            label
            and (exponent != "0" or ignore_exponent)
            and label[-1] in units_to_search
        )
        units_out.append((term, is_temp_diff))
    return units_out
