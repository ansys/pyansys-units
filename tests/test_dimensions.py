import pytest

import ansys.units as ansunits
from ansys.units.dimensions import IncorrectDimensions


def test_dimensions_init():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions={})
    assert {k: v for k, v in d1} == {}

    d2 = ansunits.Dimensions(dimensions={dims.MASS: 1.0, dims.LENGTH: -2.0})
    assert {k: v for k, v in d2} == {dims.MASS: 1.0, dims.LENGTH: -2.0}

    d3 = ansunits.Dimensions(
        dimensions={
            dims.MASS: 1.0,
            dims.LENGTH: -1.0,
            dims.TIME: -2.0,
        }
    )
    assert {k: v for k, v in d3} == {dims.MASS: 1.0, dims.LENGTH: -1.0, dims.TIME: -2.0}


def test_copy():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions={dims.MASS: 1.0, dims.LENGTH: -2.0})
    d2 = ansunits.Dimensions(copy_from=d1)
    d3 = ansunits.Dimensions(
        dimensions={dims.LENGTH: -1.0, dims.TIME: -2.0}, copy_from=d1
    )

    assert d1 == d2
    assert {k: v for k, v in d3} == {dims.MASS: 1.0, dims.LENGTH: -1.0, dims.TIME: -2.0}


def test_to_string():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions={dims.CURRENT: 1})
    assert str(d1) == "{'CURRENT': 1}"
    assert str(d1) == repr(d1)

    d2 = ansunits.Dimensions()
    assert repr(d2) == ""
    assert str(d2) == repr(d2)


def test_mul():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions={dims.CURRENT: 1})
    d2 = ansunits.Dimensions(dimensions={dims.LENGTH: 1, dims.TIME: -3})
    d3 = d1 * d2
    d4 = d2 * d2
    assert {k: v for k, v in d3} == {dims.LENGTH: 1, dims.TIME: -3, dims.CURRENT: 1}
    assert {k: v for k, v in d4} == {dims.LENGTH: 2, dims.TIME: -6}


def test_truediv():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions={dims.CURRENT: 1})
    d2 = ansunits.Dimensions(dimensions={dims.MASS: 1, dims.CURRENT: 1})

    d3 = d1 / d2
    assert {k: v for k, v in d3} == {dims.MASS: -1}


def test_pow():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions={dims.MASS: 1, dims.CURRENT: 2})
    d2 = d1**-2
    assert {k: v for k, v in d2} == {dims.MASS: -2, dims.CURRENT: -4}


def test_eq():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions={dims.LENGTH: 1, dims.TIME: -3})
    d2 = ansunits.Dimensions(dimensions={dims.LENGTH: 1, dims.TIME: -3})
    assert d1 == d2
    d1 = ansunits.Dimensions(dimensions={dims.LENGTH: 1, dims.TEMPERATURE: 1})
    d2 = ansunits.Dimensions(
        dimensions={dims.LENGTH: 1, dims.TEMPERATURE_DIFFERENCE: 1}
    )

    assert (d1 == d2) == False


def test_ne():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions={dims.LENGTH: 1, dims.TIME: -3})
    d2 = ansunits.Dimensions(dimensions={dims.MASS: 1, dims.CURRENT: -3})
    assert d1 != d2


def test_dimensional():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions={dims.LENGTH: 1, dims.TIME: -3})
    d2 = ansunits.Dimensions()

    assert bool(d1) is True
    assert bool(d2) is False


def test_errors():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions={dims.LENGTH: 2})
    d2 = ansunits.Dimensions(dimensions={dims.MASS: 1, dims.CURRENT: 1})

    with pytest.raises(IncorrectDimensions) as e_info:
        d3 = ansunits.Dimensions(dimensions={dims.MASS: 1, 11: 1})


def test_error_messages():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions={dims.LENGTH: 2})
    e1 = IncorrectDimensions()
    assert str(e1) == f"The `dimensions` key must be a 'BaseDimensions' object"
