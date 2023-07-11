"""
units.

pyunits
"""

# try:
#     import importlib.metadata as importlib_metadata
# except ModuleNotFoundError:
#     import importlib_metadata

# __version__ = importlib_metadata.version(__name__.replace(".", "-"))


from ansys.units.dimensions import (  # noqa: F401
    Dimensions,
    DimensionsError,
)
from ansys.units.quantity import Quantity, QuantityError  # noqa: F401
from ansys.units.quantity_map import (  # noqa: F401
    QuantityMap,
    QuantityMapError,
)
from ansys.units.unit_system import (  # noqa: F401
    UnitSystem,
    UnitSystemError,
)
from ansys.units.units_table import UnitsTable  # noqa: F401
