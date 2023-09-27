"""Provides the ``UnitRegistry`` class."""
import os

import yaml

import ansys.units as ansunits


class UnitRegistry:
    """
    Initialize a container of common ``Units`` for ease of use.

    Parameters
    ----------
    config: filename.yaml, optional
        Custom .yaml file or `cfg.yaml`. Format must match `cfg.yaml`.
    other: Dict, optional
        Dictionary for extra units.

    Examples
    --------
    import ansys.units as ansunits
    ureg = ansunits.UnitRegistry()

    ureg.kg == ansunits.Unit(units= "kg")

    Returns
    -------
    UnitRegistry
        contains all units initialized from the parameters.
        defaults to all units in '_fundamental_units' and '_derived_units'
    """

    def __init__(self, config="cfg.yaml", other: dict = None):
        unitdict = other or {}

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
            setattr(self, unit, ansunits.Unit(unit, unitdict[unit]))

    def __str__(self):
        returned_string = ""
        attrs = self.__dict__
        for key in attrs:
            returned_string += f"{key}, "
        return returned_string
