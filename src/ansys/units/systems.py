"""Provides the ``UnitSystem`` class."""
import ansys.units as ansunits
from ansys.units.utils import si_data


class UnitSystem:
    """
    Initializes a unit system based on user-defined units or a predefined unit system.

    Parameters
    ----------
    name: str, None
        Custom name associated with a user-defined unit system.
    base_units: list, None
        Custom units associated with a user-defined unit system.
    unit_sys: str, None
        Predefined unit system.

    Methods
    -------
    convert()
        Convert from one unit system to a given unit system.

    Returns
    -------
    Quantity
        Quantity instance.
    """

    def __init__(self, name: str = None, base_units: list = None, unit_sys: str = None):
        if name and unit_sys or base_units and unit_sys:
            raise UnitSystemError.EXCESSIVE_PARAMETERS()

        if base_units:
            if len(base_units) != ansunits.Dimensions.max_dim_len():
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

            if unit.name not in ansunits._fundamental_units:
                raise UnitSystemError.NOT_FUNDAMENTAL(unit)

            if hasattr(self, f"_{unit.type.lower()}"):
                raise UnitSystemError.UNIT_TYPE(unit)

            setattr(self, f"_{unit.type.lower()}", unit)

            if unit.type == "Temperature":
                delta_unit = ansunits.Unit(f"delta_{unit.name}")
                setattr(self, "_temperature difference", delta_unit)

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
            Quantity object containing the desired unit system conversion.
        """
        new_dim = ansunits.Dimensions(
            dimensions=quantity.dimensions, unit_sys=self.base_units
        )

        _, si_multiplier, si_offset = si_data(new_dim.units)
        new_value = (quantity.si_value / si_multiplier) - si_offset

        return ansunits.Quantity(value=new_value, units=new_dim.units)

    @property
    def name(self):
        """Name associated with the unit system."""
        return self._name

    @property
    def base_units(self):
        """Units associated with the unit system."""
        _base_units = []
        dim_order = ansunits._dimension_order
        for order in dim_order:
            unit = getattr(self, f"_{order.lower()}")
            _base_units.append(unit.name)
        return _base_units

    @property
    def mass(self):
        """Mass unit of the unit system."""
        return self._mass

    @property
    def length(self):
        """Length unit of the unit system."""
        return self._length

    @property
    def time(self):
        """Time unit of the unit system."""
        return self._time

    @property
    def temperature(self):
        """Temperature unit of the unit system."""
        return self._temperature

    @property
    def temperature_difference(self):
        """Temperature unit of the unit system."""
        return getattr(self, "_temperature difference")

    @property
    def angle(self):
        """Angle unit of the unit system."""
        return self._angle

    @property
    def chemical_amount(self):
        """Chemical Amount unit of the unit system."""
        return getattr(self, "_chemical amount")

    @property
    def light(self):
        """Light unit of the unit system."""
        return self._light

    @property
    def current(self):
        """Current unit of the unit system."""
        return self._current

    @property
    def solid_angle(self):
        """Solid Angle unit of the unit system."""
        return getattr(self, "_solid angle")


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
            f"The `base_units` argument must contain 9 units, currently there are {len}."
        )

    @classmethod
    def NOT_FUNDAMENTAL(cls, unit):
        return cls(
            f"`{unit.name}` is not a fundimental unit. To use `{unit.name}`, add it to the "
            "`fundamental_units` table within the cfg.yaml file."
        )

    @classmethod
    def UNIT_TYPE(cls, unit):
        return cls(
            f"Unit of type: `{unit.type}` already exits in this unit system"
            f"replace '{unit.name}' with unit of another type"
        )

    @classmethod
    def INVALID_UNIT_SYS(cls, sys):
        return cls(f"`{sys}` is not a supported unit system.")
