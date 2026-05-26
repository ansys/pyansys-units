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
"""Provides the ``UnitRegistry`` class and instance-scoped unit registration."""

from collections.abc import Generator, Mapping, Sequence
import math
import os
from typing import TYPE_CHECKING, Any

import yaml

from ansys.units._constants import (
    _BaseUnitInfo,
)
from ansys.units._constants import (
    _DerivedUnitInfo,
)
from ansys.units._constants import _aliases as _CONST_ALIASES
from ansys.units._constants import _base_units as _CONST_BASE_UNITS
from ansys.units._constants import _derived_units as _CONST_DERIVED_UNITS
from ansys.units.unit import Unit

if TYPE_CHECKING:
    from ansys.units.quantity import Quantity  # noqa: F401


class UnitRegistry:
    """
    A representation of valid ``Unit`` instances.

    All base and derived units loaded from the configuration file, `cfg.yaml`,
    on package initialization are provided by default.

    Parameters
    ----------
    config: str, optional
        Path of a ``YAML`` configuration file, which can be a custom file, and
        defaults to the provided file, ``cfg.yaml``. Custom configuration files
        must match the format of the default configuration file.
    other: dict, optional
        Dictionary for additional units (uses config file format).
    custom_units : list of dict, optional
        List of custom units to register during construction. Each dict must
        have keys ``"unit"``, ``"composition"``, and ``"factor"`` matching
        the :meth:`register_unit` signature.

    Examples
    --------
    >>> from ansys.units import UnitRegistry, Unit
    >>> ureg = UnitRegistry()
    >>> assert ureg.kg == Unit(units="kg")
    >>> fps = Unit("ft s^-1")
    >>> ureg.foot_per_sec = fps

    Register custom units at construction:

    >>> ur = UnitRegistry(custom_units=[
    ...     {"unit": "micron", "composition": "m", "factor": 1e-6},
    ...     {"unit": "inch", "composition": "m", "factor": 0.0254},
    ... ])
    >>> q = ur.Quantity(10, "micron")
    """

    def __init__(
        self,
        config: str = "cfg.yaml",
        other: Mapping[
            str, Mapping[str, Any]
        ] = {},  # pyright: ignore[reportCallInDefaultInitializer]
        custom_units: Sequence[Mapping[str, Any]] | None = None,
    ):
        unitdict = dict(other)

        if config:
            file_dir = os.path.dirname(__file__)
            qc_path = os.path.join(file_dir, config)

            with open(qc_path, "r") as qc_yaml:
                qc_data = yaml.safe_load(qc_yaml)
                _base_units: dict[str, _BaseUnitInfo] = qc_data["base_units"]
                _derived_units: dict[str, _DerivedUnitInfo] = qc_data["derived_units"]

            unitdict |= _base_units | _derived_units

        for unit_name in unitdict:
            # Prevent overriding attributes already present on this instance
            if hasattr(self, unit_name):
                raise UnitNameAlreadyRegistered(unit_name)

            cfg = unitdict[unit_name]
            if unit_name in _CONST_BASE_UNITS or unit_name in _CONST_DERIVED_UNITS:
                object.__setattr__(self, unit_name, Unit(unit_name, cfg))
            else:
                # For dynamically registered units not present in constants, build
                # from their composition so dimensions/si data are correct, then
                # override the name to the desired symbol and attach config.
                if "composition" in cfg:
                    composed = Unit(units=str(cfg["composition"]))
                    obj = Unit(copy_from=composed)
                    obj._name = unit_name
                    object.__setattr__(self, unit_name, obj)
                else:
                    object.__setattr__(self, unit_name, Unit(unit_name, cfg))

        # Register custom units using the same logic as register_unit
        if custom_units:
            for cu in custom_units:
                self.register_unit(
                    unit=cu["unit"],
                    composition=cu["composition"],
                    factor=cu["factor"],
                )

    def __str__(self):
        returned_string = ""
        attrs = self.__dict__
        for key in attrs:
            returned_string += f"{key}, "
        return returned_string

    if TYPE_CHECKING:

        def __getattr__(self, name: str) -> Unit: ...

    def __setattr__(self, name: str, unit: Any) -> None:
        if hasattr(self, name):
            raise UnitNameAlreadyRegistered(name)
        self.__dict__[name] = unit

    def __iter__(self) -> Generator[str]:
        yield from self.__dict__

    def get_unit(self, name: str) -> Unit:
        """
        Look up a unit by name from this registry.

        Checks instance-registered units first, then falls back to built-in
        units. This allows string-based lookup of custom registered units.

        Parameters
        ----------
        name : str
            The unit name to look up.

        Returns
        -------
        Unit
            The unit object.

        Raises
        ------
        AttributeError
            If the unit is not found in this registry or built-ins.
        """
        if name in self.__dict__:
            return self.__dict__[name]
        # Fall back to creating from global config
        if name in _CONST_BASE_UNITS or name in _CONST_DERIVED_UNITS:
            return Unit(name)
        raise AttributeError(f"Unit `{name}` not found in this registry.")

    def Quantity(
        self,
        value: "int | float | Sequence[float]",
        units: "str | Unit",
    ) -> "Quantity":
        """
        Create a Quantity using this registry's units.

        This method allows creating quantities with instance-registered units
        using string names.

        Parameters
        ----------
        value : int, float, or sequence
            The numeric value.
        units : str or Unit
            The unit name (looked up in this registry) or a Unit object.

        Returns
        -------
        Quantity
            The created quantity.

        Examples
        --------
        >>> ur = UnitRegistry()
        >>> ur.register_unit(unit="micron", composition="m", factor=1e-6)
        >>> q = ur.Quantity(1, "micron")
        >>> print(q)
        1.0 micron
        """
        from ansys.units.quantity import Quantity as _Quantity

        if isinstance(units, str):
            units = self.get_unit(units)
        return _Quantity(value, units)

    def register_unit(
        self,
        *,
        unit: str,
        composition: str,
        factor: float,
    ) -> Unit:
        """
        Register a new derived unit on this ``UnitRegistry`` instance.

        This is instance-scoped: it affects only this registry and does not
        mutate global state or other registries. The registered unit can be
        accessed as an attribute (e.g., ``ur.micron``) or via
        :meth:`get_unit` for string-based lookup.

        Parameters
        ----------
        unit: str
            The symbol/name of the new unit (e.g., "micron").
        composition: str
            A valid unit composition using existing configured units (e.g., "m").
        factor: float
            Scale factor that relates the composition to this unit.

        Returns
        -------
        Unit
            The registered unit attached on this instance.

        Raises
        ------
        UnitNameAlreadyRegistered
            If a unit with the same name already exists on this instance or
            as a built-in. This is a name-only check and does not detect
            equivalent definitions with different names.
        ValueError
            If ``unit`` is empty or ``factor`` is not finite.

        Notes
        -----
        The name collision check is superficial (name-only). Two units with
        different names but equivalent definitions (same composition and factor)
        can both be registered without error.

        Examples
        --------
        >>> ur = UnitRegistry()
        >>> ur.register_unit(unit="micron", composition="m", factor=1e-6)
        >>> q = ur.Quantity(1, "micron")  # Use registry's Quantity method
        """
        unit = unit.strip()
        if not unit:
            raise ValueError("`unit` must be a non-empty string.")
        f = float(factor)
        if not math.isfinite(f):
            raise ValueError("`factor` must be a finite number.")

        # Name-only collision check against built-ins and this instance
        if (
            unit in _CONST_BASE_UNITS
            or unit in _CONST_DERIVED_UNITS
            or hasattr(self, unit)
        ):
            raise UnitNameAlreadyRegistered(unit)

        composed = Unit(units=str(composition))
        obj = Unit(copy_from=composed)

        obj._si_scaling_factor *= f
        obj._name = unit
        object.__setattr__(self, unit, obj)
        return obj

    def register_alias(
        self,
        alias: str,
        canonical: str,
    ) -> None:
        """
        Register a new alias for an existing unit.

        The alias is added to the global alias table so that it can be used
        anywhere a unit string is accepted (``Unit()``, ``Quantity()``, etc.).

        Parameters
        ----------
        alias : str
            The alias name (e.g., ``"deg"``).
        canonical : str
            The canonical unit name the alias resolves to
            (e.g., ``"degree"``). Must be a configured base or derived unit,
            or an existing alias.

        Raises
        ------
        AliasAlreadyRegistered
            If ``alias`` is already registered as a unit or alias.
        ValueError
            If ``canonical`` is not a known unit or alias.
        """
        alias = alias.strip()
        canonical = canonical.strip()
        if not alias:
            raise ValueError("`alias` must be a non-empty string.")
        if not canonical:
            raise ValueError("`canonical` must be a non-empty string.")

        # Prevent shadowing existing units
        if (
            alias in _CONST_BASE_UNITS
            or alias in _CONST_DERIVED_UNITS
            or alias in _CONST_ALIASES
        ):
            raise AliasAlreadyRegistered(alias)

        # Validate the canonical target exists
        if not (
            canonical in _CONST_BASE_UNITS
            or canonical in _CONST_DERIVED_UNITS
            or canonical in _CONST_ALIASES
        ):
            raise ValueError(
                f"`{canonical}` is not a configured unit or existing alias."
            )

        _CONST_ALIASES[alias] = canonical


class AliasAlreadyRegistered(ValueError):
    """Raised when an alias conflicts with an existing unit or alias."""

    def __init__(self, name: str):
        super().__init__(
            f"Unable to register alias `{name}`: it already exists as a unit or alias."
        )


class UnitNameAlreadyRegistered(ValueError):
    """
    Raised when a unit name conflicts with an existing name.

    This is a name-only check. Units with different names but equivalent definitions
    (same composition and factor) are not detected.
    """

    def __init__(self, name: str):
        super().__init__(
            f"Unable to register `{name}`: a unit with this name already exists."
        )
