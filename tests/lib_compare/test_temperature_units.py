import pytest


def test_pint_raises_exception_for_multiplying_relative_temperature():
    from pint import UnitRegistry
    from pint.errors import OffsetUnitCalculusError

    ur = UnitRegistry()
    with pytest.raises(OffsetUnitCalculusError):
        # this is ambiguous - relative value!
        tc = 150.0 * ur.degC
    # this is well defined
    tk = 50.0 * ur.kelvin


def test_pint_distinguishes_temperature_from_difference():
    from pint import Quantity, UnitRegistry
    from util import assert_wrongly

    ur = UnitRegistry()
    t1 = 150.0 * ur.kelvin
    t2 = 100.0 * ur.kelvin
    td1 = t1 - t2
    assert_wrongly(
        td1 == 50.0 * ur.kelvin, "test_pint_distinguishes_temperature_from_difference"
    )
    t1 = Quantity(1.0, ur.degC)
    t2 = Quantity(2.0, ur.degC)
    t3 = t2 - t1
    assert t3 == 1.0 * ur.delta_degree_Celsius


def test_pyfluent_distinguishes_temperature_from_difference():
    from ansys.units.quantity import Quantity

    t1 = Quantity(150.0, "C")
    assert t1.type == "Temperature"
    t2 = Quantity(100.0, "C")
    assert t2.type == "Temperature"
    td1 = t1 - t2
    assert td1.type == "Temperature Difference"
    t3 = Quantity(1.0, "K")
    t4 = Quantity(2.0, "K")
    td2 = t4 - t3
    assert td2.type == "Temperature Difference"


# These next tests are completely debatable.
# If we start applying this, what can we do for compound units involving temperature?
# It gets too complicated.
# However, -1 K is *only* meaningful as a difference rather than an absolute value
# OTOH if you start asserting that -1 K has to be a temperature difference, you
# can run into a bunch of other issues.
def test_pyfluent_automatically_creates_temperature_difference_from_negative_absolute_value():
    from util import assert_rightly_but_fail, assert_wrongly

    from ansys.units.quantity import Quantity

    t = Quantity(-1.0, "K")
    assert_wrongly(
        t.type == "Temperature",
        "test_pyfluent_automatically_creates_temperature_difference_from_negative_absolute_value",
    )
    assert_rightly_but_fail(
        t.type == "Temperature Difference",
        "test_pyfluent_automatically_creates_temperature_difference_from_negative_absolute_value",
    )


# shortened from test_pyfluent_automatically_creates_temperature_
# difference_from_negative_absolute_value_based_on_relative_value
# to test_pyfluent_temperature_difference_from_negative_absolute_value_to_relative_value
def test_pyfluent_temperature_difference_from_negative_absolute_value_to_relative_value():
    from util import assert_rightly_but_fail, assert_wrongly

    from ansys.units.quantity import Quantity

    t = Quantity(-274.0, "C")
    assert_wrongly(
        t.type == "Temperature",
        "test_pyfluent_temperature_difference_from_negative_absolute_value_to_relative_value",
    )
    assert_rightly_but_fail(
        t.type == "Temperature Difference",
        "test_pyfluent_temperature_difference_from_negative_absolute_value_to_relative_value",
    )


def test_pyfluent_converts_temperature_correctly():
    from ansys.units.quantity import Quantity

    tC = Quantity(1.0, "K").to("C")
    assert tC.value == -272.15
    assert float(tC) == 1.0


# This one is not debatable. This is a pure bug in PyFluent code.
# We will need to do some extra work such that when type is a difference
# then the offset is zero in conversions.
def test_pyfluent_converts_temperature_difference_correctly():
    from util import assert_rightly_but_fail, assert_wrongly

    from ansys.units.quantity import Quantity

    tC = (Quantity(1.0, "K") - Quantity(2.0, "K")).to("C")
    assert_rightly_but_fail(
        tC.value == -1.0, "test_pyfluent_converts_temperature_difference_correctly"
    )
    assert float(tC) == -1.0
    assert_wrongly(
        tC.value == -274.15, "test_pyfluent_converts_temperature_difference_correctly"
    )
    tC = (Quantity(2.0, "K") - Quantity(1.0, "K")).to("C")
    assert_rightly_but_fail(
        tC.value == 1.0, "test_pyfluent_converts_temperature_difference_correctly"
    )
    assert float(tC) == 1.0
    assert_wrongly(
        tC.value == -272.15, "test_pyfluent_converts_temperature_difference_correctly"
    )
