# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

from collections.abc import Mapping, Sequence
import functools
import os
from typing import TYPE_CHECKING, Any, overload

from typing_extensions import override

from ansys.units._constants import (
    _base_units,
    _BaseUnitInfo,
    _derived_units,
    _DerivedUnitInfo,
    _multipliers,
    _quantity_units_table,
)
from ansys.units._unit_parsing import (
    _filter_unit_term,
    _units_to_dim,
)
from ansys.units._unit_parsing import UnconfiguredUnit as _UnconfiguredUnit
from ansys.units.base_dimensions import BaseDimensions
from ansys.units.dimensions import Dimensions
from ansys.units.preferred_units import (
    PreferredUnitInput,
    PreferredUnits,
    _coerce_preferred_units,
)
from ansys.units.quantity_tables.keys import QuantityKey
from ansys.units.systems import UnitSystem

UnconfiguredUnit = _UnconfiguredUnit

if TYPE_CHECKING:
    import numpy as np
    import numpy.typing as npt

    from ansys.units.quantity import Quantity, ValT, Vector
    from ansys.units.unit_registry import UnitRegistry


@functools.cache
def _get_quantity_and_array():
    from ansys.units.quantity import Quantity, _array

    return Quantity, _array


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
    table: dict, optional
        A dictionary of api table keys from the cfg.yaml and exponent values.
    copy_from: Unit, optional
        A previous instance of Unit.

    Attributes
    ----------
    name
    si_units
    si_scaling_factor
    si_offset
    dimensions

    See Also
    --------
    :mod:`ansys.units.common`
        A collection of predefined units for use.

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
    Quantity(5.0, "ft s^-1")
    """

    def __init__(
        self,
        units: str | None = None,
        config: Mapping[str, Any] | None = None,
        dimensions: Dimensions | None = None,
        system: UnitSystem | str | None = None,
        table: Mapping[QuantityKey, float] | None = None,
        copy_from: Unit | None = None,
        preferred_units: PreferredUnits | PreferredUnitInput = None,
    ):
        if copy_from:
            if (units) and units != copy_from.name:
                raise InconsistentDimensions()
            units = copy_from.name

        if table:
            units = _table_to_units(table=table)

        if units:
            self._name = _condense(units)
            _dimensions = _units_to_dim(units=units)
            self._dimensions = Dimensions(_dimensions)
            if dimensions and self._dimensions != dimensions:
                raise InconsistentDimensions()
            self._dimensions = self._remove_angle_as_dim(self._dimensions)

        elif dimensions:
            self._dimensions = dimensions
            if not isinstance(system, UnitSystem):
                system = UnitSystem(system=system or "SI")
            self._name = _dim_to_units(
                dimensions=dimensions,
                system=system,
                preferred_units=preferred_units,
            )
            self._dimensions = self._remove_angle_as_dim(self._dimensions)
        else:
            self._name = ""
            self._dimensions = Dimensions()

        if not config:
            config = _get_config(name=self._name)
        if config:
            for key in config:
                setattr(self, f"_{key}", config[key])

        _check_offset_unit_prefixes(self.name)
        self._si_units, self._si_scaling_factor, self._si_offset = _si_data(
            units=self.name
        )

    def _remove_angle_as_dim(self, dimensions):
        if not os.getenv("PYANSYS_UNITS_ANGLE_AS_DIMENSION", None):
            if BaseDimensions.ANGLE in dimensions._dimensions:
                del dimensions._dimensions[BaseDimensions.ANGLE]
            if BaseDimensions.SOLID_ANGLE in dimensions._dimensions:
                del dimensions._dimensions[BaseDimensions.SOLID_ANGLE]
        return dimensions

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

    def compatible_units(self) -> set[str]:
        """
        Get all units with the same dimensions.

        Returns
        -------
        set
            A set of unit objects.
        """
        compatible_units = set()
        for unit_name in {**_base_units, **_derived_units}.keys():
            unit = Unit(units=unit_name)
            if self.dimensions == unit.dimensions:
                compatible_units.add(unit.name)
        for unit_name in _quantity_units_table:
            unit = Unit(table={unit_name: 1})
            if self.dimensions == unit.dimensions:
                compatible_units.add(unit.name)
        compatible_units.discard(self.name)
        return compatible_units

    def _temp_precheck(
        self, other_unit: "Unit", op: str = "+"
    ) -> tuple["Unit", "Unit"] | None:
        """
        Validate units for temperature differences.

        Parameters
        ----------
        other_unit : Unit
            Unit for comparison against current unit.
        op : str, optional
            Operation conducted on the units.

        Returns
        -------
        Unit, Unit | None
            Two unit objects for a quantity of temperature difference or temperature.

        Raises
        ------
        ProhibitedTemperatureOperation
            Cannot add two absolute temperatures.
        IncorrectUnits
            Cannot add or subtract different units.
        """
        base = BaseDimensions
        dims = Dimensions
        temp = dims(dimensions={base.TEMPERATURE: 1})
        delta_temp = dims(dimensions={base.TEMPERATURE_DIFFERENCE: 1})
        if self.dimensions == other_unit.dimensions == temp and op == "+":
            raise ProhibitedTemperatureOperation()

        # Checks to make sure they are both temperatures.
        if (self.dimensions and other_unit.dimensions) in (temp, delta_temp):
            unit_name = self.name.removeprefix("delta_")
            relative = Unit(f"delta_{unit_name}")
            absolute = Unit(unit_name)

            if self.dimensions != other_unit.dimensions:
                # Removes the delta_ prefix if there is one.
                return absolute, relative

            if self.dimensions == other_unit.dimensions == temp and op == "-":
                return relative, absolute

        if self.dimensions != other_unit.dimensions:
            raise IncorrectUnits(self, other_unit)

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
    def has_offset(self) -> bool:
        """
        True if the unit is a non-multiplicative (offset-based) unit, such as ``C``.

        Offset units inside compound units (for example ``W m^-1 C^-1``) are
        interpreted as temperature differences and convert without an offset, so
        such compound units are multiplicative.
        """
        return self.si_offset != 0

    @property
    def is_absolute_temperature(self) -> bool:
        """True if the unit is an absolute temperature, not a difference."""
        return self.dimensions == Dimensions({BaseDimensions.TEMPERATURE: 1})

    @property
    def min_absolute_value(self) -> float | None:
        """
        Lowest physically valid value (absolute zero) in this unit.

        ``None`` if the unit is not an absolute temperature. The limit is derived
        from the unit's SI offset, so it applies to any configured temperature
        unit without referring to unit names.
        """
        if not self.is_absolute_temperature:
            return None
        return -self.si_offset

    def to_temperature_difference(self) -> "Unit":
        """
        Get the temperature difference unit matching this absolute temperature unit.

        Returns
        -------
        Unit
            Temperature difference unit with the same scaling factor.

        Raises
        ------
        ValueError
            If the unit is not an absolute temperature or has no configured
            temperature difference counterpart.
        """
        if not self.is_absolute_temperature:
            raise ValueError(f"'{self.name}' is not an absolute temperature unit.")
        candidate = f"delta_{self.name}"
        if candidate in _base_units:
            return Unit(candidate)
        for name, info in _base_units.items():
            if (
                info["type"] == "TEMPERATURE_DIFFERENCE"
                and info["si_scaling_factor"] == self.si_scaling_factor
            ):
                return Unit(name)
        raise ValueError(
            f"No temperature difference unit is configured for '{self.name}'."
        )

    @property
    def dimensions(self) -> Dimensions:
        """The units base dimensions."""
        return self._dimensions

    def convert(
        self,
        system: UnitSystem,
        preferred_units: PreferredUnits | PreferredUnitInput = None,
    ) -> Unit:
        """
        Convert a unit into the unit system.

        Parameters
        ----------
        system : UnitSystem
            Unit system to convert to.
        preferred_units : PreferredUnits, optional
            Preferred display/conversion units for derived dimensions. A plain
            unit or sequence of units is wrapped in a
            :class:`~ansys.units.preferred_units.PreferredUnits`
            automatically.

        Returns
        -------
        Unit
            Unit object converted into the unit system.

        Examples
        --------
        >>> ur = UnitRegistry()
        >>> speed_si = Unit(units= ur.m / ur.s)
        >>> bt = UnitSystem(system="BT")
        >>> speed_bt = speed_si.convert(bt)
        """
        return Unit(
            dimensions=self.dimensions,
            system=system,
            preferred_units=preferred_units,
        )

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Unit({self.name!r})"

    def __add__(self, value: "Unit") -> tuple["Unit", "Unit"]:
        return self._temp_precheck(value)

    def __mul__(self, value: "Unit") -> "Unit":
        if isinstance(value, Unit):
            offending = self if self.has_offset else value if value.has_offset else None
            if offending is not None:
                raise ProhibitedOffsetUnitOperation(offending, "*")
            new_units = f"{self.name} {value.name}"
            return _arithmetic_result(new_units)

        else:
            return NotImplemented

    @overload
    def __rmul__(
        self, value: Sequence[float] | Vector
    ) -> "Quantity[npt.NDArray[np.floating]]": ...

    @overload
    def __rmul__(self, value: float) -> "Quantity[float]": ...

    def __rmul__(self, value: Sequence[float] | Vector | float) -> "Quantity[ValT]":
        Quantity, _array = _get_quantity_and_array()
        if isinstance(value, (float, int)) or (
            _array and isinstance(value, (Sequence, _array.ndarray))
        ):
            return Quantity(value=value, units=self)
        return NotImplemented  # other cases should have already handled this so nothing to do

    def __sub__(self, value: "Unit") -> tuple["Unit", "Unit"]:
        return self._temp_precheck(value, op="-")

    def __truediv__(self, value: Unit) -> Unit:
        if not isinstance(value, Unit):
            return NotImplemented
        offending = self if self.has_offset else value if value.has_offset else None
        if offending is not None:
            raise ProhibitedOffsetUnitOperation(offending, "/")
        new_units = ""
        new_units = self.name
        for term in value.name.split():
            multiplier, base, exponent = _filter_unit_term(term)
            new_units += f" {multiplier}{base}^{exponent * -1}"
        return _arithmetic_result(new_units)

    @overload
    def __rtruediv__(
        self, value: Sequence[float] | Vector
    ) -> "Quantity[npt.NDArray[np.floating]]": ...

    @overload
    def __rtruediv__(self, value: float) -> "Quantity[float]": ...

    def __rtruediv__(self, value: Sequence[float] | Vector | float) -> "Quantity[ValT]":
        Quantity, _array = _get_quantity_and_array()
        if isinstance(value, (float, int)) or (
            _array and isinstance(value, (Sequence, _array.ndarray))
        ):
            return Quantity(value=value, units=self**-1)
        return NotImplemented  # other cases should have already handled this so nothing to do

    def __pow__(self, value: "Unit" | float) -> "Unit":
        if self.has_offset:
            raise ProhibitedOffsetUnitOperation(self, "**")
        new_units = ""
        for term in self.name.split():
            multiplier, base, exponent = _filter_unit_term(term)
            exponent *= value
            new_units += f"{multiplier}{base}^{exponent} "

        return _arithmetic_result(new_units)

    def __eq__(self, other_unit: object) -> bool:
        if not isinstance(other_unit, Unit) and self.name:
            return False
        if isinstance(other_unit, Unit):
            checks = [
                self.dimensions == other_unit.dimensions,
                self.si_offset == other_unit.si_offset,
                self.si_scaling_factor == other_unit.si_scaling_factor,
            ]
            return all(checks)
        return True

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the unit to a dictionary.

        The dictionary contains the unit name under ``"units"``. Custom units that
        are only defined in a :class:`~ansys.units.UnitRegistry` also include a
        ``"unit_definition"`` so that they can be restored without that registry.

        Examples
        --------
        >>> Unit("kg m^-3").to_dict()
        {'units': 'kg m^-3'}
        """
        from ansys.units import serialization

        return serialization.unit_to_dict(self)

    @classmethod
    def from_dict(
        cls, data: Mapping[str, Any], registry: UnitRegistry | None = None
    ) -> Unit:
        """
        Create a unit from a dictionary written by :meth:`to_dict`.

        Parameters
        ----------
        data : dict
            Serialized unit.
        registry : UnitRegistry, optional
            Registry used to resolve the unit name. Defaults to the application
            registry (see :func:`~ansys.units.set_application_registry`).
        """
        from ansys.units import serialization

        return serialization.unit_from_dict(data, registry)

    @override
    def __getstate__(self) -> dict[str, Any]:
        # Pickle by name so that units are resolved again when unpickled.
        return self.to_dict()

    def __setstate__(self, state: Mapping[str, Any]) -> None:
        if "_name" in state:
            # Pickles written before units were pickled by name.
            self.__dict__.update(state)
            return
        from ansys.units import serialization

        self.__dict__.update(serialization.unit_from_dict(state).__dict__)

    def __copy__(self) -> Unit:
        new = Unit.__new__(Unit)
        new.__dict__.update(self.__dict__)
        return new

    def __deepcopy__(self, memo: dict[int, Any]) -> Unit:
        return self.__copy__()


def _get_config(name: str) -> _BaseUnitInfo | _DerivedUnitInfo | None:
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
    system: UnitSystem | None,
    dimensions: Dimensions,
    preferred_units: PreferredUnits | PreferredUnitInput = None,
) -> str:
    """
    Convert a dimensions list into a unit string.

    Parameters
    ----------
    dimensions : Dimensions object
        Instance of Dimension class.

        system : UnitSystem object, optional
            Unit system for dimensions list.
            Default is SI units.
        preferred_units : PreferredUnits, optional
            Conversion policy deciding which named derived unit to emit for
            matching dimensions, instead of the expanded base-unit expression.

        Returns
        -------
        str
            Unit string.
    """
    if not system:
        system = UnitSystem()

    resolved_preferred_units = _coerce_preferred_units(preferred_units)
    if resolved_preferred_units:
        preferred_unit = resolved_preferred_units.unit_for(dimensions)
        if preferred_unit:
            return preferred_unit

    units = ""

    for key, value in dimensions:
        if value == 1:
            units += f"{getattr(system, key.name)} "
        elif value != 0.0:
            value = int(value) if value % 1 == 0 else value
            units += f"{getattr(system, key.name)}^{value} "

    return units.strip()


def _table_to_units(table: Mapping[QuantityKey, int]) -> str:
    """
    Convert a quantity table item into a unit string.

    Parameters
    ----------
    table : dict[str, int]
        Quantity table item to convert to a Unit.

    Returns
    -------
    Unit
        Unit object representation of a quantity table item.
    """
    for key in table.keys():
        if key not in _quantity_units_table:
            raise UnknownTableItem(key)

    base_unit = ""

    for key, value in table.items():
        terms = _quantity_units_table[key]
        for term in terms.split(" "):
            multiplier, base, exponent = _filter_unit_term(term)

            base_unit += f"{multiplier}{base}^{exponent * value} "

    return _condense(base_unit)


def _si_map(unit_term: str) -> str:
    """
    Convert a unit into its SI equivalent.

    Parameters
    ----------
    unit_term : str
        Unit term of the unit string.

    Returns
    -------
    str
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


def _condense(units: str) -> str:
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
        multiplier, unit_term, unit_term_exponent = _filter_unit_term(term)
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


def _si_data(
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
        unit_multiplier, unit_term, unit_term_exponent = _filter_unit_term(term)

        unit_term_exponent *= exponent

        si_scaling_factor *= (
            _multipliers[unit_multiplier] ** unit_term_exponent
            if unit_multiplier
            else 1.0
        )

        # Retrieve data associated with base unit
        if unit_term in _base_units:
            if unit_term_exponent == 1.0:
                si_units += f" {_si_map(unit_term)}"
            elif unit_term_exponent != 0.0:
                si_units += f" {_si_map(unit_term)}^{unit_term_exponent}"

            si_scaling_factor *= (
                _base_units[unit_term]["si_scaling_factor"] ** unit_term_exponent
            )

        # Retrieve derived unit composition unit string and SI scaling factor
        elif unit_term in _derived_units:
            si_scaling_factor *= (
                _derived_units[unit_term]["factor"] ** unit_term_exponent
            )

            # Recursively parse composition unit string
            si_units, si_scaling_factor, _ = _si_data(
                units=_derived_units[unit_term]["composition"],
                exponent=unit_term_exponent,
                si_units=si_units,
                si_scaling_factor=si_scaling_factor,
            )

    return _condense(si_units), si_scaling_factor, si_offset


def _arithmetic_result(units: str) -> Unit:
    """
    Build the unit produced by multiplying, dividing, or raising units to a power.

    Operands of these operations are never offset-based units, so any offset unit
    term they contain (for example ``C`` in ``C^2``) represents a temperature
    difference. If the terms cancel down to a bare offset unit, return the
    matching temperature difference unit rather than an absolute temperature.
    """
    unit = Unit(_condense(units))
    if unit.has_offset:
        return unit.to_temperature_difference()
    return unit


def _check_offset_unit_prefixes(name: str) -> None:
    """
    Reject multiplier prefixes on offset-based units.

    A prefix such as ``k`` in ``kC`` would scale the unit while dropping its
    offset, so the result would be neither a valid absolute temperature nor a
    temperature difference.

    Parameters
    ----------
    name : str
        Unit string representation of the quantity.

    Raises
    ------
    PrefixedOffsetUnit
        If any term is an offset-based unit with a multiplier prefix.
    """
    for term in name.split(" "):
        if not term:
            continue
        multiplier, base, _ = _filter_unit_term(term)
        base_info = _base_units.get(base)
        if multiplier and base_info and base_info["si_offset"] != 0:
            raise PrefixedOffsetUnit(term, base)


class InconsistentDimensions(ValueError):
    """Raised when units have inconsistent base dimensions."""

    def __init__(self):
        super().__init__("Unit dimensions do not match given dimensions.")


class IncorrectUnits(ValueError):
    """Raised when the specified units are incorrect."""

    def __init__(self, unit1: "Unit", unit2: "Unit"):
        super().__init__(
            f"'{unit1.si_units}' and '{unit2.si_units}' must match for this operation."
        )


class ProhibitedTemperatureOperation(TypeError):
    """Raised when two absolute temperatures are added."""

    def __init__(self, message: str | None = None):
        # The optional message lets libraries such as pandas re-raise the error
        # with extra context, which they do by calling ``type(error)(message)``.
        super().__init__(
            message
            or "In order to add two temperature-based quantities, at least one must be a temperature difference."  # noqa: E501
        )


class ProhibitedOffsetUnitOperation(TypeError):
    """Raised when an offset-based unit is used in an invalid operation."""

    def __init__(self, unit: "Unit", op: str):
        super().__init__(
            f"'{unit.name}' is a non-multiplicative (offset-based) unit and cannot be used "
            + f"with the '{op}' operation. Use a ratio-scale unit (for example 'K' or 'R') or "
            + "a temperature difference unit (for example 'delta_C') instead."
        )


class PrefixedOffsetUnit(ValueError):
    """Raised when a multiplier prefix is applied to an offset-based unit."""

    def __init__(self, term: str, base: str):
        super().__init__(
            f"'{term}' applies a multiplier prefix to the offset-based unit '{base}', "
            + f"which is not supported. Use 'delta_{base}' for a scaled temperature "
            + "difference or a ratio-scale unit (for example 'K') instead."
        )


class UnknownTableItem(ValueError):
    """Raised when a quantity table item is undefined."""

    def __init__(self, item: str):
        super().__init__(f"`{item}` is not a valid quantity table item.")
