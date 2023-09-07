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

    def __init__(self, _name: str, config: dict):
        self.name = _name
        for key in config:
            setattr(self, f"{key}", config[key])

    def __str__(self):
        returned_string = ""
        attrs = self.__dict__
        for key in attrs:
            returned_string += f"{key}: {attrs[key]}\n"
        return returned_string
