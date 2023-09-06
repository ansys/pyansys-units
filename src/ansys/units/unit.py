import ansys.units as pyunits


class Unit:
    """
    Initializes a unit.

    Parameters
    ----------
    name: str
        Unit name.

    Methods
    -------

    Returns
    -------
    Unit
        Unit instance.
    """

    def __init__(self, name: str):
        if name in [*pyunits._fundamental_units]:
            self._name = name
            dic = pyunits._fundamental_units[name]
            for key in dic:
                setattr(self, f"_{key}", dic[key])

        elif name in [*pyunits._derived_units]:
            self._name = name
            dic = pyunits._derived_units[name]
            for key in dic:
                setattr(self, f"_{key}", dic[key])

    def __str__(self):
        return f"""
                Unit: {self._name}
                Type: {self._type}
                Factor: {self._factor}
                Offset: {self._offset}"""
