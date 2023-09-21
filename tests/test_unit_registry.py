import os
import tempfile

import pytest

import ansys.units as ansunits


def test_default_units():
    ur = ansunits.UnitRegistry()
    kg = ur.kg
    assert kg.name == "kg"
    assert kg.type == "Mass"
    assert kg._factor == 1
    assert kg._offset == 0
    N = ur.N
    assert N.name == "N"
    assert N.type == "Derived"
    assert N._composition == "kg m s^-2"
    assert N._factor == 1


def test_custom_yaml():
    cwd = os.getcwd()
    custom_file = b"""
fundamental_units:
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
    ur = ansunits.UnitRegistry(config=fp.name)
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


def test_default_units():
    ur = ansunits.UnitRegistry(
        config=None, other={"kg": {"type": "Mass", "factor": 1, "offset": 0}}
    )
    assert str(ur) == "kg, "
    assert ur.kg._factor == 1

