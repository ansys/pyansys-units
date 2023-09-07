import os

import yaml

import ansys.units as pyunits


class UnitRegistry:
    """
    Initializes a Unit Registry.

    Parameters
    ----------
    Config: filename.yaml
        Custom units.
    Other: Dict
        Dictionary of units.
    Methods
    -------

    Returns
    -------
    UnitRegistry
        contains all units from cfg.yaml.
    """

    def __init__(self, config="cfg.yaml", other={}):
        unitdict = other
        if config:
            file_path = os.path.relpath(__file__)
            file_dir = os.path.dirname(file_path)
            qc_path = os.path.join(file_dir, config)

            with open(qc_path, "r") as qc_yaml:
                qc_data = yaml.safe_load(qc_yaml)
                _fundamental_units: dict = qc_data["fundamental_units"]
                _derived_units: dict = qc_data["derived_units"]

            unitdict.update(**_fundamental_units, **_derived_units)

        for unit in unitdict:
            setattr(self, unit, pyunits.Unit(unit, unitdict[unit]))

    def newUnit(self, unit):
        setattr(self, unit.name, unit)

    def __add__(self, other):
        self.__dict__.update(other.__dict__)
