"""Provides the ``Quantity`` class."""
from __future__ import annotations

from typing import Union

import ansys.units as ansunits

try:
    import numpy as np

    _array = np
except ImportError:
    _array = None


class ExcessiveParameters(ValueError):
    """Provides the error when excessive parameters are provided."""

    def __init__(self):
        super().__init__(
            "Quantity only accepts one of the following parameters: \
            (units) or (quantity_map) or (dimensions)."
        )


class InsufficientArguments(ValueError):
    """Provides the error when insufficient arguments are provided."""

    def __init__(self):
        super().__init__("Requires at least one 'value' or 'copy_from' argument.")


class IncompatibleDimensions(ValueError):
    """Provides the error when dimensions are incompatible."""

    def __init__(self, from_unit, to_unit):
        super().__init__(
            f"`{from_unit.name}` and `{to_unit.name}` have incompatible dimensions."
        )


class IncompatibleValue(ValueError):
    """Provides the error when an incompatible value is provided."""

    def __init__(self, value):
        super().__init__(f"`{value}` is incompatible with the current quantity object.")


class IncompatibleQuantities(ValueError):
    """Provides the error when quantities are incompatible."""

    def __init__(self, q1, q2):
        super().__init__(f"'{q1}' and '{q2}' are incompatible.")


class NumpyRequired(ModuleNotFoundError):
    def __init__(self):
        super().__init__("To use NumPy arrays and lists install NumPy.")


class InvalidFloatUsage(FloatingPointError):
    def __init__(self):
        super().__init__(
            "Only dimensionless quantities and angles can be used as a float."
        )


class Quantity:
    """
    A class which contains a physical quantity's value and associated units.

    A Quantity instance will contain both SI units and the SI value to
    facilitate consistent computation with other quantities. ``NumPy`` is
    required to use lists or NumPy arrays. Value is not required when using
    ``copy_from``.

    Float conversion will only work for angles or dimensionless quantities.

    Parameters
    ----------
    value : int | float | list | np.array
        Real value of the quantity.
    units : str, Unit, optional
        Initializes the quantity's units using a string or ``Unit`` instance.
    quantity_map : dict, optional
        Initializes the quantity's units using the quantity map.
    dimensions : Dimensions, optional
        Initializes the quantity's units in SI using a ``Dimensions`` instance.
    copy_from : Quantity, optional
        An existing ``Quantity`` instance.

    Attributes
    ----------
    value
    units
    si_value
    si_units
    dimensions
    is_dimensionless
    """

    def __init__(
        self,
        value: Union[int, float] = None,
        units: Union[ansunits.Unit, str] = None,
        quantity_map: dict = None,
        dimensions: ansunits.Dimensions = None,
        copy_from: ansunits.Quantity = None,
    ):
        if (
            (units and quantity_map)
            or (units and dimensions)
            or (quantity_map and dimensions)
        ):
            raise ExcessiveParameters()

        if copy_from:
            if value:
                units = copy_from.units
            else:
                units = copy_from.units
                value = copy_from.value
        elif value is None:
            raise InsufficientArguments()

        if not isinstance(value, (float, int)):
            if _array:
                if isinstance(value, _array.ndarray):
                    self._value = value
                else:
                    self._value = _array.array(value)
            elif not _array:
                raise NumpyRequired()
        else:
            self._value = float(value)

        if quantity_map:
            units = ansunits.QuantityMap(quantity_map).units

        if dimensions:
            units = ansunits.Unit(dimensions=dimensions)

        if not isinstance(units, ansunits.Unit):
            units = ansunits.Unit(units)

        if (
            (units.name in ["K", "R"] and value < 0)
            or (units.name == "C" and value < -273.15)
            or (units.name == "F" and value < -459.67)
        ):
            units = ansunits.Unit(f"delta_{units.name}")

        self._unit = units

    @property
    def value(self):
        """Real value."""
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    @property
    def units(self):
        """Unit Object."""
        return self._unit

    @property
    def si_value(self):
        """SI conversion value."""
        return (self.value + self._unit.si_offset) * self._unit.si_scaling_factor

    @property
    def si_units(self):
        """SI conversion unit string."""
        return self._unit._si_units

    @property
    def dimensions(self):
        """Dimensions Object."""
        return self._unit.dimensions

    @property
    def is_dimensionless(self):
        """True if the quantity is dimensionless."""
        return not bool(self.dimensions)

    def to(self, to_units: Union[ansunits.Unit, str]) -> "Quantity":
        """
        Perform quantity conversions.

        Parameters
        ----------
        to_units : Unit
            Desired unit to convert to.

        Returns
        -------
        Quantity
            Quantity object containing the desired quantity conversion.
        """

        if not isinstance(to_units, ansunits.Unit):
            to_units = ansunits.Unit(units=to_units)

        # Retrieve all SI required SI data and perform conversion
        new_value = (self.si_value / to_units.si_scaling_factor) - to_units.si_offset

        if self.dimensions != to_units.dimensions:
            raise IncompatibleDimensions(from_unit=self.units, to_unit=to_units)

        return Quantity(value=new_value, units=to_units)

    def __float__(self):
        base_dims = ansunits.BaseDimensions
        dims = ansunits.Dimensions
        if self.dimensions in [
            dims(),
            dims(dimensions={base_dims.ANGLE: 1.0}),
            dims(dimensions={base_dims.SOLID_ANGLE: 1.0}),
        ]:
            return self.si_value
        raise InvalidFloatUsage()

    def __array__(self):
        if _array:
            if isinstance(self.value, (float)):
                return _array.array([self.value])
            return self.value
        else:
            raise NumpyRequired()

    def __getitem__(self, idx):
        if _array:
            value = self.__array__()[idx]
            return Quantity(value, self.units)
        else:
            raise NumpyRequired()

    def __str__(self):
        return f'({self.value}, "{self._unit.name}")'

    def __repr__(self):
        return f'Quantity ({self.value}, "{self._unit.name}")'

    def __pow__(self, __value):
        new_value = self.value**__value
        new_units = self._unit**__value
        return Quantity(value=new_value, units=new_units)

    def __mul__(self, __value):
        if isinstance(__value, Quantity):
            new_value = self.value * __value.value
            new_units = self._unit * __value._unit
            return Quantity(
                value=new_value,
                units=new_units,
            )
        if isinstance(__value, ansunits.Unit):
            base_quantity = Quantity(1, __value)
            return self * base_quantity

        if isinstance(__value, (float, int)):
            return Quantity(value=self.value * __value, units=self.units)

    def __rmul__(self, __value):
        return self.__mul__(__value)

    def __truediv__(self, __value):
        if isinstance(__value, Quantity):
            new_value = self.value / __value.value
            new_units = self._unit / __value._unit
            return Quantity(
                value=new_value,
                units=new_units,
            )

        if isinstance(__value, ansunits.Unit):
            base_quantity = Quantity(1, __value)
            return self / base_quantity

        if isinstance(__value, (float, int)):
            return Quantity(value=self.value / __value, units=self._unit)

    def __rtruediv__(self, __value):
        return Quantity(__value, "") / self

    def __add__(self, __value):
        if not isinstance(__value, ansunits.Quantity):
            __value = ansunits.Quantity(__value)
        new_units = (self._unit + __value._unit) or self.units
        new_value = self.value + __value.value
        return Quantity(value=new_value, units=new_units)

    def __radd__(self, __value):
        return self.__add__(__value)

    def __sub__(self, __value):
        if not isinstance(__value, ansunits.Quantity):
            __value = ansunits.Quantity(__value)
        new_units = (self._unit - __value._unit) or self.units
        new_value = self.value - __value.value
        return Quantity(value=new_value, units=new_units)

    def __rsub__(self, __value):
        return self.__sub__(__value)

    def __neg__(self):
        return Quantity(-self.value, self._unit)

    def validate_matching_dimensions(self, other):
        """Validate dimensions of quantities."""
        if isinstance(other, Quantity) and (self.dimensions != other.dimensions):
            raise IncompatibleDimensions(from_unit=self.units, to_unit=other.units)
        elif (
            (not self.is_dimensionless)
            and (not isinstance(other, Quantity))
            and isinstance(other, (float, int))
        ):
            raise IncompatibleQuantities(self, other)

    def __gt__(self, __value):
        if isinstance(__value, ansunits.Quantity):
            self.dimensions > __value.dimensions
            return self.si_value > __value.si_value
        elif not self.is_dimensionless:
            raise IncompatibleQuantities(self, __value)
        else:
            return self.si_value > __value

    def __ge__(self, __value):
        if isinstance(__value, ansunits.Quantity):
            self.dimensions >= __value.dimensions
            return self.si_value >= __value.si_value
        elif not self.is_dimensionless:
            raise IncompatibleQuantities(self, __value)
        else:
            return self.si_value >= __value

    def __lt__(self, __value):
        if isinstance(__value, ansunits.Quantity):
            self.dimensions < __value.dimensions
            return self.si_value < __value.si_value
        elif not self.is_dimensionless:
            raise IncompatibleQuantities(self, __value)
        else:
            return self.si_value < __value

    def __le__(self, __value):
        print(self)
        if isinstance(__value, ansunits.Quantity):
            self.dimensions <= __value.dimensions
            return self.si_value <= __value.si_value
        elif not self.is_dimensionless:
            raise IncompatibleQuantities(self, __value)
        else:
            return self.si_value <= __value

    def __eq__(self, __value):
        if not self.is_dimensionless and not isinstance(__value, ansunits.Quantity):
            return False
        if isinstance(__value, ansunits.Quantity):
            if (
                self.si_value == __value.si_value
                and self.dimensions == __value.dimensions
            ):
                return True
            return False
        return self.si_value == __value

    def __ne__(self, __value):
        return not self.__eq__(__value)
