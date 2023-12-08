"""Provides the ``UnitSystem`` class."""
from __future__ import annotations

from typing import Union

import ansys.units as ansunits


class NotBaseUnit(ValueError):
    """Provides the error when the provided unit is unavailable in base units."""

    def __init__(self, unit):
        super().__init__(
            f"`{unit.name}` is not a base unit. To use `{unit.name}`, add it to the "
            "`base_units` table within the cfg.yaml file."
        )


class InvalidUnitSystem(ValueError):
    """Provides the error when the provided unit system is unsupported."""

    def __init__(self, sys):
        super().__init__(f"`{sys}` is not a supported unit system.")


class IncorrectUnitType(ValueError):
    """Provides the error when the type of provided unit is incorrect."""

    def __init__(self, unit, unit_type):
        super().__init__(
            f"The unit `{unit.name}` is incompatible with unit system type: `{unit_type.name}`"
        )


class UnitSystem:
    """
    A class containing base units for a unit system.

    Predefined unit systems work automatically and are configured when the
    package is initialized, whereas you can add user-defined systems at any time.

    Parameters
    ----------
    base_units: dict, optional
        Units mapped to base dimensions types.
    unit_sys: str, optional
        Predefined unit system.
    copy_from: UnitSystem
        Make a copy of a unit system.

    Attributes
    ----------
    base_units
    MASS
    LENGTH
    TIME
    TEMPERATURE
    TEMPERATURE_DIFFERENCE
    ANGLE
    CHEMICAL_AMOUNT
    LIGHT
    CURRENT
    SOLID_ANGLE
    """

    def __init__(
        self,
        base_units: dict[ansunits.BaseDimensions, Union[ansunits.Unit, str]] = None,
        system: str = None,
        copy_from: ansunits.UnitSystem = None,
    ):
        if copy_from:
            self._units = copy_from._units
        else:
            if not system:
                system = "SI"
            if system not in ansunits._unit_systems:
                raise InvalidUnitSystem(system)
            else:
                self._units = ansunits._unit_systems[system].copy()

        if base_units:
            for unit_type, unit in base_units.items():
                self._units[unit_type.name] = unit

        for unit_type in ansunits.BaseDimensions:
            unit = self._units[unit_type.name]
            self._set_type(unit_type=unit_type, unit=unit)

    def convert(self, quantity: ansunits.Quantity) -> ansunits.Quantity:
        """
        Convert a quantity into the unit system.

        Parameters
        ----------
        quantity : Quantity
            Quantity to convert.

        Returns
        -------
        Quantity
            Quantity object converted into the unit system.

        Examples
        --------
        >>> ur = UnitRegistry()
        >>> speed_si = Quantity(value=5, units= ur.m / ur.s)
        >>> bt = UnitSystem(system="BT")
        >>> speed_bt = bt.convert(speed_si)
        """
        new_unit = ansunits.Unit(dimensions=quantity.dimensions, system=self)

        return quantity.to(to_units=new_unit)

    def update(
        self, base_units: dict[ansunits.BaseDimensions : Union[ansunits.Unit, str]]
    ):
        """
        Change the units of the unit system.

        Parameters
        ----------
        base_units: dict, obj
            Units mapped to base dimensions types.
        """
        for unit_type, unit in base_units.items():
            self._set_type(unit_type=unit_type, unit=unit)

    def _set_type(
        self, unit_type: ansunits.BaseDimensions, unit: Union[ansunits.Unit, str]
    ):
        """
        Checks that the unit is compatible with the unit type before being set.

        Parameters
        ----------
        unit_type: obj
            Unit system type slot for the new unit.
        unit: obj
            The unit to be assigned.
        """
        if not isinstance(unit, ansunits.Unit):
            unit = ansunits.Unit(unit)

        if unit.name not in ansunits._base_units:
            raise NotBaseUnit(unit)

        if unit._type != unit_type.name:
            raise IncorrectUnitType(unit, unit_type)

        setattr(self, f"_{unit_type.name}", unit)

    @property
    def base_units(self) -> list[str]:
        """Base units of the unit system."""
        _base_units = []
        for unit_type in ansunits.BaseDimensions:
            unit = getattr(self, f"_{unit_type.name}")
            _base_units.append(unit.name)
        return _base_units

    @property
    def MASS(self):
        """Mass unit of the unit system."""
        return self._MASS

    @MASS.setter
    def MASS(self, new_unit):
        self._set_type(unit_type=ansunits.BaseDimensions.MASS, unit=new_unit)

    @property
    def LENGTH(self):
        """Length unit of the unit system."""
        return self._LENGTH

    @LENGTH.setter
    def LENGTH(self, new_unit):
        self._set_type(unit_type=ansunits.BaseDimensions.LENGTH, unit=new_unit)

    @property
    def TIME(self):
        """Time unit of the unit system."""
        return self._TIME

    @TIME.setter
    def TIME(self, new_unit):
        self._set_type(unit_type=ansunits.BaseDimensions.TIME, unit=new_unit)

    @property
    def TEMPERATURE(self):
        """Temperature unit of the unit system."""
        return self._TEMPERATURE

    @TEMPERATURE.setter
    def TEMPERATURE(self, new_unit):
        self._set_type(unit_type=ansunits.BaseDimensions.TEMPERATURE, unit=new_unit)

    @property
    def TEMPERATURE_DIFFERENCE(self):
        """Temperature unit of the unit system."""
        return self._TEMPERATURE_DIFFERENCE

    @TEMPERATURE_DIFFERENCE.setter
    def TEMPERATURE_DIFFERENCE(self, new_mass):
        self._set_type(
            unit_type=ansunits.BaseDimensions.TEMPERATURE_DIFFERENCE, unit=new_mass
        )

    @property
    def ANGLE(self):
        """Angle unit of the unit system."""
        return self._ANGLE

    @ANGLE.setter
    def ANGLE(self, new_mass):
        self._set_type(unit_type=ansunits.BaseDimensions.ANGLE, unit=new_mass)

    @property
    def CHEMICAL_AMOUNT(self):
        """Chemical Amount unit of the unit system."""
        return self._CHEMICAL_AMOUNT

    @CHEMICAL_AMOUNT.setter
    def CHEMICAL_AMOUNT(self, new_mass):
        self._set_type(unit_type=ansunits.BaseDimensions.CHEMICAL_AMOUNT, unit=new_mass)

    @property
    def LIGHT(self):
        """Light unit of the unit system."""
        return self._LIGHT

    @LIGHT.setter
    def LIGHT(self, new_mass):
        self._set_type(unit_type=ansunits.BaseDimensions.LIGHT, unit=new_mass)

    @property
    def CURRENT(self):
        """Current unit of the unit system."""
        return self._CURRENT

    @CURRENT.setter
    def CURRENT(self, new_mass):
        self._set_type(unit_type=ansunits.BaseDimensions.CURRENT, unit=new_mass)

    @property
    def SOLID_ANGLE(self):
        """Solid Angle unit of the unit system."""
        return self._SOLID_ANGLE

    @SOLID_ANGLE.setter
    def SOLID_ANGLE(self, new_mass):
        self._set_type(unit_type=ansunits.BaseDimensions.SOLID_ANGLE, unit=new_mass)

    def __repr__(self):
        units = {}
        for unit_type in ansunits.BaseDimensions:
            unit = getattr(self, f"_{unit_type.name}")
            units.update({unit_type.name: unit.name})
        return str(units)

    def __eq__(self, other_sys):
        for attr, value in self.__dict__.items():
            if getattr(other_sys, attr) != value:
                return False
        return True
