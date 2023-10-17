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

            if not isinstance(unit, ansunits.Unit):
                unit = ansunits.Unit(unit)

            if unit.name not in ansunits._base_units:
                raise UnitSystemError.NOT_BASE_UNIT(unit)

            setattr(self, f"_{unit_type.name}", unit)

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
        base_units: dict, Unit
            Units mapped to base dimensions types.
        """
        for unit_type, unit in base_units.items():
            if not isinstance(unit, ansunits.Unit):
                unit = ansunits.Unit(unit)

            if unit.name not in ansunits._base_units:
                raise UnitSystemError.NOT_BASE_UNIT(unit)

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

    @property
    def LENGTH(self):
        """Length unit of the unit system."""
        return self._LENGTH

    @property
    def TIME(self):
        """Time unit of the unit system."""
        return self._TIME

    @property
    def TEMPERATURE(self):
        """Temperature unit of the unit system."""
        return self._TEMPERATURE

    @property
    def TEMPERATURE_DIFFERENCE(self):
        """Temperature unit of the unit system."""
        return self._TEMPERATURE_DIFFERENCE

    @property
    def ANGLE(self):
        """Angle unit of the unit system."""
        return self._ANGLE

    @property
    def CHEMICAL_AMOUNT(self):
        """Chemical Amount unit of the unit system."""
        return self._CHEMICAL_AMOUNT

    @property
    def LIGHT(self):
        """Light unit of the unit system."""
        return self._LIGHT

    @property
    def CURRENT(self):
        """Current unit of the unit system."""
        return self._CURRENT

    @property
    def SOLID_ANGLE(self):
        """Solid Angle unit of the unit system."""
        return self._SOLID_ANGLE


class UnitSystemError(ValueError):
    """Provides custom unit system errors."""

    def __init__(self, err):
        super().__init__(err)

    @classmethod
    def EXCESSIVE_PARAMETERS(cls):
        return cls(
            "UnitSystem only accepts one of the following parameters: "
            "(name, base_units) or (unit_sys)."
        )

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
