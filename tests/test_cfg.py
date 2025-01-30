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

import os

import yaml


def test_config_import():
    root = os.path.abspath(os.curdir)
    qc_path = os.path.join(root, "src/ansys/units/cfg.yaml")
    table_path = os.path.join(root, "src/ansys/units/quantity_tables/si_table.yaml")

    with open(qc_path, "r") as qc_yaml:
        qc_data = yaml.safe_load(qc_yaml)

    with open(table_path, "r") as table:
        table_data = yaml.safe_load(table)

    multipliers: dict = qc_data["multipliers"]
    unit_systems: dict = qc_data["unit_systems"]
    quantity_units_table: dict = table_data["quantity_units_table"]
    base_units: dict = qc_data["base_units"]
    derived_units: dict = qc_data["derived_units"]
