# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
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
import os

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


def test_pyunits_angles_have_angle_dimensions():
    os.environ["PYANSYS_UNITS_ANGLE_AS_DIMENSION"] = "1"
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


def test_pyunits_angle_and_dimensionless_are_not_convertible():
    os.environ["PYANSYS_UNITS_ANGLE_AS_DIMENSION"] = "1"
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


def test_ansunits_frequency_and_angular_frequency_are_not_convertible():
    os.environ["PYANSYS_UNITS_ANGLE_AS_DIMENSION"] = "1"
    from ansys.units.quantity import IncompatibleDimensions, Quantity

    # ansunits avoids the pint complications by simply not allowing
    # those conversions
    hz = Quantity(1.0, "Hz")
    with pytest.raises(IncompatibleDimensions):
        hz.to("radian s^-1")
    rad_per_s = Quantity(1.0, "radian s^-1")
    with pytest.raises(IncompatibleDimensions):
        rad_per_s.to("Hz")
