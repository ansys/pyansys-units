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
