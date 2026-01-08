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

from ansys.units import UnitRegistry, register_unit
from ansys.units.unit_registry import UnitAlreadyRegistered


def test_register_unit(monkeypatch):
    # ensure a clean registry for this test and restore afterwards
    import ansys.units.unit_registry as urmod

    saved = urmod._REGISTERED_UNITS.copy()
    urmod._REGISTERED_UNITS.clear()
    try:
        register_unit(unit="Q", composition="N m", factor=1)
        ur = UnitRegistry()
        assert ur.Q == ur.J

        with pytest.raises(UnitAlreadyRegistered):
            register_unit(unit="Q", composition="N m", factor=1)

        register_unit(unit="Z", composition="N m", factor=1)
        with pytest.raises(AttributeError):
            _ = ur.Z

        ur2 = UnitRegistry()
        assert ur2.Q == ur2.J == ur2.Z
    finally:
        urmod._REGISTERED_UNITS.clear()
        urmod._REGISTERED_UNITS.update(saved)
