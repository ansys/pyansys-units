"""Provides the ``UnitRegistry`` class."""
import os

import yaml

import ansys.units as ansunits


class UnitAlreadyRegistered(ValueError):
    """Provides the error when the specified unit is trying to override a registered
    unit."""

    def __init__(self, name):
        super().__init__(f"Unable to override `{name}` it has already been registered.")


class UnitRegistry:
    """
    A container of common ``Units`` for ease of use. Defaults to all units in
    '_base_units' and '_derived_units'.

    Parameters
    ----------
    config: str, optional
        Custom .yaml file or `cfg.yaml`. Format must match `cfg.yaml`.
    other: dict, optional
        Dictionary for extra units.

    Examples
    --------
    import ansys.units as ansunits
    ureg = ansunits.UnitRegistry()

    ureg.kg == ansunits.Unit(units= "kg")
    """

    def __init__(self, config="cfg.yaml", other: dict = None):
        unitdict = other or {}

        if config:
            file_path = os.path.relpath(__file__)
            file_dir = os.path.dirname(file_path)
            qc_path = os.path.join(file_dir, config)

            with open(qc_path, "r") as qc_yaml:
                qc_data = yaml.safe_load(qc_yaml)
                _base_units: dict = qc_data["base_units"]
                _derived_units: dict = qc_data["derived_units"]

            unitdict.update(**_base_units, **_derived_units)

        for unit in unitdict:
            setattr(self, unit, ansunits.Unit(unit, unitdict[unit]))

    def __str__(self):
        returned_string = ""
        attrs = self.__dict__
        for key in attrs:
            returned_string += f"{key}, "
        return returned_string

    def __setattr__(self, __name: str, unit: any) -> None:
        if hasattr(self, __name):
            raise UnitAlreadyRegistered(__name)
        self.__dict__[__name] = unit
