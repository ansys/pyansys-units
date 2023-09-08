import ansys.units as pyunits


class Unit:
    """
    Initializes a unit.

    Parameters
    ----------
    Name: str
        Unit name.
    Config: dict
        dictionary of unit properties

    Methods
    -------

    Returns
    -------
    Unit
        Unit instance.
    """

    def __init__(self, _name: str, config: dict = None):
        self.name = _name
        if not config:
            config = self.get_config(_name)
        for key in config:
            setattr(self, f"{key}", config[key])

    def get_config(self, name: str) -> dict:
        if name in pyunits._fundamental_units:
            return pyunits._fundamental_units[name]

        if name in pyunits._derived_units:
            type = {"type": pyunits._QuantityType.derived}
            return dict(type, **pyunits._derived_units[name])

        return {"type": pyunits._QuantityType.composite}

    def __str__(self):
        returned_string = ""
        attrs = self.__dict__
        for key in attrs:
            returned_string += f"{key}: {attrs[key]}\n"
        return returned_string
