"""Provides the ``UnitSystem`` class."""
from __future__ import annotations

import ansys.units as ansunits


class UnitSystem:
    """
    A class containing base units for a user-defined or predefined unit system.

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
        base_units: dict[ansunits.BaseDimensions : ansunits.Unit | str] = None,
        unit_sys: str = None,
        copy_from: ansunits.UnitSystem = None,
    ):
        if copy_from:
            self._units = copy_from._units
        else:
            if not unit_sys:
                unit_sys = "SI"
            if unit_sys not in ansunits._unit_systems:
                raise UnitSystemError.INVALID_UNIT_SYS(unit_sys)
            else:
                self._units = ansunits._unit_systems[unit_sys].copy()

        if base_units:
            for unit_type, unit in base_units.items():
                self._units[unit_type.name] = unit

        for unit_type in ansunits.BaseDimensions:
            unit = self._units[unit_type.name]
            self._set_type(unit_type=unit_type, unit=unit)

    def convert(self, quantity: ansunits.Quantity) -> ansunits.Quantity:
        """
        Perform unit system conversions.

        Parameters
        ----------
        quantity : Quantity
            Desired quantity object to convert.

        Returns
        -------
        Quantity
            Quantity object converted to the desired unit system.
        """
        new_unit = ansunits.Unit(dimensions=quantity.dimensions, unit_sys=self)

        return quantity.to(to_units=new_unit)

    def update(self, base_units: dict[ansunits.BaseDimensions : ansunits.Unit | str]):
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
        self, unit_type: ansunits.BaseDimensions, unit: [ansunits.Unit | str]
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
            raise UnitSystemError.NOT_BASE_UNIT(unit)

        if unit._type != unit_type.name:
            raise UnitSystemError.WRONG_UNIT_TYPE(unit, unit_type)

        setattr(self, f"_{unit_type.name}", unit)

    @property
    def base_units(self):
        """Units associated with the unit system."""
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

    def __eq__(self, other_sys):
        for attr, value in self.__dict__.items():
            if getattr(other_sys, attr) != value:
                return False
        return True


class UnitSystemError(ValueError):
    """Provides custom unit system errors."""

    def __init__(self, err):
        super().__init__(err)

    @classmethod
    def BASE_UNITS_LENGTH(cls, len):
        return cls(
            f"The `base_units` argument must contain 10 unique units, currently there are {len}."
        )

    @classmethod
    def NOT_BASE_UNIT(cls, unit):
        return cls(
            f"`{unit.name}` is not a base unit. To use `{unit.name}`, add it to the "
            "`base_units` table within the cfg.yaml file."
        )

    @classmethod
    def INVALID_UNIT_SYS(cls, sys):
        return cls(f"`{sys}` is not a supported unit system.")

    @classmethod
    def WRONG_UNIT_TYPE(cls, unit, unit_type):
        return cls(
            f"The unit `{unit.name}` is incompatible with unit system type: `{unit_type.name}`"
        )
