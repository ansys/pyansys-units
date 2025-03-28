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

import math

import pytest
import util

# pint and PyUnits disagree about whether angles are dimensionless.
# Yes, angles are dimensionless, and this is pint's point of view.
# PyUnits follows CFX by saying that angle is a dimension, or it's
# convenient to treat it as a dimension. It adds a constraints that
# avoid some tricky business, as shown later.


@pytest.mark.developer_only
def test_pint_angles_are_dimensionless():
    from pint import UnitRegistry

    ur = UnitRegistry()
    angle = 1 * ur.deg
    angle_dimensions = angle.dimensionality
    assert str(angle_dimensions) == "dimensionless"
    angle_in_radians = angle.to(ur.rad)
    angle_in_radians_dimensions = angle_in_radians.dimensionality
    assert str(angle_in_radians_dimensions) == "dimensionless"


def test_pyunits_angles_have_angle_dimensions(monkeypatch):
    monkeypatch.setenv("PYANSYS_UNITS_ANGLE_AS_DIMENSION", "1")
    from ansys.units import BaseDimensions, Dimensions
    from ansys.units.quantity import Quantity

    radian = Quantity(1.0, "radian")
    assert radian.dimensions == Dimensions({BaseDimensions.ANGLE: 1})
    degree = Quantity(1.0, "degree")
    assert degree.dimensions == Dimensions({BaseDimensions.ANGLE: 1})


# pint is happy to convert between angle and dimensionless because it
# sees them as equivalent. PyUnits naturally doesn't allow it.


@pytest.mark.developer_only
def test_pint_angle_and_dimensionless_are_convertible():
    from pint import UnitRegistry

    ur = UnitRegistry()
    angle_rad = 1.0 * ur.rad
    num_rad = float(angle_rad)
    # 1 radian == 1 dimensionless unit, otherwise e.g., trigonometry gets screwed up
    assert num_rad == 1.0
    angle_deg = 1.0 * ur.deg
    num_deg = float(angle_deg)
    # 1 radian == 1 dimensionless unit, so
    # this 1 degree is a fraction of 1 dimensionless unit
    # according to the ratio between degrees and radian
    assert num_deg == util.one_degree_in_radians
    angle_deg_from_rad = angle_deg.to(ur.rad)
    num_deg_rom_rad = float(angle_deg_from_rad)
    assert num_deg_rom_rad == util.one_degree_in_radians


def test_pyunits_angle_and_dimensionless_are_not_convertible(monkeypatch):
    monkeypatch.setenv("PYANSYS_UNITS_ANGLE_AS_DIMENSION", "1")
    from ansys.units.quantity import IncompatibleDimensions, Quantity

    no_dim = Quantity(1.0, "")
    with pytest.raises(IncompatibleDimensions):
        no_dim.to("radian")
    radian = Quantity(1.0, "radian")
    with pytest.raises(IncompatibleDimensions):
        # seems generally meaningless, but OK, this is something
        # that could happen in a generic loop:
        radian.to("")


# because of the way that pint treats angles, we get seamless integration
# with mathematical functions


@pytest.mark.developer_only
def test_pint_angle_works_with_trigonometry():
    from pint import UnitRegistry

    ur = UnitRegistry()
    half_pi_rads = 0.5 * math.pi * ur.rad
    sixty_degrees = 60.0 * ur.deg
    assert math.sin(float(half_pi_rads)) == pytest.approx(1.0)
    assert math.cos(float(sixty_degrees)) == pytest.approx(0.5)


def test_pyunits_angle_works_with_trigonometry():
    from ansys.units.quantity import Quantity, get_si_value

    half_pi_rads = Quantity(0.5 * math.pi, "radian")
    sixty_degrees = Quantity(60.0, "degree")
    assert math.sin(get_si_value(half_pi_rads)) == pytest.approx(1.0)
    # see that PyUnits goes to radians for the float conversion, which is nice
    assert math.cos(get_si_value(sixty_degrees)) == pytest.approx(0.5)


@pytest.mark.developer_only
def test_pint_conversion_between_Hz_and_rps_and_radians_per_second():
    from pint import UnitRegistry
    from util import assert_rightly_but_fail, assert_wrongly
    from util.pint import pint_value

    ur = UnitRegistry()
    hz = 1 * ur.hertz
    rps = hz.to(ur.rps)
    hz_out = rps.to(ur.hertz)
    assert hz == hz_out
    # google "conversion from revolutions per second to hertz";
    # every site unanimously tells you that 1 rps = 1 Hz.
    # But see https://github.com/hgrecco/pint/pull/653 where rps is
    # revolutions per second in pint as the above PR and related
    # issue convey. See e.g., https://github.com/hgrecco/pint/pull/653#issue-342008864
    # which states "Correct behaviour is 1 rpm = 60 rps = 2 * pi * 60 Hz."
    # I don't even get where they're coming from here. 1 Hz is one cycle
    # per second, so that's 1 rps. This doesn't even seem to be ambiguous.
    # This is a tricky area but they've landed on a solution that's not even
    # arguable. But this is actually just collateral damage arising from a deeper issue.
    # See further on in the same test where rad/s is covered.
    assert_wrongly(
        pint_value(hz) == 2.0 * math.pi * pint_value(rps), "2 pi factor for Hz and rps"
    )
    # but it should be
    assert_rightly_but_fail(
        pint_value(hz) == pint_value(rps), "Hertz and rps equivalence"
    )
    radians_per_second = hz.to(ur.radian / ur.s)
    assert_rightly_but_fail(
        2.0 * math.pi * pint_value(hz) == pytest.approx(radians_per_second.magnitude),
        "2 pi factor for Hz and rad/s",
    )
    assert_wrongly(
        pint_value(hz) == pytest.approx(radians_per_second.magnitude),
        "equivalence of Hz and rad/s",
    )
    # The problem is: one radian is asserted to be unity
    #  for conversion between angles and dimensionless values.
    # So the code has to stick to the idea that one radian
    #  is unity. So, when we talk about an "inverse second",
    # or equivalently one hertz then the unit rotation in that
    #  second is one radian, and s^-1 and Hz convert directly
    # to rad/s without any numerical shift. But there is no context
    #  where this is correct. Hz is a unit of frequency, measuring
    # cycles per second, not radians per second.
    # And so, when pint maintainers write things like "Correct behaviour
    #  is 1 rpm = 60 rps = 2 * pi * 60 Hz", what they really
    # mean is "This is the inevitable outcome of the way we do things."


def test_ansunits_frequency_and_angular_frequency_are_not_convertible(monkeypatch):
    monkeypatch.setenv("PYANSYS_UNITS_ANGLE_AS_DIMENSION", "1")
    from ansys.units.quantity import IncompatibleDimensions, Quantity

    # ansunits avoids the pint complications by simply not allowing
    # those conversions
    hz = Quantity(1.0, "Hz")
    with pytest.raises(IncompatibleDimensions):
        hz.to("radian s^-1")
    rad_per_s = Quantity(1.0, "radian s^-1")
    with pytest.raises(IncompatibleDimensions):
        rad_per_s.to("Hz")


def test_degree_addition():
    import ansys.units as pyunits

    degree = pyunits.Quantity(1.0, "degree")
    assert not degree.dimensions
    assert degree.is_dimensionless
    assert degree + 1 == pyunits.Quantity(58.29577951308232, "degree")

    assert pyunits.Quantity(0, "degree") + 3 == pyunits.Quantity(
        171.88733853924697, "degree"
    )
    assert 3 + pyunits.Quantity(0, "degree") == pyunits.Quantity(3, "")


def test_degree_subtraction():
    import ansys.units as pyunits

    degree = pyunits.Quantity(120, "degree")
    assert not degree.dimensions
    assert degree.is_dimensionless
    assert degree - 1 == pyunits.Quantity(62.70422048691768, "degree")


def test_degree_division():
    import ansys.units as pyunits

    degree = pyunits.Quantity(120, "degree")
    assert not degree.dimensions
    assert degree.is_dimensionless
    assert degree / 2 == pyunits.Quantity(60, "degree")


def test_degree_multiplication():
    import ansys.units as pyunits

    degree = pyunits.Quantity(10, "degree")
    assert not degree.dimensions
    assert degree.is_dimensionless
    assert degree * 2 == pyunits.Quantity(20.0, "degree")


def test_degree_power():
    import ansys.units as pyunits

    degree = pyunits.Quantity(10, "degree")
    assert not degree.dimensions
    assert degree.is_dimensionless
    assert degree**2 == pyunits.Quantity(100, "degree^2")


def test_radian_addition():
    import ansys.units as pyunits

    radian = pyunits.Quantity(1.0, "radian")
    assert not radian.dimensions
    assert radian.is_dimensionless
    assert radian + 1 == pyunits.Quantity(2.0, "radian")
    assert (radian + 1).to("degree") == pyunits.Quantity(114.59155902616465, "degree")

    assert pyunits.Quantity(0, "radian") + 3 == pyunits.Quantity(3.0, "radian")
    assert 3 + pyunits.Quantity(0, "radian") == pyunits.Quantity(3.0, "")


def test_radian_subtraction():
    import ansys.units as pyunits

    radian = pyunits.Quantity(2.0, "radian")
    assert not radian.dimensions
    assert radian.is_dimensionless
    assert radian - 1 == pyunits.Quantity(1.0, "radian")
    assert (radian - 1).to("degree") == pyunits.Quantity(57.29577951308232, "degree")


def test_radian_division():
    import ansys.units as pyunits

    radian = pyunits.Quantity(2.0, "radian")
    assert not radian.dimensions
    assert radian.is_dimensionless
    assert radian / 2 == pyunits.Quantity(1.0, "radian")
    assert (radian / 2).to("degree") == pyunits.Quantity(57.29577951308232, "degree")


def test_radian_multiplication():
    import ansys.units as pyunits

    radian = pyunits.Quantity(2.0, "radian")
    assert not radian.dimensions
    assert radian.is_dimensionless
    assert radian * 2 == pyunits.Quantity(4.0, "radian")
    assert (radian * 2).to("degree") == pyunits.Quantity(229.1831180523293, "degree")


def test_radian_power():
    import ansys.units as pyunits

    radian = pyunits.Quantity(2.0, "radian")
    assert not radian.dimensions
    assert radian.is_dimensionless
    assert radian**2 == pyunits.Quantity(4.0, "radian^2")
    assert (radian**2).to("degree^2") == pyunits.Quantity(
        13131.225400046977, "degree^2"
    )
