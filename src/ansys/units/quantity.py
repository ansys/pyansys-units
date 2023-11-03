"""Provides the ``Quantity`` class."""
from __future__ import annotations

from typing import Union

import ansys.units as ansunits

try:
    import numpy as np

    _array = np.array
except ImportError:
    _array = None


class Quantity:
    """
    A class which contains a physical quantity's value and associated units.

    The value and units provided on initialization are internally converted into
    SI units to facilitate consistent computation with other quantities.

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
        if value == None and not copy_from:
            raise QuantityError.MISSING_REQUIREMENT()

        if copy_from:
            if value:
                units = copy_from.units
            else:
                units = copy_from.units
                value = copy_from.value

        if _array and not isinstance(value, (float, int)):
            self._value = np.array(value)
        elif not _array and not isinstance(value, (float, int)):
            raise QuantityError.REQUIRES_NUMPY()
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
            raise QuantityError.INCOMPATIBLE_DIMENSIONS(
                from_unit=self.units, to_unit=to_units
            )

        return Quantity(value=new_value, units=to_units)

    def __float__(self):
        return self.value

    def __array__(self):
        if _array:
            if isinstance(self.value, (float)):
                return np.array([self.value])
            return self.value
        else:
            raise QuantityError.REQUIRES_NUMPY()

    def __getitem__(self, idx):
        if _array:
            value = self.__array__()[idx]
            return Quantity(value, self.units)
        else:
            raise QuantityError.REQUIRES_NUMPY()

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

    def __gt__(self, __value):
        if isinstance(__value, ansunits.Quantity):
            self.dimensions > __value.dimensions
        elif not self.is_dimensionless:
            raise QuantityError.INCOMPARABLE_QUANTITIES(self, __value)
        return float(self) > float(__value)

    def __ge__(self, __value):
        if isinstance(__value, ansunits.Quantity):
            self.dimensions >= __value.dimensions
        elif not self.is_dimensionless:
            raise QuantityError.INCOMPARABLE_QUANTITIES(self, __value)
        return float(self) >= float(__value)

    def __lt__(self, __value):
        if isinstance(__value, ansunits.Quantity):
            self.dimensions < __value.dimensions
        elif not self.is_dimensionless:
            raise QuantityError.INCOMPARABLE_QUANTITIES(self, __value)
        return float(self) < float(__value)

    def __le__(self, __value):
        if isinstance(__value, ansunits.Quantity):
            self.dimensions <= __value.dimensions
        elif not self.is_dimensionless:
            raise QuantityError.INCOMPARABLE_QUANTITIES(self, __value)
        return float(self) <= float(__value)

    def __eq__(self, __value):
        if not self.is_dimensionless and not isinstance(__value, ansunits.Quantity):
            raise QuantityError.INCOMPARABLE_QUANTITIES(self, __value)
        elif float(self) != float(__value):
            return False
        elif isinstance(__value, ansunits.Quantity):
            if self.dimensions != __value.dimensions:
                return False
        return True

    def __ne__(self, __value):
        return not self.__eq__(__value)


class QuantityError(ValueError):
    """Custom quantity errors."""

    def __init__(self, err):
        super().__init__(err)

    @classmethod
    def EXCESSIVE_PARAMETERS(cls):
        return cls(
            "Quantity only accepts one of the following parameters: \
            (units) or (quantity_map) or (dimensions)."
        )

    @classmethod
    def MISSING_REQUIREMENT(cls):
        return cls("Requires at least one 'value' or 'copy_from' argument.")

    @classmethod
    def INCOMPATIBLE_DIMENSIONS(cls, from_unit, to_unit):
        return cls(
            f"`{from_unit.name}` and `{to_unit.name}` have incompatible dimensions."
        )

    @classmethod
    def INCOMPATIBLE_VALUE(cls, value):
        return cls(f"`{value}` is incompatible with the current quantity object.")

    @classmethod
    def INCOMPARABLE_QUANTITIES(cls, q1, q2):
        return cls(f"'{q1}' cannot be compared to '{q2}' in this manner.")

    @classmethod
    def REQUIRES_NUMPY(cls):
        return cls(f"To use arrays and lists install numpy.")
