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
"""Provides ``QuantityType`` class."""

import os
from typing import TYPE_CHECKING, TypedDict

import yaml

if TYPE_CHECKING:
    from ansys.units.quantity_tables.keys import *  # noqa: F403


class _QuantityType:
    composite = "Composite"
    derived = "Derived"
    no_type = "No Type"
    temperature = "Temperature"
    temperature_difference = "Temperature Difference"


# Single import of static tables

file_dir = os.path.dirname(__file__)
qc_path = os.path.join(file_dir, "cfg.yaml")

with open(qc_path, "r") as qc_yaml:
    qc_data = yaml.safe_load(qc_yaml)

_multipliers: dict[str, float] = qc_data["multipliers"]
_unit_systems: dict["Systems", dict["BaseUnit", "UnitKey"]] = qc_data["unit_systems"]


class _BaseUnitInfo(TypedDict):
    type: "BaseUnit"
    si_scaling_factor: float
    si_offset: float


_base_units: dict[str, _BaseUnitInfo] = qc_data["base_units"]


class _DerivedUnitInfo(TypedDict):
    composition: str
    factor: float


_derived_units: dict[str, _DerivedUnitInfo] = qc_data["derived_units"]

table_path = os.path.join(file_dir, "quantity_tables/si_table.yaml")

with open(table_path, "r") as table:
    table_data = yaml.safe_load(table)
_quantity_units_table: dict["QuantityKey", str] = table_data["quantity_units_table"]
