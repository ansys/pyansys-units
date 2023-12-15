import os

import yaml


def test_config_import():
    root = os.path.abspath(os.curdir)
    qc_path = os.path.join(root, "src/ansys/units/cfg.yaml")
    map_path = os.path.join(root, "src/ansys/units/quantity_maps/base_map.yaml")

    with open(qc_path, "r") as qc_yaml:
        qc_data = yaml.safe_load(qc_yaml)

    with open(map_path, "r") as quantity_map:
        map_data = yaml.safe_load(quantity_map)

    multipliers: dict = qc_data["multipliers"]
    unit_systems: dict = qc_data["unit_systems"]
    api_quantity_map: dict = map_data["api_quantity_map"]
    base_units: dict = qc_data["base_units"]
    derived_units: dict = qc_data["derived_units"]
