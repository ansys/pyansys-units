import ansys.units as ansunits


class Unit:
    """
    Initializes a Unit. Contains all the unit information.

    Parameters
    ----------
    Name: str,
        Name of the unit or string chain of combined units
    Config: dict
        dictionary of unit properties

    Methods
    -------

    Returns
    -------
    Unit
        Unit instance.
    """

    def __init__(self, units: str, config: dict = None):
        self._name = units

        if not config:
            config = self._get_config(self._name)
        if config:
            for key in config:
                setattr(self, f"_{key}", config[key])

        self._dimensions = ansunits.Dimensions(units=units)

    def _get_config(self, name: str) -> dict:
        if name in ansunits._fundamental_units:
            return ansunits._fundamental_units[name]

        if name in ansunits._derived_units:
            return ansunits._derived_units[name]

        return

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def dimensions(self):
        return self._dimensions

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
            return Unit(units=new_units)

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
            return Unit(units=new_units)

    def __pow__(self, __value):
        temp_dimensions = [dim * __value for dim in self.dimensions]
        new_dimensions = ansunits.Dimensions(dimensions=temp_dimensions)
        return Unit(units=new_dimensions.units)
