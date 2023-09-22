import pytest

import ansys.units as ansunits


def test_dimensions():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions_container={})
    assert d1.dimensions == {}

    d2 = ansunits.Dimensions(dimensions_container={dims.mass: 1.0, dims.length: -2.0})
    assert d2.dimensions == {0: 1.0, 1: -2.0}

    d3 = ansunits.Dimensions(
        dimensions_container={
            dims.mass: 1.0,
            dims.length: -1.0,
            dims.time: -2.0,
        }
    )
    assert d3.dimensions == {0: 1.0, 1: -1.0, 2: -2.0}


def test_str_():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions_container={dims.current: 1})
    assert str(d1) == "{'current': 1}"

    d2 = ansunits.Dimensions()
    assert str(d2) == ""


def test_add():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions_container={dims.current: 1})
    d2 = ansunits.Dimensions(dimensions_container={dims.length: 1, dims.time: -3})
    d3 = d1 + d2
    d4 = d2 + d2
    assert d3.dimensions == {1: 1.0, 2: -3.0, 8: 1.0}
    assert d4.dimensions == {1: 2.0, 2: -6.0}


def test_sub():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions_container={dims.current: 1})
    d2 = ansunits.Dimensions(dimensions_container={dims.mass: 1, dims.current: 1})

    d3 = d1 - d2
    assert d3.dimensions == {0: -1}


def test_mul():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions_container={dims.mass: 1, dims.current: 2})
    d2 = d1 * -2
    assert d2.dimensions == {0: -2, 8: -4}


def test_eq():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions_container={dims.length: 1, dims.time: -3})
    d2 = ansunits.Dimensions(dimensions_container={dims.length: 1, dims.time: -3})
    assert d1 == d2
    d1 = ansunits.Dimensions(dimensions_container={dims.length: 1, dims.temperature: 1})
    d2 = ansunits.Dimensions(
        dimensions_container={dims.length: 1, dims.temperature_difference: 1}
    )

    assert d1 == d2


def test_ne():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions_container={dims.length: 1, dims.time: -3})
    d2 = ansunits.Dimensions(dimensions_container={dims.mass: 1, dims.current: -3})
    assert d1 != d2


def test_errors():
    dims = ansunits.BaseDimensions
    with pytest.raises(ansunits.DimensionsError) as e_info:
        d1 = ansunits.Dimensions(dimensions_container={dims.mass: 1, 11: 1})


def test_error_messages():
    e1 = ansunits.DimensionsError.INCORRECT_DIMENSIONS()
    assert (
        str(e1) == f"The `dimensions_container` key must be a 'BaseDimensions' object"
    )
