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
        ur.register_unit(unit="J", composition="N m", factor=1)

    # Register alias 'Q' equal to Joule
    ur.register_unit(unit="Q", composition="N m", factor=1)
    assert ur.Q == ur.J

    # Same instance cannot re-register same name
    with pytest.raises(UnitAlreadyRegistered):
        ur.register_unit(unit="Q", composition="N m", factor=1)

    # New registry does not see instance registration
    ur2 = UnitRegistry()
    with pytest.raises(AttributeError):
        _ = ur2.Q

    # Register independently on another instance
    ur2.register_unit(unit="Q", composition="N m", factor=1)
    assert ur2.Q == ur2.J

    # Factor scales SI relative to composition
    ur.register_unit(unit="Z", composition="N m", factor=1000)
    assert ur.Z.dimensions == ur.J.dimensions
    assert ur.Z.si_scaling_factor == pytest.approx(ur.J.si_scaling_factor * 1000)
