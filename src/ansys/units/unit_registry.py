"""Provides the ``UnitRegistry`` class."""
import os

import yaml

import ansys.units as ansunits


class UnitRegistry:
    """
    A container of valid ``Unit`` instances.

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
            raise RegistryError.UNIT_ALREADY_REGISTERED(__name)
        self.__dict__[__name] = unit


class RegistryError(ValueError):
    """Custom dimensions errors."""

    def __init__(self, err):
        super().__init__(err)

    @classmethod
    def UNIT_ALREADY_REGISTERED(cls, name):
        """Return in case of trying to override a registered unit."""
        return cls(f"Unable to override `{name}` it has already been registered.")
