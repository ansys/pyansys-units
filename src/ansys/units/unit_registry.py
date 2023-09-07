import ansys.units as pyunits


class UnitRegistry:
    """
    Initializes a Unit Registry.

    Parameters
    ----------
    Config: dict, None
        Custom dictionary of units.

    Methods
    -------

    Returns
    -------
    UnitRegistry
        contains all units from cfg.yaml.
    """

    def __init__(self, config=None):
        if not config:
            unitdict = dict(pyunits._fundamental_units, **pyunits._derived_units)
        else:
            unitdict = config

        for unit in unitdict:
            setattr(self, unit, pyunits.Unit(unit, unitdict[unit]))

    def newUnit(self, unit):
        setattr(self, unit.name, unit)

    def __add__(self, other):
        self.__dict__.update(other.__dict__)
