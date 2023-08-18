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

_dimension_order: dict = qc_data["dimension_order"]
_multipliers: dict = qc_data["multipliers"]
_unit_systems: dict = qc_data["unit_systems"]
_api_quantity_map: dict = qc_data["api_quantity_map"]
_fundamental_units: dict = qc_data["fundamental_units"]
_derived_units: dict = qc_data["derived_units"]
