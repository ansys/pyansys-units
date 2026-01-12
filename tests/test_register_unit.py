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
from ansys.units.unit_registry import UnitAlreadyRegistered


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
    with pytest.raises(UnitAlreadyRegistered):
        ur.register_unit(name="J", composition="N m", factor=1)

    # Register alias 'Q' equal to Joule using one composition
    ur.register_unit(name="Q", composition="N m", factor=1)
    assert ur.Q == ur.J

    # Same instance cannot re-register same name
    with pytest.raises(UnitAlreadyRegistered):
        ur.register_unit(name="Q", composition="N m", factor=1)

    # New registry does not see instance registration
    ur2 = UnitRegistry()
    with pytest.raises(AttributeError):
        _ = ur2.Q

    # Register independently on another instance with a different equivalent composition
    ur2.register_unit(name="Q", composition="W s", factor=1)
    assert ur2.Q == ur2.J
    # Independence: earlier registration on ur remains unchanged
    assert ur.Q == ur.J
    # Objects are distinct across registries
    assert ur.Q is not ur2.Q
    # Equivalent SI scaling for equivalent compositions
    assert ur.Q.si_scaling_factor == pytest.approx(ur2.Q.si_scaling_factor)

    # Factor scales SI relative to composition
    ur.register_unit(name="Z", composition="N m", factor=1000)
    assert ur.Z.dimensions == ur.J.dimensions
    assert ur.Z.si_scaling_factor == pytest.approx(ur.J.si_scaling_factor * 1000)


def test_instance_register_unit_independence_with_factor():
    # Each registry can define the same symbol with different scale factors
    ur = UnitRegistry()
    ur2 = UnitRegistry()

    ur.register_unit(name="Q2", composition="N m", factor=1)
    ur2.register_unit(name="Q2", composition="N m", factor=2)

    # ur.A equals Joule; ur2.A has double SI scaling compared to Joule
    assert ur.Q2 == ur.J
    assert ur2.Q2.si_scaling_factor == pytest.approx(ur2.J.si_scaling_factor * 2)
    # Distinct objects and independent configuration
    assert ur.Q2 is not ur2.Q2


def test_duplicate_registration_same_registry():
    ur = UnitRegistry()

    # First registration succeeds
    ur.register_unit(name="B", composition="N m", factor=1)
    assert ur.B == ur.J

    # Re-register same name with same composition should fail
    with pytest.raises(UnitAlreadyRegistered):
        ur.register_unit(name="B", composition="N m", factor=1)

    # Re-register same name with different (but equivalent) composition should also fail
    with pytest.raises(UnitAlreadyRegistered):
        ur.register_unit(name="B", composition="W s", factor=1)
