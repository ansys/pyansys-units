"""Provides the ``QuantityMap`` class."""
from ansys.units import Unit, _api_quantity_map


class UnknownMapItem(ValueError):
    """Provides the error when the specified quantity map is undefined in the yaml."""

    def __init__(self, item):
        super().__init__(f"`{item}` is not a valid quantity map item.")


class QuantityMap(object):
    """
    A class that contains quantity map and equivalent units.

    Parameters
    ----------
    quantity_map : dict[str, int]
        Dictionary containing quantity map units and their exponents.

    Attributes
    ----------
    units
    """

    def __init__(self, quantity_map):
        for item in quantity_map:
            if item not in _api_quantity_map:
                raise UnknownMapItem(item)

        self._units = self._map_to_units(quantity_map)

    def _map_to_units(self, quantity_map: dict) -> str:
        """
        Convert a quantity map into a Unit.

        Parameters
        ----------
        quantity_map : dict[str, int]
            Quantity map to convert to a Unit.

        Returns
        -------
        Unit
            Unit object representation of the quantity map.
        """
        base_unit = Unit()
        for term, exponent in quantity_map.items():
            base_unit *= Unit(_api_quantity_map[term]) ** exponent

        return base_unit

    @property
    def units(self):
        """Unit representation of the quantity map."""
        return self._units
