# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
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
"""Provides the ``Quantity`` class."""

from __future__ import annotations

from collections.abc import Callable, Iterator, Mapping, Sequence
import operator
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    Protocol,
    TypeVar,
    overload,
    runtime_checkable,
)

from ansys.units.base_dimensions import BaseDimensions
from ansys.units.dimensions import Dimensions
from ansys.units.quantity_tables.keys import QuantityKey, UnitKey
from ansys.units.systems import UnitSystem
from ansys.units.unit import Unit

try:
    import numpy as np

    _array = np
except ImportError:
    _array = None

try:
    from pydantic_core import core_schema

    _core_schema = core_schema
except ImportError:
    _core_schema = None

try:
    from matplotlib.units import AxisInfo, ConversionInterface, registry

    _ci = ConversionInterface
    _ai = AxisInfo
    _registry = registry
except ImportError:
    _ci, _ai, _registry = object, None, dict()


@runtime_checkable
class ArrayLike(Protocol):
    """Protocol for numpy-like arrays."""

    def __getitem__(self, idx: int) -> object: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator["SupportsRichComparison"]: ...
    def __add__(self, other: float | ArrayLike) -> "Self": ...
    def __sub__(self, other: float | ArrayLike) -> "Self": ...
    def __neg__(self) -> "Self": ...
    def __mul__(self, other: float | ArrayLike) -> "Self": ...
    def __rmul__(self, other: float | ArrayLike) -> "Self": ...
    def __pow__(self, other: float) -> "Self": ...
    def __truediv__(self, other: float | ArrayLike) -> "Self": ...
    def __rtruediv__(self, other: float | ArrayLike) -> "Self": ...
    def __lt__(self, other: float | ArrayLike) -> bool: ...
    def tolist(self) -> Sequence[object]: ...


if TYPE_CHECKING:
    from _typeshed import SupportsRichComparison
    from typing_extensions import Self, TypeVar

    ValT = TypeVar(
        "ValT",
        bound=float | ArrayLike,
        default=float | ArrayLike,
        covariant=True,
    )
else:
    ValT = TypeVar("ValT")


class Quantity(Generic[ValT]):
    """
    A class representing a physical quantity's value and associated units.

    A Quantity object can be instantiated from a NumPy array or list only if the
    ``NumPy`` package is installed.

    The value argument is not required when using ``copy_from``. A value can be given
    to override the value from the copy.

    Implicit conversion from Quantity to float is only allowed if the operand is
    of quantity type angle or dimensionless.

    Parameters
    ----------
    value : int, float, list, np.array
        Real value of the quantity.
    units : str, Unit, optional
        Initializes the quantity's units using a string or ``Unit`` instance.
    quantity_table : dict[str, int], optional
        Initializes the quantity's units using the quantity table.
    dimensions : Dimensions, optional
        Initializes the quantity's units in SI using a ``Dimensions`` instance.
    copy_from : Quantity, optional
        An existing ``Quantity`` instance.

    Attributes
    ----------
    value
    units
    dimensions
    is_dimensionless
    """

    _chosen_units = []

    @overload
    def __init__(
        self,
        value: ValT,
        units: Unit | UnitKey | str | None = None,
    ) -> None: ...

    @overload
    def __init__(
        self,
        value: ValT,
        *,
        dimensions: Dimensions,
    ) -> None: ...

    @overload
    def __init__(
        self,
        value: ValT,
        *,
        quantity_table: Mapping[QuantityKey, float],
    ) -> None: ...

    @overload
    def __init__(
        self,
        *,
        copy_from: "Quantity[ValT]",
    ) -> None: ...

    @overload
    def __init__(
        self,
        value: ValT,
        *,
        copy_from: "Quantity",
    ) -> None: ...

    def __init__(
        self,
        value: ValT | None = None,
        units: Unit | str | None = None,
        *,
        quantity_table: Mapping[QuantityKey, float] | None = None,
        dimensions: Dimensions | None = None,
        copy_from: Quantity | None = None,
        **kwargs: Any,
    ):
        if (
            (units and quantity_table)
            or (units and dimensions)
            or (quantity_table and dimensions)
        ):
            raise ExcessiveParameters()

        self._value = value
        self.unit = units

        if copy_from:
            if value:
                units = copy_from.units
            else:
                units = copy_from.units
                value = copy_from.value
        elif value is None:
            raise InsufficientArguments()

        if not isinstance(value, (float, int)):
            if isinstance(value, str):
                raise TypeError("value should be either float, int or [float, int].")
            if _array:
                if isinstance(value, _array.ndarray):
                    self._value = value
                else:
                    self._value = _array.array(value)
            elif not _array:
                raise NumPyRequired()
        else:
            self._value = float(value)

        if quantity_table:
            units = Unit(table=quantity_table)

        if dimensions:
            units = Unit(dimensions=dimensions)

        if not isinstance(units, Unit):
            units = Unit(units)

        min_value = value if isinstance(value, (int, float)) else min(value)

        if (
            (units.name in ["K", "R"] and value < 0)
            or (units.name == "C" and min_value < -273.15)
            or (units.name == "F" and min_value < -459.67)
        ):
            units = Unit(f"delta_{units.name}")

        self._unit = units

        for unit in self._chosen_units:
            if unit.name != units.name and self.dimensions == unit.dimensions:
                self._value = self.to(unit).value
                self._unit = unit

        self.extra_fields = kwargs

    @classmethod
    def preferred_units(
        cls, units: Sequence[Unit | UnitKey], remove: bool = False
    ) -> None:
        """
        Add or remove preferred units.

        Quantities are automatically converted to preferred units when the
        quantity is initialized. Conversion is always carried out if the base
        units are consistent with the preferred units.

        Each preferred unit must have unique dimensions. To override units with
        the same dimensions, the original must first be removed.

        Parameters
        ----------
        units : list
            A list of units to be added or removed.
        remove : bool
            Specify if the units should be removed.
        """
        for unit in units:
            if isinstance(unit, str):
                unit = Unit(units=unit)
            if remove and unit in cls._chosen_units:
                cls._chosen_units.remove(unit)
            elif not remove:
                for chosen_unit in cls._chosen_units:
                    if chosen_unit.dimensions == unit.dimensions:
                        raise RequiresUniqueDimensions(unit, chosen_unit)
                cls._chosen_units.append(unit)

    @property
    def value(self) -> ValT:
        """Value in contained units."""
        return self._value

    @property
    def units(self) -> Unit:
        """The quantity's units."""
        return self._unit

    @property
    def dimensions(self) -> Dimensions:
        """The quantity's dimensions."""
        return self._unit.dimensions

    @property
    def is_dimensionless(self) -> bool:
        """True if the quantity is dimensionless."""
        return not bool(self.dimensions)

    def to(self, to_units: Unit | str) -> "Quantity":
        """
        Perform quantity conversions.

        Parameters
        ----------
        to_units : Unit or str
            Desired unit to convert to.

        Returns
        -------
        Quantity
            Quantity instance in the desired units.

        Examples
        --------
        >>> speed_si = Quantity(value=5, units="m s^-1")
        >>> speed_bt = speed_si.to("ft s^-1")
        """

        if not isinstance(to_units, Unit):
            to_units = Unit(units=to_units)

        # Retrieve all SI required SI data and perform conversion
        new_value = (
            get_si_value(self) / to_units.si_scaling_factor
        ) - to_units.si_offset

        if self.dimensions != to_units.dimensions:
            raise IncompatibleDimensions(from_unit=self.units, to_unit=to_units)

        return Quantity(value=new_value, units=to_units)

    def compatible_units(self) -> set[str]:
        """
        Get all units with the same dimensions.

        Returns
        -------
        set
            A set of unit objects.
        """

        return self.units.compatible_units()

    def convert(self, system: UnitSystem) -> Quantity:
        """
        Convert a quantity into the unit system.

        Parameters
        ----------
        system : UnitSystem
            Unit system to convert to.

        Returns
        -------
        Quantity
            Quantity object converted into the unit system.

        Examples
        --------
        >>> ur = UnitRegistry()
        >>> speed_si = Quantity(value=5, units= ur.m / ur.s)
        >>> bt = UnitSystem(system="BT")
        >>> speed_bt = speed_si.convert(bt)
        """
        new_unit = self.units.convert(system)

        return self.to(to_units=new_unit)

    def _relative_unit_check(
        self,
        _other: Quantity[ValT] | float,
        r_add_sub: bool,
        op: Callable[[Any, Any], Any] = operator.add,
    ) -> Quantity[ValT]:
        """
        Checks relative units for temperature differences.

        Parameters
        ----------
        other : float, int, Quantity
            The value to be added or subtracted to self.
        r_add_sub : bool
            Whether called in __radd__ or __rsub__.
        op : operator, optional
            The operation being performed. Default is addition.

        Returns
        -------
        Quantity
            Quantity instance changed to or from relative units.
        """
        other = _other if isinstance(_other, Quantity) else Quantity(_other)

        # Checks the temperatures at the unit level.
        new_units, other_units = op(self.units, other.units) or (
            self.units,
            other.units,
        )

        # If value does not equal relative units, use the corrected absolute units.
        if other.units.dimensions != other_units.dimensions:
            value = other.to(new_units).value
        # If both values are temperatures, use the corrected relative units.
        elif other.units.dimensions != self.units.dimensions:
            value = other.to(other_units).value
        else:
            value = (
                other.to(other_units).value if r_add_sub else other.to(self.units).value
            )

        new_value = op(self.value, value)
        if r_add_sub:
            return Quantity(value=new_value, units=other_units)
        return Quantity(value=new_value, units=new_units)

    def __float__(self: Quantity[float]) -> float:
        base_dims = BaseDimensions
        dims = Dimensions
        if self.dimensions in [
            dims(),
            dims(dimensions={base_dims.ANGLE: 1.0}),
            dims(dimensions={base_dims.SOLID_ANGLE: 1.0}),
        ]:
            return get_si_value(self)
        raise ValueError(
            "Cannot convert to a float as the Quantity is not dimensionless or a (solid) angle"
        )

    def __getitem__(self: Quantity[ArrayLike], idx: int) -> Quantity[float]:
        return Quantity(value=float(self.value[idx]), units=self.units)

    def __str__(self):
        return f"{self.value} {self.units.name}"

    def __repr__(self):
        return f'Quantity({self.value}, "{self.units.name}")'

    def __pow__(self, other: float) -> Quantity["ValT"]:
        new_value = self.value**other
        new_units = self.units**other
        return Quantity(value=new_value, units=new_units)

    def __mul__(self, other: "Quantity" | Unit | float | int) -> "Quantity":
        if isinstance(other, Quantity):
            new_value = self.value * other.value
            new_units = self._unit * other._unit
            return Quantity(
                value=new_value,
                units=new_units,
            )
        if isinstance(other, Unit):
            base_quantity = Quantity(1, other)
            return self * base_quantity

        if isinstance(other, (float, int)):
            return Quantity(value=self.value * other, units=self.units)
        return NotImplemented

    __rmul__ = __mul__

    def __truediv__(self, other: "Quantity | float | Unit") -> "Quantity":
        if isinstance(other, Quantity):
            new_value = self.value / other.value
            new_units = self._unit / other._unit
            return Quantity(
                value=new_value,
                units=new_units,
            )

        if isinstance(other, Unit):
            base_quantity = Quantity(1, other)
            return self / base_quantity

        if isinstance(other, (float, int)):
            return Quantity(value=self.value / other, units=self._unit)
        return NotImplemented

    def __rtruediv__(self, other: "Quantity | float | Unit") -> "Quantity":
        return Quantity(other, "") / self

    def __add__(self, other):
        return self._relative_unit_check(other, r_add_sub=False)

    def __radd__(self, other):
        return self._relative_unit_check(other, r_add_sub=True)

    def __sub__(self, other):
        return self._relative_unit_check(other, r_add_sub=False, op=operator.sub)

    def __rsub__(self, other):
        return self._relative_unit_check(other, r_add_sub=True, op=operator.sub)

    def __neg__(self):
        return Quantity(-self.value, self._unit)

    def validate_matching_dimensions(self, other):
        """Validates dimensions of quantities."""
        if isinstance(other, Quantity) and (self.dimensions != other.dimensions):
            raise IncompatibleDimensions(from_unit=self.units, to_unit=other.units)
        elif (
            (not self.is_dimensionless)
            and (not isinstance(other, Quantity))
            and isinstance(other, (float, int))
        ):
            raise IncompatibleQuantities(self, other)

    def _compute_single_value_comparison(
        self, other: Quantity, op: Callable[[Any, Any], bool]
    ):
        """Compares quantity values."""
        return (
            op(get_si_value(self), other)
            if self.is_dimensionless
            else op(get_si_value(self), get_si_value(other))
        )

    def __gt__(self, other: Quantity) -> bool:
        self.validate_matching_dimensions(other)
        return self._compute_single_value_comparison(other, op=operator.gt)

    def __ge__(self, other: Quantity) -> bool:
        self.validate_matching_dimensions(other)
        return self._compute_single_value_comparison(other, op=operator.ge)

    def __lt__(self, other: Quantity) -> bool:
        self.validate_matching_dimensions(other)
        return self._compute_single_value_comparison(other, op=operator.lt)

    def __le__(self, other: Quantity) -> bool:
        self.validate_matching_dimensions(other)
        return self._compute_single_value_comparison(other, op=operator.le)

    def __eq__(self, other) -> bool:
        self.validate_matching_dimensions(other)
        if all(
            (
                isinstance(self.value, float),
                any(
                    (
                        isinstance(x, float)
                        for x in (other, getattr(other, "value", None))
                    )
                ),
            )
        ):
            return self._compute_single_value_comparison(other, op=operator.eq)
        # no type-checking here since array_equal happily processes anything
        return (
            _array
            and _array.array_equal(get_si_value(self), get_si_value(other))
            or False
        )

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        """Define the pydantic core schema for QuantityPydanticAdapter."""

        def validate_quantity_type(obj):
            if isinstance(obj, cls):
                return obj
            if isinstance(obj, Quantity):
                return cls(
                    value=(
                        obj._value.tolist()
                        if hasattr(obj._chosen_unitsvalue, "tolist")
                        else obj.value
                    ),
                    units=obj.units.name,
                )
            if isinstance(obj, dict):
                value = obj.get("value")
                units = obj.get("units")
                extras = {k: v for k, v in obj.items() if k not in {"value", "units"}}
                return cls(value=value, units=units, **extras)
            raise TypeError(
                "Expected dict, Quantity, or QuantityPydanticAdapter instance."
            )

        def serialize(instance):
            base = {"value": instance.value, "units": instance.units.name}
            return {**base, **instance.extra_fields}

        if _core_schema is None:
            raise PydanticRequired()

        return _core_schema.no_info_plain_validator_function(
            validate_quantity_type,
            json_schema_input_schema=_core_schema.model_fields_schema(
                {
                    "value": _core_schema.list_schema(
                        items_schema=_core_schema.float_schema()
                    ),
                    "units": _core_schema.str_schema(),
                },
                extras_schema=_core_schema.any_schema(),
            ),
            serialization=_core_schema.plain_serializer_function_ser_schema(
                serialize, return_schema=_core_schema.dict_schema()
            ),
        )


def get_si_value(quantity: Quantity[ValT]) -> ValT:
    """Returns a quantity's value in SI units."""

    def _convert(value: float, offset: float, factor: float):
        return float((value + offset) * factor)

    if isinstance(quantity.value, float):
        return _convert(
            quantity.value, quantity.units.si_offset, quantity.units.si_scaling_factor
        )
    if _array and isinstance(quantity.value, _array.ndarray):
        offset = quantity.units.si_offset
        factor = quantity.units.si_scaling_factor
        return _array.array([_convert(x, offset, factor) for x in quantity.value])
    raise ValueError(
        (
            "quantity cannot be converted to a meaningful SI representation. "
            "Perhaps you didn't install numpy"
        )
    )


class ExcessiveParameters(ValueError):
    """Raised when excessive parameters are provided."""

    def __init__(self):
        super().__init__(
            "Quantity only accepts one of the following parameters: \
            (units) or (quantity_table) or (dimensions)."
        )


class InsufficientArguments(ValueError):
    """Raised when insufficient arguments are provided."""

    def __init__(self):
        super().__init__("Requires at least one 'value' or 'copy_from' argument.")


class IncompatibleDimensions(ValueError):
    """Raised when dimensions are incompatible."""

    def __init__(self, from_unit, to_unit):
        super().__init__(
            f"`{from_unit.name}` and `{to_unit.name}` have incompatible dimensions."
        )


class IncompatibleValue(ValueError):
    """Raised when an incompatible value is provided."""

    def __init__(self, value):
        super().__init__(f"`{value}` is incompatible with the current quantity object.")


class IncompatibleQuantities(ValueError):
    """Raised when quantities are incompatible."""

    def __init__(self, q1, q2):
        super().__init__(f"'{q1}' and '{q2}' are incompatible.")


class NumPyRequired(ModuleNotFoundError):
    """Raised when NumPy is unavailable."""

    def __init__(self):
        super().__init__("To use NumPy arrays and lists install NumPy.")


class PydanticRequired(ModuleNotFoundError):
    """Raised when pydantic or pydantic_core is unavailable."""

    def __init__(self):
        super().__init__(
            "To use pydantic features, install it using 'pip install ansys-units[additional]'."
        )


class InvalidFloatUsage(FloatingPointError):
    """Raised when float is unsupported for given type of quantity."""

    def __init__(self):
        super().__init__(
            "Only dimensionless quantities and angles can be used as a float."
        )


class RequiresUniqueDimensions(ValueError):
    """Raised when two units with the same dimensions are added to the chosen units."""

    def __init__(self, unit, other_unit):
        super().__init__(
            f"For '{unit.name}' to be added '{other_unit.name}' must be removed."
        )


class QuantityConverter(_ci):
    @staticmethod
    def convert(value, unit, axis):
        if isinstance(value, Quantity):
            return value._value
        else:
            return [quantity._value for quantity in value]

    @staticmethod
    def axisinfo(unit, axis):
        return _ai(label=unit)

    @staticmethod
    def default_units(x, axis):
        "Return the default unit for x or None"
        if isinstance(x, Quantity):
            attr = getattr(x, "unit", None)
        else:
            attr = getattr(x[0], "unit", None)
        return attr.name if isinstance(attr, Unit) else attr


_registry[Quantity] = QuantityConverter()
