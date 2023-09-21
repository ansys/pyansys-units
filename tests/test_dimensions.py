import pytest

import ansys.units as ansunits


def test_dimensions():
    d1 = ansunits.Dimensions(
        dimensions_container=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    )
    assert d1.full_list == [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    d2 = ansunits.Dimensions(dimensions_container=[0, 1.0, -2.0])
    assert d2.full_list == [0.0, 1.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    d3 = ansunits.Dimensions(
        dimensions_container=[1.0, -1.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    )
    assert d3.full_list == [1.0, -1.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


def test_dictionary():
    d1 = ansunits.Dimensions(dimensions_container=[0, 1.0, -2.0])
    assert d1.short_dictionary == {"length": 1.0, "time": -2.0}
    d2 = ansunits.Dimensions(
        dimensions_container=[1.0, 0.0, -2.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0]
    )
    assert d2.short_dictionary == {"mass": 1, "time": -2.0, "light": 1}


def test_short_list():
    d1 = ansunits.Dimensions(dimensions_container=[0, 1.0, -2.0])
    assert d1.short_list == [0, 1.0, -2.0]
    d2 = ansunits.Dimensions(
        dimensions_container=[1.0, 0.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0]
    )
    assert d2.short_list == [1.0, 0.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]


def test_max_dim_len():
    max_len = ansunits.Dimensions.max_dim_len()
    assert max_len == 10


def test_str_():
    d1 = ansunits.Dimensions(
        dimensions_container=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
    )
    assert str(d1) == "[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0]"

    d2 = ansunits.Dimensions(dimensions_container=[0.0, 1.0, -3.0])
    assert str(d2) == "[0.0, 1.0, -3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]"


def test_add():
    d1 = ansunits.Dimensions(
        dimensions_container=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
    )
    d2 = ansunits.Dimensions(dimensions_container=[0.0, 1.0, -3.0])
    d3 = d1 + d2
    assert d3.short_list == [0.0, 1.0, -3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]


def test_sub():
    d1 = ansunits.Dimensions(
        dimensions_container=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
    )
    d2 = ansunits.Dimensions(dimensions_container={"Mass": 1, "Current": 1})
    d3 = d1 - d2
    assert d3.short_dictionary == {"mass": -1}


def test_mul():
    d1 = ansunits.Dimensions(dimensions_container={"Mass": 1, "Current": 2})
    d2 = d1 * -2
    assert d2.full_list == [-2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -4.0, 0.0]


def test_errors():
    with pytest.raises(ansunits.DimensionsError) as e_info:
        d1 = ansunits.Dimensions(
            dimensions_container=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        )
    with pytest.raises(ansunits.DimensionsError) as e_info:
        d2 = ansunits.Dimensions(dimensions_container={"Mass": 1, "Sound": 1})


def test_error_messages():
    e1 = ansunits.DimensionsError.EXCESSIVE_DIMENSIONS(200)
    assert (
        str(e1)
        == "The `dimensions` argument must contain 10 values or less, currently there are 200."
    )
    e2 = ansunits.DimensionsError.INCORRECT_DIMENSIONS()
    assert (
        str(e2)
        == f"The `dimensions` must only contain values from {ansunits._dimension_order}"
    )
