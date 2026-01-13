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

from collections.abc import Generator, Mapping
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
from ansys.units._constants import _base_units as _CONST_BASE_UNITS
from ansys.units._constants import _derived_units as _CONST_DERIVED_UNITS
from ansys.units.unit import Unit


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
        Dictionary for additional units.

    Examples
    --------
    >>> from ansys.units import UnitRegistry, Unit
    >>> ureg = UnitRegistry()
    >>> assert ureg.kg == Unit(units="kg")
    >>> fps = Unit("ft s^-1")
    >>> ureg.foot_per_sec = fps
    """

    def __init__(
        self,
        config: str = "cfg.yaml",
        other: Mapping[
            str, Mapping[str, Any]
        ] = {},  # pyright: ignore[reportCallInDefaultInitializer]
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
                raise UnitAlreadyRegistered(unit_name)

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
            raise UnitAlreadyRegistered(name)
        self.__dict__[name] = unit

    def __iter__(self) -> Generator[str]:
        yield from self.__dict__

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
        mutate global state or other registries.

        Parameters
        ----------
        unit: str
            The symbol/name of the new unit (e.g., "Q"). Preferred keyword.
        composition: str
            A valid unit composition using existing configured units (e.g., "N m").
        factor: float
            Scale factor that relates the composition to this unit.

        Returns
        -------
        Unit
            The registered unit attached on this instance.

        Raises
        ------
        UnitAlreadyRegistered
            If a unit with the same name already exists on this instance or is built-in.
        ValueError
            If ``unit`` is empty or ``factor`` is not finite.
        """
        unit = unit.strip()
        if not unit:
            raise ValueError("`unit` must be a non-empty string.")
        f = float(factor)
        if not math.isfinite(f):
            raise ValueError("`factor` must be a finite number.")

        # Prevent overriding built-ins or existing attributes on this instance
        if (
            unit in _CONST_BASE_UNITS
            or unit in _CONST_DERIVED_UNITS
            or hasattr(self, unit)
        ):
            raise UnitAlreadyRegistered(unit)

        composed = Unit(units=str(composition))
        obj = Unit(copy_from=composed)

        obj._si_scaling_factor *= f
        obj._name = unit
        object.__setattr__(self, unit, obj)
        return obj


class UnitAlreadyRegistered(ValueError):
    """Raised when a unit has previously been registered."""

    def __init__(self, name: str):
        super().__init__(f"Unable to override `{name}` it has already been registered.")
