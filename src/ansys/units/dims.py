from __future__ import annotations
from enum import Enum
from typing import Union


class BaseDimension(Enum):
    mass = 1
    length = 2
    time = 3
    # etc


class Dimensions:

    def __init__(self, d) -> None:
        self._dims = d

    def __mul__(self, other: Dimensions)-> Dimensions:
        result = self._dims.copy()
        for k, v in other._dims.items():
            if k in result:
                result[k] += v
            else:
                result[k] = v
        return Dimensions(result)

    def __truediv__(self, other: Dimensions)-> Dimensions:
        result = self._dims.copy()
        for k, v in other._dims.items():
            if k in result:
                result[k] -= v
            else:
                result[k] = -v
        return Dimensions(result)
    
    def dimension_of(self, base_dimension: BaseDimension)-> Union[float, int]:
        return self._dims.get(base_dimension, 0)
    
    def items(self)->'a set-like object providing a view on dict items':
        return self._dims.items()
    
    
Mass = Dimensions({BaseDimension.mass:1})
Length = Dimensions({BaseDimension.length:1})
Time = Dimensions({BaseDimension.time:1})