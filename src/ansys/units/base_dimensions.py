"""Provides the ``BaseDimensions`` class."""
from enum import Enum


class BaseDimensions(Enum):
    """
    Supplies all valid base dimensions used in dimensional analysis.

    Used as dictionary keys for defining a `Dimensions` object.

    Attributes
    ----------
    MASS
    LENGTH
    TIME
    TEMPERATURE
    TEMPERATURE_DIFFERENCE
    ANGLE
    CHEMICAL_AMOUNT
    LIGHT
    CURRENT
    SOLID_ANGLE
    """

    MASS = 0
    LENGTH = 1
    TIME = 2
    TEMPERATURE = 3
    TEMPERATURE_DIFFERENCE = 4
    ANGLE = 5
    CHEMICAL_AMOUNT = 6
    LIGHT = 7
    CURRENT = 8
    SOLID_ANGLE = 9
