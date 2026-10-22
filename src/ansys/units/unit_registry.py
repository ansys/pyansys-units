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
from typing import TYPE_CHECKING, Any, overload
import weakref

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

# Bookkeeping for `export_custom_units`. Kept out of instance `__dict__` (which
# is treated as "the set of registered unit names" by `__iter__`/`__str__`) via
# a WeakKeyDictionary keyed on the owning `UnitRegistry` instance.
_CUSTOM_UNIT_DEFINITIONS: (
    "weakref.WeakKeyDictionary[UnitRegistry, dict[str, dict[str, Any]]]"
) = weakref.WeakKeyDictionary()
_CUSTOM_UNIT_ALIASES: "weakref.WeakKeyDictionary[UnitRegistry, dict[str, str]]" = (
    weakref.WeakKeyDictionary()
)


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
        the :meth:`register_unit` signature. An optional ``"aliases"`` key
        (a list of strings) is also supported.
    custom_units_file : str, optional
        Path to a ``YAML`` file previously produced by
        :meth:`export_custom_units`. Entries are loaded and registered the
        same way as ``custom_units``, and the two can be combined.

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
    ...     {"unit": "furlong", "composition": "m", "factor": 201.168,
    ...      "aliases": ["furlongs"]},
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
        custom_units_file: str | None = None,
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
        custom_units = list(custom_units) if custom_units else []
        if custom_units_file:
            custom_units += load_custom_units(custom_units_file)
        for cu in custom_units:
            self.register_unit(
                unit=cu["unit"],
                composition=cu["composition"],
                factor=cu["factor"],
                aliases=cu.get("aliases"),
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
        units and compound unit strings. This allows string-based lookup of
        custom registered units as well as standard unit expressions.

        Parameters
        ----------
        name : str
            The unit name or compound unit string to look up (e.g., "micron",
            "m", "kg mol^-1").

        Returns
        -------
        Unit
            The unit object.

        Raises
        ------
        AttributeError
            If the unit is not found in this registry or cannot be parsed.
        """
        # First check instance-registered units
        if name in self.__dict__:
            return self.__dict__[name]
        # Fall back to creating a Unit (handles built-ins and compound strings)
        try:
            return Unit(name)
        except Exception as e:
            raise AttributeError(f"Unit `{name}` not found in this registry.") from e

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

    @overload
    def register_unit(
        self,
        unit: str,
        definition: "Unit | Quantity[Any]",
        *,
        aliases: Sequence[str] | None = None,
    ) -> Unit: ...

    @overload
    def register_unit(
        self,
        *,
        unit: str,
        composition: str,
        factor: float,
        aliases: Sequence[str] | None = None,
    ) -> Unit: ...

    def register_unit(
        self,
        unit: str,
        definition: "Unit | Quantity[Any] | None" = None,
        *,
        composition: str | None = None,
        factor: float | None = None,
        aliases: Sequence[str] | None = None,
    ) -> Unit:
        """
        Register a new derived unit on this ``UnitRegistry`` instance.

        This is instance-scoped: it affects only this registry and does not
        mutate global state or other registries. The registered unit can be
        accessed as an attribute (e.g., ``ur.micron``) or via
        :meth:`get_unit` for string-based lookup.

        This method supports two equivalent calling conventions: an
        object-based form that accepts a ``Unit`` or ``Quantity`` definition,
        and a ``composition``/``factor`` form.

        Parameters
        ----------
        unit: str
            The symbol/name of the new unit (e.g., "micron").
        definition: Unit or Quantity, optional
            An object-based definition of the new unit, for example
            ``201.168 * m`` (a ``Quantity``) or a bare ``Unit`` instance
            (treated as a factor of ``1``). Mutually exclusive with
            ``composition``/``factor``.
        composition: str, optional
            A valid unit composition using existing configured units (e.g., "m").
            Must be provided together with ``factor``. Mutually exclusive with
            ``definition``.
        factor: float, optional
            Scale factor that relates the composition to this unit. Must be
            provided together with ``composition``. Mutually exclusive with
            ``definition``.
        aliases: sequence of str, optional
            Additional names that resolve to the same registered unit on this
            instance (e.g., ``["furlongs"]``).

        Returns
        -------
        Unit
            The registered unit attached on this instance.

        Raises
        ------
        UnitNameAlreadyRegistered
            If ``unit`` (or one of ``aliases``) is a built-in unit name, or
            already exists on this instance with a different effective
            definition (dimensions, SI scaling factor, or SI offset).
            Re-registering the same name with an equivalent definition is a
            no-op that returns the existing unit.
        ValueError
            If ``unit`` or an alias is empty, ``factor`` is not finite, or
            both/neither of ``definition`` and ``composition``/``factor`` are
            given.

        Notes
        -----
        The duplicate-name check compares effective definitions (dimensions,
        SI scaling factor, and SI offset). Re-registering the same name with
        an equivalent definition is idempotent. Built-in unit names can never
        be overridden, even with an equivalent definition. The check does not
        detect equivalent definitions registered under a *different* name.

        Examples
        --------
        >>> ur = UnitRegistry()
        >>> ur.register_unit(unit="micron", composition="m", factor=1e-6)
        >>> q = ur.Quantity(1, "micron")  # Use registry's Quantity method

        Object-based form, with an alias:

        >>> from ansys.units.common import m
        >>> ur.register_unit("furlong", 201.168 * m, aliases=["furlongs"])
        >>> ur.furlong == ur.furlongs
        True
        """
        unit = unit.strip()
        if not unit:
            raise ValueError("`unit` must be a non-empty string.")

        if definition is not None:
            if composition is not None or factor is not None:
                raise ValueError(
                    "Provide either `definition` or `composition`/`factor`, "
                    "not both."
                )
            from ansys.units.quantity import Quantity as _Quantity

            if isinstance(definition, _Quantity):
                composed = definition.units
                f = float(definition.value)
            elif isinstance(definition, Unit):
                composed = definition
                f = 1.0
            else:
                raise TypeError("`definition` must be a `Unit` or `Quantity` instance.")
        else:
            if composition is None or factor is None:
                raise ValueError(
                    "Provide either `definition` or both `composition` and " "`factor`."
                )
            composed = Unit(units=str(composition))
            f = float(factor)

        if not math.isfinite(f):
            raise ValueError("`factor` must be a finite number.")

        candidate = Unit(copy_from=composed)
        candidate._si_scaling_factor = composed.si_scaling_factor * f
        candidate._name = unit

        unit_is_new = not hasattr(self, unit)
        obj = self._register_name(unit, candidate)
        if unit_is_new:
            _CUSTOM_UNIT_DEFINITIONS.setdefault(self, {})[unit] = {
                "composition": composed.name,
                "factor": f,
            }

        if aliases:
            for alias in aliases:
                alias = alias.strip()
                if not alias:
                    raise ValueError("`aliases` entries must be non-empty strings.")
                alias_is_new = not hasattr(self, alias)
                self._register_name(alias, obj)
                if alias_is_new:
                    _CUSTOM_UNIT_ALIASES.setdefault(self, {})[alias] = unit

        return obj

    def _register_name(self, name: str, candidate: Unit) -> Unit:
        """
        Attach ``candidate`` on this instance under ``name``.

        Built-in collisions always raise. If ``name`` is already registered
        on this instance with an equivalent effective definition (dimensions,
        SI scaling factor, and SI offset), this is a no-op that returns the
        existing unit. Otherwise, a differing definition raises.
        """
        if name in _CONST_BASE_UNITS or name in _CONST_DERIVED_UNITS:
            raise UnitNameAlreadyRegistered(name)

        if hasattr(self, name):
            existing = getattr(self, name)
            if (
                existing.dimensions == candidate.dimensions
                and math.isclose(
                    existing.si_scaling_factor,
                    candidate.si_scaling_factor,
                    rel_tol=1e-12,
                )
                and math.isclose(existing.si_offset, candidate.si_offset, abs_tol=1e-12)
            ):
                return existing
            raise UnitNameAlreadyRegistered(name)

        object.__setattr__(self, name, candidate)
        return candidate

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

    def export_custom_units(self, path: str, *, overwrite: bool = False) -> None:
        """
        Export this registry's runtime-registered custom units to a YAML file.

        Only units registered via :meth:`register_unit` (directly, or through
        the ``custom_units``/``custom_units_file`` constructor parameters) are
        exported. Built-in units are never included. The resulting file can be
        reloaded with :func:`load_custom_units` or passed directly as
        ``custom_units_file`` to a new ``UnitRegistry``.

        Parameters
        ----------
        path : str
            Destination file path.
        overwrite : bool, optional
            Whether to overwrite ``path`` if it already exists. Default is
            ``False``.

        Raises
        ------
        ValueError
            If this registry has no custom registered units to export.
        FileExistsError
            If ``path`` already exists and ``overwrite`` is ``False``.

        Examples
        --------
        >>> from ansys.units.common import m
        >>> ur = UnitRegistry()
        >>> ur.register_unit("furlong", 201.168 * m, aliases=["furlongs"])
        >>> ur.export_custom_units("units.yaml")
        >>> ur2 = UnitRegistry(custom_units_file="units.yaml")
        >>> ur2.furlong is ur2.furlongs
        True
        """
        definitions = _CUSTOM_UNIT_DEFINITIONS.get(self, {})
        if not definitions:
            raise ValueError("This registry has no custom registered units to export.")

        if os.path.exists(path) and not overwrite:
            raise FileExistsError(
                f"`{path}` already exists. Pass `overwrite=True` to replace it."
            )

        aliases_by_unit: dict[str, list[str]] = {}
        for alias, canonical in _CUSTOM_UNIT_ALIASES.get(self, {}).items():
            aliases_by_unit.setdefault(canonical, []).append(alias)

        entries = []
        for name, info in definitions.items():
            entry: dict[str, Any] = {
                "unit": name,
                "composition": info["composition"],
                "factor": info["factor"],
            }
            if name in aliases_by_unit:
                entry["aliases"] = aliases_by_unit[name]
            entries.append(entry)

        with open(path, "w") as custom_units_yaml:
            yaml.safe_dump(
                {"custom_units": entries}, custom_units_yaml, sort_keys=False
            )


def load_custom_units(path: str) -> list[dict[str, Any]]:
    """
    Load custom unit definitions from a file written by ``export_custom_units``.

    Parameters
    ----------
    path : str
        Path to a ``YAML`` file previously produced by
        :meth:`UnitRegistry.export_custom_units`.

    Returns
    -------
    list of dict
        A list of custom unit definitions, suitable for passing directly as
        the ``custom_units`` constructor parameter of ``UnitRegistry``.

    Examples
    --------
    >>> ur.export_custom_units("units.yaml")
    >>> custom_units = load_custom_units("units.yaml")
    >>> ur2 = UnitRegistry(custom_units=custom_units)
    """
    with open(path, "r") as custom_units_yaml:
        data = yaml.safe_load(custom_units_yaml) or {}
    return data.get("custom_units", [])


class AliasAlreadyRegistered(ValueError):
    """Raised when an alias conflicts with an existing unit or alias."""

    def __init__(self, name: str):
        super().__init__(
            f"Unable to register alias `{name}`: it already exists as a unit or alias."
        )


class UnitNameAlreadyRegistered(ValueError):
    """
    Raised when a unit name conflicts with an existing name.

    This is raised when ``unit`` (or an alias) is a built-in unit name, or
    when it is already registered on the instance with a *different*
    effective definition (dimensions, SI scaling factor, or SI offset).
    Re-registering the same name with an equivalent definition is a no-op and
    does not raise. Units with different names but equivalent definitions
    (same composition and factor) are also not detected as conflicts.
    """

    def __init__(self, name: str):
        super().__init__(
            f"Unable to register `{name}`: a unit with this name already exists."
        )
