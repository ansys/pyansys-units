import pytest

import ansys.units as ansunits


def test_dimensions():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions_container={})
    assert d1.dimensions == {}

    d2 = ansunits.Dimensions(dimensions_container={dims.MASS: 1.0, dims.LENGTH: -2.0})
    assert d2.dimensions == {dims.MASS: 1.0, dims.LENGTH: -2.0}

    d3 = ansunits.Dimensions(
        dimensions_container={
            dims.MASS: 1.0,
            dims.LENGTH: -1.0,
            dims.TIME: -2.0,
        }
    )
    assert d3.dimensions == {dims.MASS: 1.0, dims.LENGTH: -1.0, dims.TIME: -2.0}


def test_copy():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions_container={dims.MASS: 1.0, dims.LENGTH: -2.0})
    d2 = ansunits.Dimensions(copy_from=d1)
    d3 = ansunits.Dimensions(
        dimensions_container={dims.LENGTH: -1.0, dims.TIME: -2.0}, copy_from=d1
    )

    assert d1 == d2
    assert d3.dimensions == {dims.MASS: 1.0, dims.LENGTH: -1.0, dims.TIME: -2.0}


def test_str_():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions_container={dims.CURRENT: 1})
    assert str(d1) == "{'CURRENT': 1}"
    assert repr(d1) == "{'CURRENT': 1}"

    d2 = ansunits.Dimensions()
    assert str(d2) == ""
    assert repr(d2) == ""


def test_mul():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions_container={dims.CURRENT: 1})
    d2 = ansunits.Dimensions(dimensions_container={dims.LENGTH: 1, dims.TIME: -3})
    d3 = d1 * d2
    d4 = d2 * d2
    assert d3.dimensions == {dims.LENGTH: 1, dims.TIME: -3, dims.CURRENT: 1}
    assert d4.dimensions == {dims.LENGTH: 2, dims.TIME: -6}


def test_truediv():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions_container={dims.CURRENT: 1})
    d2 = ansunits.Dimensions(dimensions_container={dims.MASS: 1, dims.CURRENT: 1})

    d3 = d1 / d2
    assert d3.dimensions == {dims.MASS: -1}


def test_pow():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions_container={dims.MASS: 1, dims.CURRENT: 2})
    d2 = d1**-2
    assert d2.dimensions == {dims.MASS: -2, dims.CURRENT: -4}


def test_eq():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions_container={dims.LENGTH: 1, dims.TIME: -3})
    d2 = ansunits.Dimensions(dimensions_container={dims.LENGTH: 1, dims.TIME: -3})
    assert d1 == d2
    d1 = ansunits.Dimensions(dimensions_container={dims.LENGTH: 1, dims.TEMPERATURE: 1})
    d2 = ansunits.Dimensions(
        dimensions_container={dims.LENGTH: 1, dims.TEMPERATURE_DIFFERENCE: 1}
    )

    assert d1 != d2


def test_ne():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions_container={dims.LENGTH: 1, dims.TIME: -3})
    d2 = ansunits.Dimensions(dimensions_container={dims.MASS: 1, dims.CURRENT: -3})
    assert d1 != d2


def test_base_dimensions():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions_container={dims.LENGTH: 2})
    d2 = ansunits.Dimensions(dimensions_container={dims.MASS: 1, dims.CURRENT: 1})


def test_errors():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions_container={dims.LENGTH: 2})
    d2 = ansunits.Dimensions(dimensions_container={dims.MASS: 1, dims.CURRENT: 1})

    with pytest.raises(ansunits.DimensionsError) as e_info:
        d3 = ansunits.Dimensions(dimensions_container={dims.MASS: 1, 11: 1})


def test_error_messages():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions_container={dims.LENGTH: 2})
    e1 = ansunits.DimensionsError.INCORRECT_DIMENSIONS()
    assert (
        str(e1) == f"The `dimensions_container` key must be a 'BaseDimensions' object"
    )
