# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pytest

from ansys.units import BaseDimensions, Dimensions, QuantityDimensions
from ansys.units.dimensions import IncorrectDimensions


def test_dimensions_init():
    dims = BaseDimensions
    d1 = Dimensions(dimensions={})
    assert {k: v for k, v in d1} == {}

    d2 = Dimensions(dimensions={dims.MASS: 1.0, dims.LENGTH: -2.0})
    assert {k: v for k, v in d2} == {dims.MASS: 1.0, dims.LENGTH: -2.0}

    d3 = Dimensions(
        dimensions={
            dims.MASS: 1.0,
            dims.LENGTH: -1.0,
            dims.TIME: -2.0,
        }
    )
    assert {k: v for k, v in d3} == {dims.MASS: 1.0, dims.LENGTH: -1.0, dims.TIME: -2.0}


def test_copy():
    dims = BaseDimensions
    d1 = Dimensions(dimensions={dims.MASS: 1.0, dims.LENGTH: -2.0})
    d2 = Dimensions(copy_from=d1)
    d3 = Dimensions(dimensions={dims.LENGTH: -1.0, dims.TIME: -2.0}, copy_from=d1)

    assert d1 == d2
    assert {k: v for k, v in d3} == {dims.MASS: 1.0, dims.LENGTH: -1.0, dims.TIME: -2.0}


def test_to_string():
    dims = BaseDimensions
    d1 = Dimensions(dimensions={dims.CURRENT: 1})
    assert str(d1) == "{'CURRENT': 1}"
    assert str(d1) == repr(d1)

    d2 = Dimensions()
    assert repr(d2) == "{}"
    assert str(d2) == repr(d2)


def test_mul():
    dims = BaseDimensions
    d1 = Dimensions(dimensions={dims.CURRENT: 1})
    d2 = Dimensions(dimensions={dims.LENGTH: 1, dims.TIME: -3})
    d3 = d1 * d2
    d4 = d2 * d2
    assert {k: v for k, v in d3} == {dims.LENGTH: 1, dims.TIME: -3, dims.CURRENT: 1}
    assert {k: v for k, v in d4} == {dims.LENGTH: 2, dims.TIME: -6}


def test_truediv():
    dims = BaseDimensions
    d1 = Dimensions(dimensions={dims.CURRENT: 1})
    d2 = Dimensions(dimensions={dims.MASS: 1, dims.CURRENT: 1})

    d3 = d1 / d2
    assert {k: v for k, v in d3} == {dims.MASS: -1}


def test_pow():
    dims = BaseDimensions
    d1 = Dimensions(dimensions={dims.MASS: 1, dims.CURRENT: 2})
    d2 = d1**-2
    assert {k: v for k, v in d2} == {dims.MASS: -2, dims.CURRENT: -4}


def test_eq():
    dims = BaseDimensions
    d1 = Dimensions(dimensions={dims.LENGTH: 1, dims.TIME: -3})
    d2 = Dimensions(dimensions={dims.LENGTH: 1, dims.TIME: -3})
    assert d1 == d2

    d1 = Dimensions(dimensions={dims.LENGTH: 1, dims.TIME: 0})
    d2 = Dimensions(dimensions={dims.LENGTH: 1})
    assert d1 == d2

    d1 = Dimensions(dimensions={dims.LENGTH: 1, dims.TEMPERATURE: 1})
    d2 = Dimensions(dimensions={dims.LENGTH: 1, dims.TEMPERATURE_DIFFERENCE: 1})

    assert d1 != d2

    dims = BaseDimensions
    d1 = Dimensions(dimensions={dims.LENGTH: 1, dims.TIME: -3})
    d2 = Dimensions(dimensions={dims.MASS: 1, dims.CURRENT: -3})
    assert d1 != d2


def test_dimensional():
    dims = BaseDimensions
    d1 = Dimensions(dimensions={dims.LENGTH: 1, dims.TIME: -3})
    d2 = Dimensions()

    assert bool(d1) is True
    assert bool(d2) is False


def test_errors():
    dims = BaseDimensions
    Dimensions(dimensions={dims.LENGTH: 2})
    Dimensions(dimensions={dims.MASS: 1, dims.CURRENT: 1})

    with pytest.raises(IncorrectDimensions):
        Dimensions(
            dimensions={dims.MASS: 1, 11: 1}
        )  # pyright: ignore[reportArgumentType]


def test_error_messages():
    dims = BaseDimensions
    Dimensions(dimensions={dims.LENGTH: 2})
    e1 = IncorrectDimensions()
    assert str(e1) == "The `dimensions` key must be a 'BaseDimensions' object"


def test_quantity_dimensions():
    qd = QuantityDimensions
    base = BaseDimensions
    assert qd.ELECTRICAL_POTENTIAL == qd.CURRENT * qd.ELECTRICAL_RESISTANCE
    assert qd.FORCE == Dimensions(
        dimensions={base.MASS: 1, base.LENGTH: 1, base.TIME: -2}
    )


def test_quantity_dimensions_subscription():
    dims = BaseDimensions
    d2 = Dimensions(dimensions={dims.MASS: 1.0, dims.LENGTH: -1.0})
    assert d2["MASS"] == 1.0
    assert d2["LENGTH"] == -1.0
