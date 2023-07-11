"""
units.

pyunits
"""

# try:
#     import importlib.metadata as importlib_metadata
# except ModuleNotFoundError:
#     import importlib_metadata

# __version__ = importlib_metadata.version(__name__.replace(".", "-"))


from ansys.units.dimensions import Dimensions, DimensionsError  # noqa: F401
from ansys.units.quantity import Quantity, QuantityError  # noqa: F401
from ansys.units.quantity_map import QuantityMap, QuantityMapError  # noqa: F401
from ansys.units.unit_system import UnitSystem, UnitSystemError  # noqa: F401
from ansys.units.units_table import UnitsTable  # noqa: F401
