"""Pyunits is a pythonic interface for units, unit systems, and unit conversions."""


try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version(__name__.replace(".", "-"))

import os

from ansys.units._constants import (  # noqa: F401
    _base_units,
    _derived_units,
    _multipliers,
    _quantity_units_table,
    _QuantityType,
    _unit_systems,
)
from ansys.units.base_dimensions import BaseDimensions  # noqa: F401
from ansys.units.dimensions import Dimensions  # noqa: F401
from ansys.units.quantity import Quantity, get_si_value  # noqa: F401
from ansys.units.systems import UnitSystem  # noqa: F401
from ansys.units.unit import Unit  # noqa: F401
from ansys.units.unit_registry import UnitRegistry  # noqa: F401

_THIS_DIRNAME = os.path.dirname(__file__)
_README_FILE = os.path.normpath(os.path.join(_THIS_DIRNAME, "docs", "README.rst"))

if os.path.exists(_README_FILE):
    with open(_README_FILE, encoding="utf8") as f:
        __doc__ = f.read()
