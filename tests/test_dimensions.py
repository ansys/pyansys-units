import pytest

import ansys.units as ansunits


def test_dimensions():
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


def test_to_string():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions={dims.CURRENT: 1})
    assert str(d1) == "{'CURRENT': 1}"
    assert str(d1) == repr(d1)

    d2 = ansunits.Dimensions()
    assert repr(d2) == ""
    assert str(d2) == repr(d2)


def test_add():
    temp = ansunits.Dimensions(dimensions={ansunits.BaseDimensions.TEMPERATURE: 1.0})
    delta_temp = ansunits.Dimensions(
        dimensions={ansunits.BaseDimensions.TEMPERATURE_DIFFERENCE: 1.0}
    )
    not_temp = ansunits.Dimensions(dimensions={ansunits.BaseDimensions.MASS: 1.0})

    assert temp + delta_temp == temp
    assert temp + temp == None
    assert temp + not_temp == None


def test_sub():
    temp = ansunits.Dimensions(dimensions={ansunits.BaseDimensions.TEMPERATURE: 1.0})
    delta_temp = ansunits.Dimensions(
        dimensions={ansunits.BaseDimensions.TEMPERATURE_DIFFERENCE: 1.0}
    )
    not_temp = ansunits.Dimensions(dimensions={ansunits.BaseDimensions.MASS: 1.0})

    assert temp - temp == delta_temp
    assert temp - delta_temp == temp
    assert delta_temp - delta_temp == None
    assert temp - not_temp == None


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

    assert d1 != d2


def test_ne():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions={dims.LENGTH: 1, dims.TIME: -3})
    d2 = ansunits.Dimensions(dimensions={dims.MASS: 1, dims.CURRENT: -3})
    assert d1 != d2


def test_dimensional():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions={dims.LENGTH: 1, dims.TIME: -3})
    d2 = ansunits.Dimensions()

    assert bool(d1) == True
    assert bool(d2) == False


def test_comparison_operations():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions={dims.LENGTH: 1, dims.TIME: -3})
    d2 = ansunits.Dimensions(dimensions={dims.LENGTH: 1})

    assert (d1 > d1) == None
    assert (d1 >= d1) == None
    assert (d1 < d1) == None
    assert (d1 <= d1) == None

    with pytest.raises(ansunits.DimensionsError):
        d1 > d2
    with pytest.raises(ansunits.DimensionsError):
        d1 >= d2
    with pytest.raises(ansunits.DimensionsError):
        d1 < d2
    with pytest.raises(ansunits.DimensionsError):
        d1 <= d2


def test_base_dimensions():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions={dims.LENGTH: 2})
    d2 = ansunits.Dimensions(dimensions={dims.MASS: 1, dims.CURRENT: 1})


def test_errors():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions={dims.LENGTH: 2})
    d2 = ansunits.Dimensions(dimensions={dims.MASS: 1, dims.CURRENT: 1})

    with pytest.raises(ansunits.DimensionsError) as e_info:
        d3 = ansunits.Dimensions(dimensions={dims.MASS: 1, 11: 1})


def test_error_messages():
    dims = ansunits.BaseDimensions
    d1 = ansunits.Dimensions(dimensions={dims.LENGTH: 2})
    e1 = ansunits.DimensionsError.INCORRECT_DIMENSIONS()
    assert str(e1) == f"The `dimensions` key must be a 'BaseDimensions' object"
