# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
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
"""Provides the ``UnitSystem`` class."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from typing_extensions import Protocol, override

from ansys.units._constants import _base_units, _unit_systems
from ansys.units._unit_parsing import _units_to_dim
from ansys.units.base_dimensions import BaseDimensions
from ansys.units.dimensions import Dimensions
from ansys.units.quantity_tables.keys import *  # noqa: F403

_unit_system_preferred_units: dict[str, list[str]] = {}


class UnitLike(Protocol):
    """Protocol for unit-like objects accepted by unit system helpers."""

    @property
    def name(self) -> str: ...

    @property
    def dimensions(self) -> Dimensions: ...


def _validate_base_unit(unit_type: BaseDimensions, unit: UnitKey | str) -> str:
    """
    Validate that ``unit`` is dimensionally atomic and matches ``unit_type``.

    A unit is dimensionally atomic when it corresponds to exactly one base
    dimension raised to the power of 1. This covers configured base units
    (for example ``"kg"``), SI-prefixed base units (for example ``"mm"``,
    which is the ``"m"`` multiplier ``"m"`` applied to the base unit ``"m"``),
    single-composition derived units (for example ``"tonne"``, which is
    defined as ``1000 kg``), and instance-scoped custom units registered via
    :meth:`~ansys.units.unit_registry.UnitRegistry.register_unit` (validated
    using their own precomputed dimensions, since such units are not known
    globally by name). Compound units, such as ``"N"`` or ``"Pa"``, which
    span more than one base dimension, are rejected.

    Parameters
    ----------
    unit_type: BaseDimensions
        Unit system type slot the unit is intended for.
    unit: str, obj
        The unit to validate.

    Returns
    -------
    str
        The resolved name of ``unit``.

    Raises
    ------
    NotBaseUnit
        If the unit cannot be resolved or is not dimensionally atomic.
    IncorrectUnitType
        If the unit is atomic but corresponds to a different base dimension.
    """
    name = getattr(unit, "name", None) or unit

    # Fast path: unit is a literal, configured base unit (e.g. "kg", "K").
    if name in _base_units:
        if _base_units[name]["type"] != unit_type.name:
            raise IncorrectUnitType(name, unit_type)
        return name

    # If a concrete ``Unit`` instance was supplied (for example a custom,
    # instance-scoped unit registered on a ``UnitRegistry``), trust its own
    # precomputed dimensions instead of re-deriving them from its name
    # against the global unit tables, since instance-registered units are
    # not resolvable by name outside of their owning registry.
    unit_dimensions = getattr(unit, "dimensions", None)
    if unit_dimensions is not None:
        dims_dict = dict(unit_dimensions)
        if len(dims_dict) == 1:
            dim, exponent = next(iter(dims_dict.items()))
            if exponent == 1:
                if dim != unit_type:
                    raise IncorrectUnitType(name, unit_type)
                return name
        raise NotBaseUnit(name)

    # Fallback: resolve prefixed (e.g. "mm") or single-composition derived
    # (e.g. "tonne") units by their underlying dimensions.
    try:
        resolved_dims = _units_to_dim(units=str(name))
    except Exception:
        raise NotBaseUnit(name) from None

    if len(resolved_dims) == 1:
        dim, exponent = next(iter(resolved_dims.items()))
        if exponent == 1:
            if dim != unit_type:
                raise IncorrectUnitType(name, unit_type)
            return name

    raise NotBaseUnit(name)


def _validate_preferred_unit(
    unit: UnitKey | str | UnitLike,
) -> tuple[str, dict[BaseDimensions, float]]:
    """
    Validate a preferred unit and return its name and dimensions.

    Preferred units are display/conversion targets for derived quantities. They do not
    need to be dimensionally atomic, but they do need to resolve to a valid unit with
    dimensions.
    """
    name = str(getattr(unit, "name", None) or unit)
    try:
        dims_dict = _units_to_dim(units=str(name))
    except Exception:
        raise UnconfiguredPreferredUnit(name) from None

    if not dims_dict:
        raise UnconfiguredPreferredUnit(name)

    return name, dims_dict


def _iter_preferred_units(
    units: Sequence[UnitKey | str | UnitLike] | UnitKey | str | UnitLike,
) -> Sequence[UnitKey | str | UnitLike]:
    """Return preferred units as a sequence while treating strings as one unit."""
    if isinstance(units, str) or not isinstance(units, Sequence):
        return [units]
    return units


class UnitSystem:
    """
    A class representing base units for a unit system.

    Predefined unit systems work automatically and are configured when the
    package is initialized, whereas you can add user-defined systems at any time.

    Parameters
    ----------
    base_units: dict, optional
        Units mapped to base dimensions types.
    preferred_units: str, list, optional
        Preferred units used when converted dimensions match. These units are
        display/conversion targets for derived quantities, not base-unit slots.
    system: str, Unit, optional
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
        base_units: Mapping[BaseDimensions, UnitKey | str] | None = None,
        preferred_units: (
            Sequence[UnitKey | str | UnitLike] | UnitKey | str | UnitLike | None
        ) = None,
        system: Systems | str = "SI",
        copy_from: UnitSystem | None = None,
    ):
        if copy_from:
            self._units = copy_from._units.copy()
            self._preferred_units = copy_from._preferred_units.copy()
        else:
            if system not in _unit_systems:
                raise InvalidUnitSystem(system)
            else:
                self._units = _unit_systems[system].copy()
            self._preferred_units: dict[DimensionsKey, str] = {}
            if system in _unit_system_preferred_units:
                self.add_preferred_units(_unit_system_preferred_units[system])

        if base_units:
            for unit_type, unit in base_units.items():
                self._units[unit_type.name] = unit

        for unit_type in BaseDimensions:
            unit = self._units[unit_type.name]
            self._set_type(unit_type=unit_type, unit=unit)

        if preferred_units:
            self.add_preferred_units(preferred_units)

    def update(self, base_units: Mapping[BaseDimensions, UnitKey | str]):
        """
        Change the units of the unit system.

        Parameters
        ----------
        base_units: dict
            Units mapped to base dimensions types.
        """
        for unit_type, unit in base_units.items():
            self._set_type(unit_type=unit_type, unit=unit)

    def add_preferred_units(
        self,
        units: Sequence[UnitKey | str | UnitLike] | UnitKey | str | UnitLike,
    ) -> None:
        """
        Add preferred display units for derived dimensions.

        When a unit is converted using this unit system, a matching preferred
        unit is returned instead of the expanded base-unit expression. For
        example, a millimeter-tonne-second system can prefer ``"MPa"`` for
        pressure/stress dimensions instead of ``"tonne mm^-1 s^-2"``.

        Parameters
        ----------
        units: list
            Preferred units to use for matching dimensions.
        """
        for unit in _iter_preferred_units(units):
            name, dims_dict = _validate_preferred_unit(unit)
            dimensions_key = DimensionsKey(dims_dict)
            if dimensions_key in self._preferred_units:
                existing_unit = self._preferred_units[dimensions_key]
                if existing_unit != name:
                    raise PreferredUnitAlreadyRegistered(existing_unit, name)
            self._preferred_units[dimensions_key] = name

    def preferred_unit_for(self, dimensions: Dimensions) -> str | None:
        """Return the preferred unit name for dimensions, if one is configured."""
        return self._preferred_units.get(DimensionsKey(dict(dimensions)))

    @classmethod
    def register_system(
        cls,
        name: str,
        base_units: Mapping[BaseDimensions, UnitKey | str],
        preferred_units: (
            Sequence[UnitKey | str | UnitLike] | UnitKey | str | UnitLike | None
        ) = None,
    ) -> None:
        """
        Register a new named unit system for later reuse.

        Once registered, the system can be created anywhere via
        ``UnitSystem(system=name)``, the same way built-in systems such as
        ``"SI"``, ``"CGS"``, and ``"BT"`` are used. Registration is global for
        the running process (module-scoped), matching the behavior of the
        predefined unit systems loaded from ``cfg.yaml``.

        .. note::
            Only the resolved unit *name* is persisted, not the ``Unit``
            object itself. Instance-scoped custom units created with
            :meth:`~ansys.units.unit_registry.UnitRegistry.register_unit`
            are not known globally by name, so while passing one here
            succeeds (it is valid at registration time), reconstructing the
            system later with ``UnitSystem(system=name)`` fails unless the
            unit is also resolvable without that specific registry (for
            example a built-in unit, or a prefixed/derived atomic unit).

        Parameters
        ----------
        name: str
            Name of the new unit system, for example ``"MMGS"``.
        base_units: dict
            Units mapped to base dimensions types. Every member of
            :class:`~ansys.units.base_dimensions.BaseDimensions` must be
            provided so the resulting system is fully defined.
        preferred_units: str, list, optional
            Preferred units used when converted dimensions match. These units
            are display/conversion targets for derived quantities, not
            base-unit slots.

        Raises
        ------
        UnitSystemAlreadyRegistered
            If ``name`` is already used by a built-in or previously
            registered unit system.
        IncompleteUnitSystem
            If ``base_units`` is missing one or more base dimensions.
        NotBaseUnit
            If a unit is not dimensionally atomic (for example a derived
            unit that spans more than one base dimension, such as ``"Pa"``).
        IncorrectUnitType
            If a unit does not match its intended base dimension.
        UnconfiguredPreferredUnit
            If a preferred unit cannot be resolved globally by name.
        PreferredUnitAlreadyRegistered
            If two preferred units have the same dimensions.

        Examples
        --------
        Register a custom "mm, g, s" (MMGS) unit system:

        >>> from ansys.units import BaseDimensions, UnitSystem
        >>> dims = BaseDimensions
        >>> UnitSystem.register_system(
        ...     name="MMGS",
        ...     base_units={
        ...         dims.MASS: "g",
        ...         dims.LENGTH: "mm",
        ...         dims.TIME: "s",
        ...         dims.TEMPERATURE: "K",
        ...         dims.TEMPERATURE_DIFFERENCE: "delta_K",
        ...         dims.ANGLE: "radian",
        ...         dims.CHEMICAL_AMOUNT: "mol",
        ...         dims.LIGHT: "cd",
        ...         dims.CURRENT: "A",
        ...         dims.SOLID_ANGLE: "sr",
        ...     },
        ... )
        >>> mmgs = UnitSystem(system="MMGS")
        >>> mmgs.LENGTH
        'mm'
        """
        name = name.strip()
        if not name:
            raise ValueError("`name` must be a non-empty string.")
        if name in _unit_systems:
            raise UnitSystemAlreadyRegistered(name)

        missing = [dim for dim in BaseDimensions if dim not in base_units]
        if missing:
            raise IncompleteUnitSystem(missing)

        resolved: dict[str, str] = {}
        for unit_type, unit in base_units.items():
            resolved[unit_type.name] = _validate_base_unit(
                unit_type=unit_type, unit=unit
            )

        resolved_preferred_units: list[str] = []
        if preferred_units:
            preferred_unit_system = UnitSystem(system="SI")
            preferred_unit_system.add_preferred_units(preferred_units)
            for unit in _iter_preferred_units(preferred_units):
                resolved_preferred_units.append(_validate_preferred_unit(unit)[0])

        _unit_systems[name] = resolved
        if resolved_preferred_units:
            _unit_system_preferred_units[name] = resolved_preferred_units

    def _set_type(self, unit_type: BaseDimensions, unit: UnitKey | str):
        """
        Checks that the unit is compatible with the unit type before being set.

        Parameters
        ----------
        unit_type: obj
            Unit system type slot for the new unit.
        unit: str, obj
            The unit to be assigned.
        """
        _validate_base_unit(unit_type=unit_type, unit=unit)
        setattr(self, f"_{unit_type.name}", unit)

    @property
    def MASS(self) -> MassKey | str:
        """Mass unit of the unit system."""
        return self._MASS

    @MASS.setter
    def MASS(self, new_unit: MassKey | str) -> None:
        self._set_type(unit_type=BaseDimensions.MASS, unit=new_unit)

    @property
    def LENGTH(self) -> LengthKey | str:
        """Length unit of the unit system."""
        return self._LENGTH

    @LENGTH.setter
    def LENGTH(self, new_unit: LengthKey | str) -> None:
        self._set_type(unit_type=BaseDimensions.LENGTH, unit=new_unit)

    @property
    def TIME(self) -> TimeKey | str:
        """Time unit of the unit system."""
        return self._TIME

    @TIME.setter
    def TIME(self, new_unit: TimeKey | str) -> None:
        self._set_type(unit_type=BaseDimensions.TIME, unit=new_unit)

    @property
    def TEMPERATURE(self) -> TemperatureKey | str:
        """Temperature unit of the unit system."""
        return self._TEMPERATURE

    @TEMPERATURE.setter
    def TEMPERATURE(self, new_unit: TemperatureKey | str) -> None:
        self._set_type(unit_type=BaseDimensions.TEMPERATURE, unit=new_unit)

    @property
    def TEMPERATURE_DIFFERENCE(self) -> TemperatureDifferenceKey | str:
        """Temperature unit of the unit system."""
        return self._TEMPERATURE_DIFFERENCE

    @TEMPERATURE_DIFFERENCE.setter
    def TEMPERATURE_DIFFERENCE(self, new_mass: TemperatureDifferenceKey | str) -> None:
        self._set_type(unit_type=BaseDimensions.TEMPERATURE_DIFFERENCE, unit=new_mass)

    @property
    def ANGLE(self) -> AngleKey | str:
        """Angle unit of the unit system."""
        return self._ANGLE

    @ANGLE.setter
    def ANGLE(self, new_mass: AngleKey | str) -> None:
        self._set_type(unit_type=BaseDimensions.ANGLE, unit=new_mass)

    @property
    def CHEMICAL_AMOUNT(self) -> ChemicalAmountKey | str:
        """Chemical Amount unit of the unit system."""
        return self._CHEMICAL_AMOUNT

    @CHEMICAL_AMOUNT.setter
    def CHEMICAL_AMOUNT(self, new_mass: ChemicalAmountKey | str) -> None:
        self._set_type(unit_type=BaseDimensions.CHEMICAL_AMOUNT, unit=new_mass)

    @property
    def LIGHT(self) -> LightKey | str:
        """Light unit of the unit system."""
        return self._LIGHT

    @LIGHT.setter
    def LIGHT(self, new_mass: LightKey | str) -> None:
        self._set_type(unit_type=BaseDimensions.LIGHT, unit=new_mass)

    @property
    def CURRENT(self) -> CurrentKey | str:
        """Current unit of the unit system."""
        return self._CURRENT

    @CURRENT.setter
    def CURRENT(self, new_mass: CurrentKey | str) -> None:
        self._set_type(unit_type=BaseDimensions.CURRENT, unit=new_mass)

    @property
    def SOLID_ANGLE(self) -> SolidAngleKey | str:
        """Solid Angle unit of the unit system."""
        return self._SOLID_ANGLE

    @SOLID_ANGLE.setter
    def SOLID_ANGLE(self, new_mass: SolidAngleKey | str) -> None:
        self._set_type(unit_type=BaseDimensions.SOLID_ANGLE, unit=new_mass)

    def __repr__(self) -> str:
        units = ""
        for unit_type in BaseDimensions:
            unit = getattr(self, f"_{unit_type.name}")
            units += f"{unit_type.name}: {unit}\n"
        return units

    def __eq__(self, other_sys: object) -> bool:
        if not isinstance(other_sys, UnitSystem):
            return False
        return all(
            getattr(other_sys, attr) == value for attr, value in self.__dict__.items()
        )


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


class UnitSystemAlreadyRegistered(ValueError):
    """Raised when a unit system name conflicts with an existing unit system."""

    def __init__(self, name: str):
        super().__init__(
            f"Unable to register `{name}`: a unit system with this name already exists."
        )


class IncompleteUnitSystem(ValueError):
    """Raised when a unit system definition is missing one or more base dimensions."""

    def __init__(self, missing: list[BaseDimensions]):
        missing_names = ", ".join(dim.name for dim in missing)
        super().__init__(
            "Unable to register unit system: missing units for base "
            f"dimension(s): {missing_names}."
        )


class UnconfiguredPreferredUnit(ValueError):
    """Raised when a preferred unit cannot be resolved."""

    def __init__(self, unit: UnitKey | str):
        super().__init__(f"`{unit}` is not a configured unit.")


class PreferredUnitAlreadyRegistered(ValueError):
    """Raised when two preferred units have the same dimensions."""

    def __init__(self, existing_unit: str, conflicting_unit: str):
        message = (
            f"`{existing_unit}` is already configured as the preferred unit for "
            f"the same dimensions as `{conflicting_unit}`."
        )
        super().__init__(message)


class DimensionsKey:
    """Hashable key for matching dimension dictionaries."""

    def __init__(self, dimensions: Mapping[BaseDimensions, float]):
        self._dimensions: tuple[tuple[BaseDimensions, float], ...] = tuple(
            sorted(dimensions.items(), key=lambda item: item[0].name)
        )

    @override
    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, DimensionsKey) and self._dimensions == other._dimensions
        )

    @override
    def __hash__(self) -> int:
        return hash(self._dimensions)
