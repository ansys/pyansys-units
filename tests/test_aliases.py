# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
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
"""Tests for unit aliasing support."""

import pytest

from ansys.units import Quantity, Unit, UnitRegistry
from ansys.units._constants import _aliases
from ansys.units.unit_registry import AliasAlreadyRegistered


class TestBuiltinAliases:
    """Tests for aliases defined in cfg.yaml."""

    def test_deg_resolves_to_degree(self):
        u = Unit("deg")
        assert u.name == "degree"

    def test_rad_resolves_to_radian(self):
        u = Unit("rad")
        assert u.name == "radian"

    def test_sec_resolves_to_s(self):
        u = Unit("sec")
        assert u.name == "s"

    def test_meter_resolves_to_m(self):
        u = Unit("meter")
        assert u.name == "m"

    def test_kilogram_resolves_to_kg(self):
        u = Unit("kilogram")
        assert u.name == "kg"

    def test_newton_resolves_to_N(self):
        u = Unit("newton")
        assert u.name == "N"

    def test_foot_resolves_to_ft(self):
        u = Unit("foot")
        assert u.name == "ft"

    def test_hertz_resolves_to_Hz(self):
        u = Unit("hertz")
        assert u.name == "Hz"


class TestAliasInCompoundUnits:
    """Aliases work inside compound unit strings."""

    def test_deg_per_sec(self):
        u = Unit("deg sec^-1")
        assert u.name == "degree s^-1"

    def test_meter_per_sec_squared(self):
        u = Unit("meter sec^-2")
        assert u.name == "m s^-2"

    def test_newton_meter(self):
        u = Unit("newton meter")
        assert u.name == "N m"


class TestAliasWithQuantity:
    """Aliases work when creating Quantity objects."""

    def test_quantity_with_deg(self):
        q = Quantity(90, "deg")
        assert q.value == 90.0
        assert q.units.name == "degree"

    def test_quantity_with_rad(self):
        q = Quantity(3.14, "rad")
        assert q.value == 3.14
        assert q.units.name == "radian"

    def test_quantity_with_meter(self):
        q = Quantity(10, "meter")
        assert q.value == 10.0
        assert q.units.name == "m"


class TestAliasSIProperties:
    """Alias-resolved units have the same SI properties as the canonical unit."""

    def test_deg_si_scaling_factor(self):
        assert Unit("deg").si_scaling_factor == Unit("degree").si_scaling_factor

    def test_deg_si_offset(self):
        assert Unit("deg").si_offset == Unit("degree").si_offset

    def test_deg_dimensions(self):
        assert Unit("deg").dimensions == Unit("degree").dimensions

    def test_rad_si_scaling_factor(self):
        assert Unit("rad").si_scaling_factor == Unit("radian").si_scaling_factor

    def test_sec_si_scaling_factor(self):
        assert Unit("sec").si_scaling_factor == Unit("s").si_scaling_factor

    def test_meter_si_scaling_factor(self):
        assert Unit("meter").si_scaling_factor == Unit("m").si_scaling_factor

    def test_foot_si_scaling_factor(self):
        assert Unit("foot").si_scaling_factor == Unit("ft").si_scaling_factor


class TestAliasEquality:
    """An alias-created Unit equals the canonical Unit."""

    def test_deg_equals_degree(self):
        assert Unit("deg") == Unit("degree")

    def test_rad_equals_radian(self):
        assert Unit("rad") == Unit("radian")

    def test_meter_equals_m(self):
        assert Unit("meter") == Unit("m")


class TestRegisterAlias:
    """Tests for programmatic alias registration via UnitRegistry."""

    def test_register_new_alias(self):
        ureg = UnitRegistry()
        ureg.register_alias("angular_deg", "degree")
        u = Unit("angular_deg")
        assert u.name == "degree"
        # Clean up
        del _aliases["angular_deg"]

    def test_register_alias_for_derived_unit(self):
        ureg = UnitRegistry()
        ureg.register_alias("newton_force", "N")
        u = Unit("newton_force")
        assert u.name == "N"
        del _aliases["newton_force"]

    def test_register_alias_pointing_to_alias(self):
        ureg = UnitRegistry()
        # "deg" is already an alias for "degree"
        ureg.register_alias("angular_degree", "deg")
        u = Unit("angular_degree")
        assert u.name == "degree"
        del _aliases["angular_degree"]

    def test_register_duplicate_alias_raises(self):
        ureg = UnitRegistry()
        with pytest.raises(AliasAlreadyRegistered):
            ureg.register_alias("deg", "degree")

    def test_register_alias_shadowing_base_unit_raises(self):
        ureg = UnitRegistry()
        with pytest.raises(AliasAlreadyRegistered):
            ureg.register_alias("kg", "g")

    def test_register_alias_for_unknown_canonical_raises(self):
        ureg = UnitRegistry()
        with pytest.raises(ValueError, match="not a configured"):
            ureg.register_alias("myunit", "nonexistent")

    def test_register_alias_empty_alias_raises(self):
        ureg = UnitRegistry()
        with pytest.raises(ValueError, match="non-empty"):
            ureg.register_alias("", "degree")

    def test_register_alias_empty_canonical_raises(self):
        ureg = UnitRegistry()
        with pytest.raises(ValueError, match="non-empty"):
            ureg.register_alias("mydeg", "")


class TestConversionWithAlias:
    """Conversions work correctly with aliased units."""

    def test_deg_to_radian_conversion(self):
        q = Quantity(180, "deg")
        q_rad = q.to("radian")
        assert abs(q_rad.value - 3.141592653589793) < 1e-10

    def test_rad_to_degree_conversion(self):
        q = Quantity(3.141592653589793, "rad")
        q_deg = q.to("degree")
        assert abs(q_deg.value - 180.0) < 1e-10

    def test_meter_to_ft_conversion(self):
        q = Quantity(1, "meter")
        q_ft = q.to("ft")
        assert abs(q_ft.value - 3.280839895013123) < 1e-6
