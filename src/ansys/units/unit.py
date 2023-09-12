import ansys.units as ansunits


class Unit:
    """
    Initializes a unit.

    Parameters
    ----------
    Name: str, dimension list
        Unit name or dimension list
    Config: dict
        dictionary of unit properties

    Methods
    -------

    Returns
    -------
    Unit
        Unit instance.
    """

    def __init__(self, _units: str, config: dict = None):
        self.name = _units

        if not config:
            config = self.get_config(self.name)
        if "type" not in config:
            config.update({"type": self.get_config(self.name)["type"]})
        for key in config:
            setattr(self, f"{key}", config[key])

        dimensions = ansunits.Dimensions(units=_units)
        self.dimensions = dimensions.dimensions

    def get_config(self, name: str) -> dict:
        if name in ansunits._fundamental_units:
            return ansunits._fundamental_units[name]

        if name in ansunits._derived_units:
            type = {"type": ansunits._QuantityType.derived}
            return dict(**type, **ansunits._derived_units[name])

        return {"type": ansunits._QuantityType.composite}

    def __str__(self):
        returned_string = ""
        attrs = self.__dict__
        for key in attrs:
            returned_string += f"{key}: {attrs[key]}\n"
        return returned_string

    def __mul__(self, __value):
        if isinstance(__value, Unit):
            temp_dimensions = [
                dim + __value.dimensions[idx] for idx, dim in enumerate(self.dimensions)
            ]
            new_dimensions = ansunits.Dimensions(dimensions=temp_dimensions)
            new_units = new_dimensions.units
            return Unit(_units=new_units)

        if isinstance(__value, (float, int)):
            return ansunits.Quantity(value=__value, units=self)

    def __rmul__(self, __value):
        return self.__mul__(__value)

    def __truediv__(self, __value):
        if isinstance(__value, Unit):
            temp_dimensions = [
                dim - __value.dimensions[idx] for idx, dim in enumerate(self.dimensions)
            ]
            new_dimensions = ansunits.Dimensions(dimensions=temp_dimensions)
            new_units = new_dimensions.units
            return Unit(_units=new_units)

    def __pow__(self, __value):
        temp_dimensions = [dim * __value for dim in self.dimensions]
        new_dimensions = ansunits.Dimensions(dimensions=temp_dimensions)
        return Unit(_units=new_dimensions.units)
