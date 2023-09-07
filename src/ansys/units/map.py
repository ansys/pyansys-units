"""Provides the ``QuantityMap`` class."""
import ansys.units as ansunits


class QuantityMap(object):
    """
    Creates a ``QuantityMap`` object based on a given quantity map.

    Parameters
    ----------
    quantity_map : dict
        Dictionary containing quantity map units and values.

    Returns
    -------
    QuantityMap
        Quantity map instance.
    """

    def __init__(self, quantity_map):
        self._units = ansunits.Units()

        for item in quantity_map:
            if item not in ansunits._api_quantity_map:
                raise QuantityMapError.UNKNOWN_MAP_ITEM(item)

        self._units = self._map_to_units(quantity_map)

    def _map_to_units(self, quantity_map: dict) -> str:
        """
        Convert a quantity map into a unit string.

        Parameters
        ----------
        quantity_map : dict
            Quantity map to convert to a unit string.

        Returns
        -------
        str
            Unit string representation of the quantity map.
        """
        unit_dict = {
            ansunits._api_quantity_map[term]: power
            for term, power in quantity_map.items()
        }

        units = ""

        # Split unit string into terms and parse data associated with individual terms
        for terms in unit_dict:
            for term in terms.split(" "):
                _, unit_term, unit_term_power = self._units.filter_unit_term(term)

                unit_term_power *= unit_dict[terms]

                if unit_term_power == 1.0:
                    units += f" {unit_term}"
                elif unit_term_power != 0.0:
                    units += f" {unit_term}^{unit_term_power}"

        return self._units.condense(units=units)

    @property
    def units(self):
        """Unit string representation of the quantity map."""
        return self._units


class QuantityMapError(ValueError):
    """Provides custom quantity map errors."""

    def __init__(self, err):
        super().__init__(err)

    @classmethod
    def UNKNOWN_MAP_ITEM(cls, item):
        return cls(f"`{item}` is not a valid quantity map item.")
