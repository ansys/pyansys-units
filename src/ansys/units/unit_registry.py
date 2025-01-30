# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
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
"""Provides the ``UnitRegistry`` class."""

import os

import yaml

from ansys.units import Unit


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

    def __init__(self, config="cfg.yaml", other: dict = None):
        unitdict = other or {}

        if config:
            file_dir = os.path.dirname(__file__)
            qc_path = os.path.join(file_dir, config)

            with open(qc_path, "r") as qc_yaml:
                qc_data = yaml.safe_load(qc_yaml)
                _base_units: dict = qc_data["base_units"]
                _derived_units: dict = qc_data["derived_units"]

            unitdict.update(**_base_units, **_derived_units)

        for unit in unitdict:
            setattr(self, unit, Unit(unit, unitdict[unit]))

    def __str__(self):
        returned_string = ""
        attrs = self.__dict__
        for key in attrs:
            returned_string += f"{key}, "
        return returned_string

    def __setattr__(self, name: str, unit: any) -> None:
        if hasattr(self, name):
            raise UnitAlreadyRegistered(name)
        self.__dict__[name] = unit

    def __iter__(self):
        for item in self.__dict__:
            yield getattr(self, item)


class UnitAlreadyRegistered(ValueError):
    """Raised when a unit has previously been registered."""

    def __init__(self, name: str):
        super().__init__(f"Unable to override `{name}` it has already been registered.")
