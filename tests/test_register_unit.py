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

import pytest

from ansys.units import UnitRegistry
from ansys.units.unit_registry import UnitNameAlreadyRegistered


def test_register_unit():
    # Backward-compat removal: global registration no longer exists.
    # Ensure that creating a new registry does not reflect any external state.
    ur = UnitRegistry()
    with pytest.raises(AttributeError):
        _ = ur.Q


def test_instance_register_unit():
    # Instance-scoped registration should affect only that registry
    ur = UnitRegistry()

    # Cannot override built-ins
    with pytest.raises(UnitNameAlreadyRegistered):
        ur.register_unit(unit="J", composition="N m", factor=1)

    # Register alias 'Q' equal to Joule using one composition
    ur.register_unit(unit="Q", composition="N m", factor=1)
    assert ur.Q == ur.J

    # Same instance cannot re-register same name
    with pytest.raises(UnitNameAlreadyRegistered):
        ur.register_unit(unit="Q", composition="N m", factor=1)

    # New registry does not see instance registration
    ur2 = UnitRegistry()
    with pytest.raises(AttributeError):
        _ = ur2.Q

    # Register independently on another instance with a different equivalent composition
    ur2.register_unit(unit="Q", composition="W s", factor=1)
    assert ur2.Q == ur2.J
    # Independence: earlier registration on ur remains unchanged
    assert ur.Q == ur.J
    # Objects are distinct across registries
    assert ur.Q is not ur2.Q
    # Equivalent SI scaling for equivalent compositions
    assert ur.Q.si_scaling_factor == pytest.approx(ur2.Q.si_scaling_factor)

    # Factor scales SI relative to composition
    ur.register_unit(unit="Z", composition="N m", factor=1000)
    assert ur.Z.dimensions == ur.J.dimensions
    assert ur.Z.si_scaling_factor == pytest.approx(ur.J.si_scaling_factor * 1000)


def test_instance_register_unit_independence_with_factor():
    # Each registry can define the same symbol with different scale factors
    ur = UnitRegistry()
    ur2 = UnitRegistry()

    ur.register_unit(unit="Q2", composition="N m", factor=1)
    ur2.register_unit(unit="Q2", composition="N m", factor=2)

    # ur.A equals Joule; ur2.A has double SI scaling compared to Joule
    assert ur.Q2 == ur.J
    assert ur2.Q2.si_scaling_factor == pytest.approx(ur2.J.si_scaling_factor * 2)
    # Distinct objects and independent configuration
    assert ur.Q2 is not ur2.Q2


def test_duplicate_registration_same_registry():
    ur = UnitRegistry()

    # First registration succeeds
    ur.register_unit(unit="B", composition="N m", factor=1)
    assert ur.B == ur.J

    # Re-register same name with same composition should fail
    with pytest.raises(UnitNameAlreadyRegistered):
        ur.register_unit(unit="B", composition="N m", factor=1)

    # Re-register same name with different (but equivalent) composition should also fail
    with pytest.raises(UnitNameAlreadyRegistered):
        ur.register_unit(unit="B", composition="W s", factor=1)


def test_name_only_collision_check():
    """
    Test that collision detection is name-only.

    Two units with different names but equivalent definitions (same composition and
    factor) should both be allowed, demonstrating that the check is superficial (name-
    based) rather than semantic (equivalence-based).
    """
    ur = UnitRegistry()

    # Register two different names for equivalent definitions
    ur.register_unit(unit="energy1", composition="N m", factor=1)
    ur.register_unit(
        unit="energy2", composition="N m", factor=1
    )  # Same definition, different name

    # Both should exist
    assert ur.energy1.si_scaling_factor == pytest.approx(ur.energy2.si_scaling_factor)
    assert ur.energy1.dimensions == ur.energy2.dimensions

    # Same definition via different but equivalent composition
    ur.register_unit(unit="energy3", composition="W s", factor=1)
    assert ur.energy3.si_scaling_factor == pytest.approx(ur.energy1.si_scaling_factor)


def test_get_unit_instance_registered():
    """Test get_unit retrieves instance-registered units by name."""
    ur = UnitRegistry()
    ur.register_unit(unit="micron", composition="m", factor=1e-6)

    # String-based lookup should work
    unit = ur.get_unit("micron")
    assert unit.name == "micron"
    assert unit.si_scaling_factor == pytest.approx(1e-6)


def test_get_unit_builtin():
    """Test get_unit falls back to built-in units."""
    ur = UnitRegistry()

    # Built-in unit should be accessible
    unit = ur.get_unit("m")
    assert unit.name == "m"

    unit = ur.get_unit("J")
    assert unit.name == "J"


def test_get_unit_not_found():
    """Test get_unit raises AttributeError for unknown units."""
    ur = UnitRegistry()

    with pytest.raises(AttributeError, match="not found"):
        ur.get_unit("nonexistent_unit")


def test_registry_quantity_with_registered_unit():
    """Test ur.Quantity() allows string-based creation with registered units."""
    ur = UnitRegistry()
    ur.register_unit(unit="micron", composition="m", factor=1e-6)

    # Create quantity using string name
    q = ur.Quantity(1, "micron")
    assert q.value == 1.0
    assert q.units.name == "micron"

    # SI value should be 1e-6
    from ansys.units import get_si_value

    assert get_si_value(q) == pytest.approx(1e-6)


def test_registry_quantity_with_builtin():
    """Test ur.Quantity() works with built-in units."""
    ur = UnitRegistry()

    q = ur.Quantity(5, "m")
    assert q.value == 5.0
    assert q.units.name == "m"


def test_registry_quantity_with_unit_object():
    """Test ur.Quantity() accepts Unit objects directly."""
    ur = UnitRegistry()
    ur.register_unit(unit="micron", composition="m", factor=1e-6)

    q = ur.Quantity(2, ur.micron)
    assert q.value == 2.0
    assert q.units.name == "micron"


def test_registry_quantity_instance_isolation():
    """Test that ur.Quantity uses that registry's units, not global."""
    ur1 = UnitRegistry()
    ur2 = UnitRegistry()

    ur1.register_unit(unit="X", composition="m", factor=10)
    ur2.register_unit(unit="X", composition="m", factor=100)

    q1 = ur1.Quantity(1, "X")
    q2 = ur2.Quantity(1, "X")

    from ansys.units import get_si_value

    assert get_si_value(q1) == pytest.approx(10)
    assert get_si_value(q2) == pytest.approx(100)


# =============================================================================
# Edge cases: Aliasing and indirect equivalence
# =============================================================================


def test_register_unit_does_not_check_aliases():
    """
    Test that register_unit collision check does NOT include global aliases.

    This documents the current behavior: you can register a unit with a name
    that shadows a global alias. The registered unit takes precedence in
    ur.get_unit() and ur.Quantity(), but Unit("alias_name") still resolves
    to the canonical unit via global alias resolution.
    """
    ur = UnitRegistry()

    # "deg" is a built-in alias for "degree"
    # Registering a unit named "deg" is allowed (no collision check against aliases)
    ur.register_unit(unit="deg", composition="m", factor=1.0)

    # The instance-registered unit is accessible
    assert ur.deg.name == "deg"
    assert ur.deg.dimensions == ur.m.dimensions  # It's a length unit now

    # ur.get_unit returns the instance-registered unit
    assert ur.get_unit("deg").name == "deg"
    assert ur.get_unit("deg").dimensions == ur.m.dimensions

    # ur.Quantity uses instance-registered unit
    q = ur.Quantity(1, "deg")
    assert q.units.dimensions == ur.m.dimensions

    # But Unit("deg") still resolves via global alias to "degree" (angle)
    from ansys.units import Unit

    global_deg = Unit("deg")
    assert global_deg.name == "degree"  # Resolved via alias


def test_register_unit_does_not_detect_equivalent_factor():
    """
    Test that collision check is name-only, not factor-based.

    Two units with the same composition and factor but different names can both be
    registered. No semantic equivalence check is performed.
    """
    ur = UnitRegistry()

    # Register two units that are semantically identical (same as Joule)
    ur.register_unit(unit="myjoule", composition="N m", factor=1)
    ur.register_unit(unit="yourjoule", composition="N m", factor=1)

    # Both exist and have the same SI scaling factor
    assert ur.myjoule.si_scaling_factor == pytest.approx(ur.yourjoule.si_scaling_factor)
    assert ur.myjoule.si_scaling_factor == pytest.approx(ur.J.si_scaling_factor)


def test_register_unit_does_not_detect_equivalent_offset():
    """
    Test that collision check doesn't consider SI offset equivalence.

    Note: register_unit only supports factor, not offset. This test confirms
    that even if two units have the same effective SI conversion, they can
    both be registered as long as their names differ.
    """
    ur = UnitRegistry()

    # Register units with different factors - both allowed despite potential overlap
    ur.register_unit(unit="mymeter", composition="m", factor=1)
    ur.register_unit(unit="alsometer", composition="m", factor=1)

    # Both units are functionally identical to "m"
    assert ur.mymeter.si_scaling_factor == pytest.approx(ur.m.si_scaling_factor)
    assert ur.alsometer.si_scaling_factor == pytest.approx(ur.m.si_scaling_factor)


def test_get_unit_does_not_resolve_global_aliases():
    """
    Test that get_unit doesn't resolve global aliases for non-registered units.

    get_unit checks instance-registered units, then falls back to built-in base/derived
    units, but does NOT resolve aliases.
    """
    ur = UnitRegistry()

    # "deg" is a global alias for "degree", but get_unit won't find it
    # because it only checks instance-registered and built-in (base/derived)
    with pytest.raises(AttributeError, match="not found"):
        ur.get_unit("deg")

    # "degree" (the canonical name) is a built-in derived unit
    unit = ur.get_unit("degree")
    assert unit.name == "degree"


def test_register_unit_name_check_is_case_sensitive():
    """
    Test that the name collision check is case-sensitive.

    'M' (mega) and 'm' (meter) are different names.
    """
    ur = UnitRegistry()

    # 'm' is a built-in base unit (meter)
    with pytest.raises(UnitNameAlreadyRegistered):
        ur.register_unit(unit="m", composition="ft", factor=1)

    # 'M' is not a built-in unit name (it's a multiplier prefix), so this succeeds
    # Note: This may or may not be desirable behavior depending on use case
    ur.register_unit(unit="M", composition="m", factor=1e6)
    assert ur.M.si_scaling_factor == pytest.approx(1e6)


def test_equivalent_compositions_same_dimensions():
    """
    Test that equivalent compositions produce units with same dimensions.

    This confirms that while name collision isn't checked semantically, the resulting
    units do have correct dimensions.
    """
    ur = UnitRegistry()

    # N m and W s are equivalent energy units
    ur.register_unit(unit="energy_nm", composition="N m", factor=1)
    ur.register_unit(unit="energy_ws", composition="W s", factor=1)
    ur.register_unit(unit="energy_kgm2s2", composition="kg m^2 s^-2", factor=1)

    # All should have same dimensions as Joule
    assert ur.energy_nm.dimensions == ur.J.dimensions
    assert ur.energy_ws.dimensions == ur.J.dimensions
    assert ur.energy_kgm2s2.dimensions == ur.J.dimensions

    # All should have same SI scaling factor
    assert ur.energy_nm.si_scaling_factor == pytest.approx(ur.J.si_scaling_factor)
    assert ur.energy_ws.si_scaling_factor == pytest.approx(ur.J.si_scaling_factor)
    assert ur.energy_kgm2s2.si_scaling_factor == pytest.approx(ur.J.si_scaling_factor)
