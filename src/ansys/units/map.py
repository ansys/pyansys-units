"""Provides the ``QuantityMap`` class."""
import ansys.units as ansunits


class QuantityMap(object):
    """
    A class that contains quantity map and equivalent units.

    Parameters
    ----------
    quantity_map : dict
        Dictionary containing quantity map units and powers.

    Attributes
    ----------
    units
    """

    def __init__(self, quantity_map):
        for item in quantity_map:
            if item not in ansunits._api_quantity_map:
                raise QuantityMapError.UNKNOWN_MAP_ITEM(item)

        self._units = self._map_to_units(quantity_map)

    def _map_to_units(self, quantity_map: dict) -> str:
        """
        Convert a quantity map into a Unit.

        Parameters
        ----------
        quantity_map : dict
            Quantity map to convert to a Unit.

        Returns
        -------
        Unit
            Unit object representation of the quantity map.
        """
        base_unit = ansunits.Unit()
        for term, power in quantity_map.items():
            base_unit *= ansunits.Unit(ansunits._api_quantity_map[term]) ** power

        return base_unit

    @property
    def units(self):
        """Unit representation of the quantity map."""
        return self._units


class QuantityMapError(ValueError):
    """Provides custom quantity map errors."""

    def __init__(self, err):
        super().__init__(err)

    @classmethod
    def UNKNOWN_MAP_ITEM(cls, item):
        """Returns in case the given quantity map is not in the yaml."""
        return cls(f"`{item}` is not a valid quantity map item.")
