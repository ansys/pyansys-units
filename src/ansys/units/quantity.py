"""Provides the ``Quantity`` class."""
from typing import Optional

import ansys.units as ansunits
from ansys.units.utils import si_data


class Quantity(float):
    """
    Instantiates a physical quantity using a real value and units.

    All instances of this class are converted to the base SI unit system
    to have consistency in arithmetic operations.

    Parameters
    ----------
    value : int | float
        Real value of the quantity.
    units : str, Unit, optional
        Unit string representation of the quantity.
    quantity_map : dict, optional
        Quantity map representation of the quantity.
    dimensions : Dimensions, optional
        Dimensions representation of the quantity.

    Methods
    -------
    to()
        Convert to a given unit string.

    Returns
    -------
    Quantity
        Quantity instance.
    """

    def __new__(
        cls,
        value,
        units=None,
        quantity_map=None,
        dimensions: ansunits.Dimensions = None,
    ):
        if (
            (units and quantity_map)
            or (units and dimensions)
            or (quantity_map and dimensions)
        ):
            raise QuantityError.EXCESSIVE_PARAMETERS()

        _value = float(value)

        if units is not None:
            _unit = units

        if quantity_map:
            units = ansunits.QuantityMap(quantity_map).units
            _unit = units

        if dimensions:
            _unit = ansunits.Unit(dimensions=dimensions)

        if not isinstance(_unit, ansunits.Unit):
            _unit = ansunits.Unit(_unit)

        _, si_multiplier, si_offset = si_data(units=_unit.name)
        _si_value = (_value + si_offset) * si_multiplier

        return float.__new__(cls, _si_value)

    def __init__(
        self,
        value,
        units=None,
        quantity_map=None,
        dimensions: ansunits.Dimensions = None,
    ):
        if (
            (units and quantity_map)
            or (units and dimensions)
            or (quantity_map and dimensions)
        ):
            raise QuantityError.EXCESSIVE_PARAMETERS()

        self._value = float(value)

        if units is not None:
            self._unit = units

        if quantity_map:
            units = ansunits.QuantityMap(quantity_map).units
            self._unit = units

        if dimensions:
            self._unit = ansunits.Unit(dimensions=dimensions)

        if not isinstance(self._unit, ansunits.Unit):
            self._unit = ansunits.Unit(self._unit)

        if (
            (self._unit.name in ["K", "R"] and value < 0)
            or (self._unit.name == "C" and value < -273.15)
            or (self._unit.name == "F" and value < -459.67)
        ):
            self._unit = ansunits.Unit(f"delta_{self._unit.name}")

        si_units, si_multiplier, si_offset = si_data(units=self._unit.name)

        self._si_units = si_units

        self._si_value = (self.value + si_offset) * si_multiplier

    def _arithmetic_precheck(self, __value) -> str:
        """
        Validate dimensions of the quantity.

        Parameters
        ----------
        __value : Quantity | int | float
            Value for modifying the current ``Quantity`` object.
        """

        # Cannot perform operations between quantities with incompatible dimensions
        if isinstance(__value, Quantity) and self.dimensions != __value.dimensions:
            raise QuantityError.INCOMPATIBLE_DIMENSIONS(self.units, __value.units)
        # Cannot perform operations on a non-dimensionless quantity

        if not isinstance(__value, Quantity) and not self.is_dimensionless:
            raise QuantityError.INCOMPATIBLE_VALUE(__value)

    def _temp_precheck(self, units, op: str = None) -> Optional[str]:
        """
        Validate units for temperature differences.

        Parameters
        ----------
        units : Unit
            Unit for comparison against current units.
        op : str, None
            Operation conducted on units. "+"|"-"

        Returns
        -------
        str | None
            Units of temperature difference.
        """
        temp = ["K", "C", "F", "R"]
        delta_temp = ["delta_K", "delta_C", "delta_F", "delta_R"]
        if op == "-" and self.units in temp and units in temp:
            return delta_temp[temp.index(self.units)]
        elif self.units in delta_temp and units in temp:
            return temp[delta_temp.index(self.units)]

    @property
    def value(self):
        """Real value."""
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    @property
    def units(self):
        """Unit string."""
        return self._unit.name

    @property
    def si_value(self):
        """SI conversion value."""
        return self._si_value

    @property
    def si_units(self):
        """SI conversion unit string."""
        return self._si_units

    @property
    def dimensions(self):
        """Dimensions."""
        return self._unit.dimensions

    @property
    def is_dimensionless(self):
        """Dimensions."""
        return not bool(self._unit.dimensions.dimensions)

    def to(self, to_units: [str, any]) -> "Quantity":
        """
        Perform quantity conversions.

        Parameters
        ----------
        to_units : str, Unit
            Desired unit to convert to.

        Returns
        -------
        Quantity
            Quantity object containing the desired quantity conversion.
        """
        if isinstance(to_units, ansunits.Unit):
            to_units = to_units.name

        if not isinstance(to_units, str):
            raise TypeError("`to_units` should be a `str` type.")

        # Retrieve all SI required SI data and perform conversion
        _, si_multiplier, si_offset = si_data(to_units)
        new_value = (self.si_value / si_multiplier) - si_offset

        new_obj = Quantity(value=new_value, units=to_units)

        # Confirm conversion compatibility
        self._arithmetic_precheck(new_obj)

        return new_obj

    def __str__(self):
        return f'({self.value}, "{self.units}")'

    def __repr__(self):
        return f'Quantity ({self.value}, "{self.units}")'

    def __pow__(self, __value):
        new_si_value = self.si_value**__value
        new_units = self._unit**__value
        return Quantity(value=new_si_value, units=new_units)

    def __mul__(self, __value):
        if isinstance(__value, Quantity):
            new_si_value = self.si_value * __value.si_value
            new_units = self._unit * __value._unit
            return Quantity(
                value=new_si_value,
                units=new_units,
            )
        if isinstance(__value, ansunits.Unit):
            base_quantity = Quantity(1, __value)
            return self * base_quantity

        if isinstance(__value, (float, int)):
            return Quantity(value=self.si_value * __value, units=self.si_units)

    def __rmul__(self, __value):
        return self.__mul__(__value)

    def __truediv__(self, __value):
        if isinstance(__value, Quantity):
            new_si_value = self.si_value / __value.si_value
            new_units = self._unit / __value._unit
            return Quantity(
                value=new_si_value,
                units=new_units,
            )

        if isinstance(__value, ansunits.Unit):
            base_quantity = Quantity(1, __value)
            return self / base_quantity

        if isinstance(__value, (float, int)):
            return Quantity(value=self.si_value / __value, units=self._unit)

    def __rtruediv__(self, __value):
        return Quantity(__value, "") / self

    def __add__(self, __value):
        self._arithmetic_precheck(__value)
        new_units = self.si_units
        new_value = float(self) + float(__value)
        new_quantity = Quantity(value=new_value, units=new_units)
        preferred_units = self._temp_precheck(__value.units)
        if preferred_units and preferred_units != new_units:
            return new_quantity.to(preferred_units)
        return new_quantity.to(self.units)

    def __radd__(self, __value):
        return self.__add__(__value)

    def __sub__(self, __value):
        self._arithmetic_precheck(__value)
        new_units = self.si_units
        new_value = float(self) - float(__value)
        new_quantity = Quantity(value=new_value, units=new_units)
        preferred_units = self._temp_precheck(__value.units, op="-")
        if preferred_units and preferred_units != new_units:
            return new_quantity.to(preferred_units)
        return new_quantity.to(self.units)

    def __rsub__(self, __value):
        return self.__sub__(__value)

    def __neg__(self):
        return Quantity(-self.value, self._unit)

    def __gt__(self, __value):
        self._arithmetic_precheck(__value)
        return float(self) > float(__value)

    def __ge__(self, __value):
        self._arithmetic_precheck(__value)
        return float(self) >= float(__value)

    def __lt__(self, __value):
        self._arithmetic_precheck(__value)
        return float(self) < float(__value)

    def __le__(self, __value):
        self._arithmetic_precheck(__value)
        return float(self) <= float(__value)

    def __eq__(self, __value):
        self._arithmetic_precheck(__value)
        return float(self) == float(__value)

    def __neq__(self, __value):
        self._arithmetic_precheck(__value)
        return float(self) != float(__value)


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
    def INCOMPATIBLE_DIMENSIONS(cls, from_unit, to_unit):
        return cls(f"`{from_unit}` and `{to_unit}` have incompatible dimensions.")

    @classmethod
    def INCOMPATIBLE_VALUE(cls, value):
        return cls(f"`{value}` is incompatible with the current quantity object.")

    @classmethod
    def UNKNOWN_UNITS(cls, unit: str):
        return cls(f"`{unit}` is an unknown or unconfigured unit.")
