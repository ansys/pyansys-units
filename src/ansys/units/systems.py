"""Provides the ``UnitSystem`` class."""
from __future__ import annotations

from ansys.units import BaseDimensions, _base_units, _unit_systems


class UnitSystem:
    """
    A class representing base units for a unit system.

    Predefined unit systems work automatically and are configured when the
    package is initialized, whereas you can add user-defined systems at any time.

    Parameters
    ----------
    base_units: dict, optional
        Units mapped to base dimensions types.
    unit_sys: str, Unit, optional
        Predefined unit system.
    copy_from: UnitSystem, optional
        Make a copy of a unit system.

    Attributes
    ----------
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
        base_units: dict[BaseDimensions, any] = None,
        system: str = None,
        copy_from: UnitSystem = None,
    ):
        if copy_from:
            self._units = copy_from._units
        else:
            if not system:
                system = "SI"
            if system not in _unit_systems:
                raise InvalidUnitSystem(system)
            else:
                self._units = _unit_systems[system].copy()

        if base_units:
            for unit_type, unit in base_units.items():
                self._units[unit_type.name] = unit

        for unit_type in BaseDimensions:
            unit = self._units[unit_type.name]
            self._set_type(unit_type=unit_type, unit=unit)

    def update(self, base_units: dict[BaseDimensions:any]):
        """
        Change the units of the unit system.

        Parameters
        ----------
        base_units: dict
            Units mapped to base dimensions types.
        """
        for unit_type, unit in base_units.items():
            self._set_type(unit_type=unit_type, unit=unit)

    def _set_type(self, unit_type: BaseDimensions, unit: any):
        """
        Checks that the unit is compatible with the unit type before being set.

        Parameters
        ----------
        unit_type: obj
            Unit system type slot for the new unit.
        unit: str, obj
            The unit to be assigned.
        """
        name = getattr(unit, "name", None) or unit

        if name not in _base_units:
            raise NotBaseUnit(name)
        if _base_units[name]["type"] != unit_type.name:
            raise IncorrectUnitType(name, unit_type)

        setattr(self, f"_{unit_type.name}", unit)

    @property
    def MASS(self):
        """Mass unit of the unit system."""
        return self._MASS

    @MASS.setter
    def MASS(self, new_unit):
        self._set_type(unit_type=BaseDimensions.MASS, unit=new_unit)

    @property
    def LENGTH(self):
        """Length unit of the unit system."""
        return self._LENGTH

    @LENGTH.setter
    def LENGTH(self, new_unit):
        self._set_type(unit_type=BaseDimensions.LENGTH, unit=new_unit)

    @property
    def TIME(self):
        """Time unit of the unit system."""
        return self._TIME

    @TIME.setter
    def TIME(self, new_unit):
        self._set_type(unit_type=BaseDimensions.TIME, unit=new_unit)

    @property
    def TEMPERATURE(self):
        """Temperature unit of the unit system."""
        return self._TEMPERATURE

    @TEMPERATURE.setter
    def TEMPERATURE(self, new_unit):
        self._set_type(unit_type=BaseDimensions.TEMPERATURE, unit=new_unit)

    @property
    def TEMPERATURE_DIFFERENCE(self):
        """Temperature unit of the unit system."""
        return self._TEMPERATURE_DIFFERENCE

    @TEMPERATURE_DIFFERENCE.setter
    def TEMPERATURE_DIFFERENCE(self, new_mass):
        self._set_type(unit_type=BaseDimensions.TEMPERATURE_DIFFERENCE, unit=new_mass)

    @property
    def ANGLE(self):
        """Angle unit of the unit system."""
        return self._ANGLE

    @ANGLE.setter
    def ANGLE(self, new_mass):
        self._set_type(unit_type=BaseDimensions.ANGLE, unit=new_mass)

    @property
    def CHEMICAL_AMOUNT(self):
        """Chemical Amount unit of the unit system."""
        return self._CHEMICAL_AMOUNT

    @CHEMICAL_AMOUNT.setter
    def CHEMICAL_AMOUNT(self, new_mass):
        self._set_type(unit_type=BaseDimensions.CHEMICAL_AMOUNT, unit=new_mass)

    @property
    def LIGHT(self):
        """Light unit of the unit system."""
        return self._LIGHT

    @LIGHT.setter
    def LIGHT(self, new_mass):
        self._set_type(unit_type=BaseDimensions.LIGHT, unit=new_mass)

    @property
    def CURRENT(self):
        """Current unit of the unit system."""
        return self._CURRENT

    @CURRENT.setter
    def CURRENT(self, new_mass):
        self._set_type(unit_type=BaseDimensions.CURRENT, unit=new_mass)

    @property
    def SOLID_ANGLE(self):
        """Solid Angle unit of the unit system."""
        return self._SOLID_ANGLE

    @SOLID_ANGLE.setter
    def SOLID_ANGLE(self, new_mass):
        self._set_type(unit_type=BaseDimensions.SOLID_ANGLE, unit=new_mass)

    def __repr__(self):
        units = ""
        for unit_type in BaseDimensions:
            unit = getattr(self, f"_{unit_type.name}")
            units += f"{unit_type.name}: {unit}\n"
        return units

    def __eq__(self, other_sys):
        for attr, value in self.__dict__.items():
            if getattr(other_sys, attr) != value:
                return False
        return True


class NotBaseUnit(ValueError):
    """Raised when a unit system unit is not a configured base unit."""

    def __init__(self, unit):
        super().__init__(
            f"`{unit}` is not a base unit. To use `{unit}`, add it to the "
            "`base_units` table within the cfg.yaml file."
        )


class InvalidUnitSystem(ValueError):
    """Raised when a unit system is initialized with an unsupported unit system."""

    def __init__(self, sys):
        super().__init__(f"`{sys}` is not a supported unit system.")


class IncorrectUnitType(ValueError):
    """Raised when a unit is provided that does not have a valid type of base unit."""

    def __init__(self, unit, unit_type):
        super().__init__(
            f"The unit `{unit}` is incompatible with unit system type: `{unit_type.name}`"
        )
