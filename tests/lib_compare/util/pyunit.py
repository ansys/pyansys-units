from typing import Dict

#
# adding code in here implies something missing in the library
#


class TestDimension(list):
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

    def __init__(self, d: Dict[int, float]):
        dims = 10 * [0.0]
        for dim, exponent in d.items():
            dims[dim] = exponent
        super().__init__(dims)
