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


def test_max_dim_len():
    max_len = ansunits.Dimensions.max_dim_len()
    assert max_len == 10


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
        e1.__str__()
        == "The `dimensions` argument must contain 10 values or less, currently there are 200."
    )
    e2 = ansunits.DimensionsError.INCORRECT_DIMENSIONS()
    assert (
        e2.__str__()
        == f"The `dimensions` must only contain values from {ansunits._dimension_order}"
    )
