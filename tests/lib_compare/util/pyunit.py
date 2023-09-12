from typing import Dict

#
# adding code in here implies something missing in the library
#


class TestDimension(list):
    MASS = 0
    LENGTH = 1
    TIME = 2
    TEMPERATURE = 3
    ANGLE = 4
    CHEMICAL_AMOUNT = 5
    LIGHT = 6
    CURRENT = 7
    SOLID_ANGLE = 8

    def __init__(self, d: Dict[int, float]):
        dims = 9 * [0]
        for dim, exponent in d.items():
            dims[dim] = exponent
        super().__init__(dims)
