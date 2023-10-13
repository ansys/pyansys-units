"""Provides the ``UnitSystem`` class."""
import ansys.units as ansunits


class UnitSystem:
    """
    A class containing base units for a user-defined or predefined unit system.

    Parameters
    ----------
    name: str, optional
        Custom name associated with a user-defined unit system.
    base_units: list, optional
        Custom units associated with a user-defined unit system.
    unit_sys: str, optional
        Predefined unit system.

    Attributes
    ----------
    name
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

    def __init__(self, name: str = None, base_units: list = None, unit_sys: str = None):
        if name and unit_sys or base_units and unit_sys:
            raise UnitSystemError.EXCESSIVE_PARAMETERS()

        if base_units:
            if len(set(base_units)) != len(ansunits.BaseDimensions):
                raise UnitSystemError.BASE_UNITS_LENGTH(len(base_units))

            self._name = name
            self._base_units = base_units

        else:
            if not unit_sys:
                unit_sys = "SI"
            if unit_sys not in ansunits._unit_systems:
                raise UnitSystemError.INVALID_UNIT_SYS(unit_sys)

            self._name = unit_sys
            self._base_units = ansunits._unit_systems[unit_sys]

        for unit in self._base_units:
            if not isinstance(unit, ansunits.Unit):
                unit = ansunits.Unit(unit)

            if unit.name not in ansunits._base_units:
                raise UnitSystemError.NOT_BASE_UNIT(unit)

            unit_type = self._get_type(dimensions=unit.dimensions)

            setattr(self, f"_{unit_type}", unit)

    def _get_type(self, dimensions: ansunits.Dimensions):
        return [x.name for x in dimensions.dimensions.keys()][0]

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

    @property
    def name(self):
        """Name associated with the unit system."""
        return self._name

    @property
    def base_units(self):
        """Units associated with the unit system."""
        _base_units = []
        for type in ansunits.BaseDimensions:
            unit = getattr(self, f"_{type.name}")
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
