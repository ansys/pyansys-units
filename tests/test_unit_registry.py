import os
import tempfile

import pytest

from ansys.units import Unit, UnitRegistry, _base_units
from ansys.units.unit_registry import UnitAlreadyRegistered


def test_default_units():
    ur = UnitRegistry()
    kg = ur.kg
    assert kg.name == "kg"
    assert kg._type == "MASS"
    assert kg.si_scaling_factor == 1
    assert kg.si_offset == 0
    N = ur.N
    assert N.name == "N"
    assert N._composition == "kg m s^-2"
    assert N.si_scaling_factor == 1
    inch = ur.inch
    assert inch.name == "inch"
    assert inch._type == "LENGTH"
    assert inch.si_scaling_factor == 0.0254
    assert inch.si_offset == 0


def test_custom_yaml():
    cwd = os.getcwd()
    custom_file = b"""
base_units:
  kg:
    type: Mass
    factor: 1
    offset: 0
  g:
    type: Mass
    factor: 0.001
    offset: 0
derived_units:
  N:
    composition: kg m s^-2
    factor: 1
  Pa:
    _composition: N m^-2
    factor: 1
"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".yaml", dir=cwd) as fp:
        fp.write(custom_file)
    ur = UnitRegistry(config=fp.name)
    os.remove(fp.name)
    if os.path.exists(fp.name):
        print(f"File: {fp.name} was not deleted")
        assert 0
    with pytest.raises(AttributeError) as e:
        ur.ft
    assert str(e.value) == "'UnitRegistry' object has no attribute 'ft'"
    assert ur.kg.name == "kg"
    assert ur.N._composition == "kg m s^-2"
    assert ur.Pa._factor == 1
    assert str(ur) == "kg, g, N, Pa, "


def test_additional_units():
    kg = _base_units["kg"]
    ur = UnitRegistry(config=None, other={"kg": kg})
    default_ur = UnitRegistry()
    assert str(ur) == "kg, "
    assert ur.kg == default_ur.kg


def test_immutability():
    ur = UnitRegistry()
    with pytest.raises(UnitAlreadyRegistered):
        ur.m = Unit("ft")


def test_error_message():
    e1 = UnitAlreadyRegistered("kg")
    expected_str = "Unable to override `kg` it has already been registered."
    assert str(e1) == expected_str
