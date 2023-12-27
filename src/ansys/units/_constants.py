"""Provides ``QuantityType`` class."""
import os

import yaml


class _QuantityType:
    composite = "Composite"
    derived = "Derived"
    no_type = "No Type"
    temperature = "Temperature"
    temperature_difference = "Temperature Difference"


# Single import of static tables

file_path = os.path.relpath(__file__)
file_dir = os.path.dirname(file_path)
qc_path = os.path.join(file_dir, "cfg.yaml")

with open(qc_path, "r") as qc_yaml:
    qc_data = yaml.safe_load(qc_yaml)

_multipliers: dict = qc_data["multipliers"]
_unit_systems: dict = qc_data["unit_systems"]
_base_units: dict = qc_data["base_units"]
_derived_units: dict = qc_data["derived_units"]

table_path = os.path.join(file_dir, "quantity_tables/si_table.yaml")

with open(table_path, "r") as table:
    table_data = yaml.safe_load(table)
_quantity_units_table: dict = table_data["quantity_units_table"]
