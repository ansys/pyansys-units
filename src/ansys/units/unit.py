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
            self.name = name
            dic = pyunits._fundamental_units[name]
            for key in dic:
                setattr(self, f"{key}", dic[key])

        elif name in [*pyunits._derived_units]:
            self.name = name
            dic = pyunits._derived_units[name]
            for key in dic:
                setattr(self, f"{key}", dic[key])

    def __str__(self):
        returned_string = ""
        attrs = self.__dict__
        for key in attrs:
            returned_string += f"{key}: {attrs[key]}\n"
        return returned_string
