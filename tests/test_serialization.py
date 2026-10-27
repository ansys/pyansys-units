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
"""Tests for dict, JSON (via pydantic), string and pickle serialization."""

import copy
import json
import math
import pickle

import numpy as np
import pytest

from ansys.units import (
    Quantity,
    Unit,
    UnitRegistry,
    get_application_registry,
    set_application_registry,
)
from ansys.units.serialization import (
    ConflictingUnitDefinition,
    UnresolvableUnit,
    resolve_unit,
)


@pytest.fixture(autouse=True)
def _reset_application_registry():
    yield
    set_application_registry(None)


@pytest.fixture
def micron_registry():
    registry = UnitRegistry()
    registry.register_unit(unit="micron", composition="m", factor=1e-6)
    return registry


def _assert_same(restored: Quantity, original: Quantity) -> None:
    assert restored.units == original.units
    assert restored.units.name == original.units.name
    assert np.array_equal(restored.value, original.value, equal_nan=True)
    assert restored.extra_fields == original.extra_fields


QUANTITIES = [
    Quantity(5, "m s^-1"),
    Quantity(-1.5e-7, "kg m^-3"),
    Quantity(20.0, "C"),
    Quantity(-300.0, "C"),  # stored as delta_C
    Quantity(3.0, ""),
    Quantity(90.0, "degree"),
    Quantity([1.0, 2.0, 3.0], "Pa"),
    Quantity([[1.0, float("nan")], [float("inf"), -4.0]], "W m^-1 K^-1"),
    Quantity([], "m"),
    Quantity(2.0, "N", source="sensor", calibrated=True),
]


# ---------------------------------------------------------------------------
# Dictionaries
# ---------------------------------------------------------------------------


def test_to_dict_uses_builtin_types():
    assert Quantity(5, "m s^-1").to_dict() == {"value": 5.0, "units": "m s^-1"}
    data = Quantity([[1, 2], [3, 4]], "kg", source="test").to_dict()
    assert data == {"value": [[1, 2], [3, 4]], "units": "kg", "source": "test"}
    assert type(data["value"][0][0]) is int
    assert Unit("kg m^-3").to_dict() == {"units": "kg m^-3"}


@pytest.mark.parametrize("quantity", QUANTITIES, ids=str)
def test_dict_round_trip(quantity):
    _assert_same(Quantity.from_dict(quantity.to_dict()), quantity)


def test_unit_dict_round_trip():
    for name in ("kg m^-3", "C", "delta_F", "", "kelvin"):
        assert Unit.from_dict(Unit(name).to_dict()) == Unit(name)


def test_from_dict_validates_input():
    with pytest.raises(TypeError):
        Quantity.from_dict([1.0, "m"])
    with pytest.raises(ValueError, match="value"):
        Quantity.from_dict({"units": "m"})
    with pytest.raises(TypeError):
        Quantity.from_dict({"value": 1.0, "units": 5})
    with pytest.raises(TypeError):
        Quantity.from_dict({"value": "1.0", "units": "m"})
    with pytest.raises(ValueError):
        Quantity.from_dict({"value": 1.0, "units": "not_a_unit"})
    # Missing units means dimensionless.
    assert Quantity.from_dict({"value": 2.0}).is_dimensionless


def test_reserved_extra_field_names_are_rejected():
    quantity = Quantity(1.0, "m", unit_definition="oops")
    with pytest.raises(ValueError, match="reserved"):
        quantity.to_dict()


# ---------------------------------------------------------------------------
# Custom units, registries and the application registry
# ---------------------------------------------------------------------------


def test_custom_unit_is_stored_with_its_definition(micron_registry):
    data = micron_registry.Quantity(3.0, "micron").to_dict()
    assert data == {
        "value": 3.0,
        "units": "micron",
        "unit_definition": {"composition": "m", "factor": 1e-6},
    }


def test_custom_unit_restored_without_registry(micron_registry):
    original = micron_registry.Quantity(3.0, "micron")
    restored = Quantity.from_dict(original.to_dict())
    assert restored.units.name == "micron"
    assert restored.units == micron_registry.micron
    assert restored.to("m").value == pytest.approx(3e-6)


def test_custom_unit_resolved_from_registry(micron_registry):
    restored = Quantity.from_dict(
        {"value": 3.0, "units": "micron"}, registry=micron_registry
    )
    assert restored.units == micron_registry.micron

    set_application_registry(micron_registry)
    assert get_application_registry() is micron_registry
    assert Quantity.from_dict({"value": 3.0, "units": "micron"}).units.name == "micron"
    assert Quantity.from_string("3.0 micron").to("m").value == pytest.approx(3e-6)


def test_unknown_unit_without_definition_is_unresolvable():
    with pytest.raises(UnresolvableUnit, match="set_application_registry"):
        Quantity.from_dict({"value": 3.0, "units": "micron"})
    with pytest.raises(UnresolvableUnit):
        resolve_unit("micron")


def test_conflicting_definition_is_rejected(micron_registry):
    other = UnitRegistry()
    other.register_unit(unit="micron", composition="m", factor=2e-6)
    data = micron_registry.Quantity(3.0, "micron").to_dict()
    with pytest.raises(ConflictingUnitDefinition):
        Quantity.from_dict(data, registry=other)


@pytest.mark.parametrize(
    "definition, error",
    [
        ("m", TypeError),
        ({"composition": 1, "factor": 1.0}, TypeError),
        ({"composition": "m", "factor": "1"}, ValueError),
        ({"composition": "m", "factor": True}, ValueError),
        ({"composition": "m", "factor": 0}, ValueError),
        ({"composition": "m", "factor": math.inf}, ValueError),
        ({"composition": "not_a_unit", "factor": 1.0}, ValueError),
    ],
)
def test_invalid_unit_definitions_are_rejected(definition, error):
    with pytest.raises(error):
        Quantity.from_dict(
            {"value": 1.0, "units": "custom", "unit_definition": definition}
        )


def test_set_application_registry_validates_type():
    with pytest.raises(TypeError):
        set_application_registry("not a registry")


# ---------------------------------------------------------------------------
# JSON (through pydantic, or json + to_dict without pydantic)
# ---------------------------------------------------------------------------


@pytest.fixture
def quantity_adapter():
    pydantic = pytest.importorskip("pydantic")
    # Keep NaN and infinity, which pydantic writes as null by default.
    return pydantic.TypeAdapter(
        Quantity, config=pydantic.ConfigDict(ser_json_inf_nan="constants")
    )


@pytest.mark.parametrize("quantity", QUANTITIES, ids=str)
def test_pydantic_json_round_trip(quantity, quantity_adapter):
    text = quantity_adapter.dump_json(quantity)
    _assert_same(quantity_adapter.validate_json(text), quantity)


@pytest.mark.parametrize("quantity", QUANTITIES, ids=str)
def test_json_round_trip_without_pydantic(quantity):
    text = json.dumps(quantity.to_dict())
    _assert_same(Quantity.from_dict(json.loads(text)), quantity)


def test_pydantic_default_json_mode_nan_gives_clear_error():
    pydantic = pytest.importorskip("pydantic")
    adapter = pydantic.TypeAdapter(Quantity)
    text = adapter.dump_json(Quantity([1.0, float("nan")], "m"))
    assert b"null" in text
    with pytest.raises(pydantic.ValidationError, match="ser_json_inf_nan"):
        adapter.validate_json(text)
    with pytest.raises(ValueError, match="ser_json_inf_nan"):
        Quantity.from_dict({"value": [[1.0], [None]], "units": "m"})
    with pytest.raises(ValueError, match="ser_json_inf_nan"):
        Quantity.from_dict({"value": None, "units": "m"})


def test_pydantic_model_with_nested_quantities(micron_registry):
    pydantic = pytest.importorskip("pydantic")

    class Measurement(pydantic.BaseModel):
        length: Quantity
        samples: list[Quantity]
        size: Quantity

    model = Measurement(
        length=Quantity(2.0, "m"),
        samples=[Quantity([1.0, 2.0], "s"), {"value": 3.0, "units": "kg"}],
        size=micron_registry.Quantity(4.0, "micron"),
    )
    restored = Measurement.model_validate_json(model.model_dump_json())
    assert restored.length == Quantity(2.0, "m")
    assert restored.samples[0].value.tolist() == [1.0, 2.0]
    assert restored.samples[1] == Quantity(3.0, "kg")
    assert restored.size.units == micron_registry.micron

    with pytest.raises(pydantic.ValidationError):
        Measurement.model_validate(
            {"length": "2 m", "samples": [], "size": {"value": 1, "units": "m"}}
        )
    with pytest.raises(pydantic.ValidationError):
        Measurement.model_validate(
            {
                "length": {"value": "2", "units": "m"},
                "samples": [],
                "size": {"value": 1, "units": "m"},
            }
        )


# ---------------------------------------------------------------------------
# Strings
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("quantity", QUANTITIES[:-1], ids=str)
def test_string_round_trip(quantity):
    restored = Quantity.from_string(str(quantity))
    assert restored.units == quantity.units
    assert np.array_equal(restored.value, quantity.value, equal_nan=True)


@pytest.mark.parametrize(
    "text, value, units",
    [
        ("5 m", 5.0, "m"),
        ("  -2.5e-3   kg m^-3 ", -2.5e-3, "kg m^-3"),
        ("4", 4.0, ""),
        ("[1, 2, 3] s", [1.0, 2.0, 3.0], "s"),
        ("[[1 2]\n [3 4]] Pa", [[1.0, 2.0], [3.0, 4.0]], "Pa"),
    ],
)
def test_from_string_formats(text, value, units):
    restored = Quantity.from_string(text)
    assert restored.units == Unit(units)
    assert np.array_equal(restored.value, value)


@pytest.mark.parametrize(
    "text, error",
    [
        (5, TypeError),
        ("", ValueError),
        ("five m", ValueError),
        ("[1, 2 m", ValueError),
        ("[1, 2]] m", ValueError),
        ("[1 x] m", ValueError),
        ("[1 ... 9] m", ValueError),
        ("[1] [2] m", ValueError),
        ("5 not_a_unit", ValueError),
    ],
)
def test_from_string_errors(text, error):
    with pytest.raises(error):
        Quantity.from_string(text)


def test_from_string_rejects_summarized_arrays():
    large = Quantity(np.arange(2000.0), "m")
    with pytest.raises(ValueError, match="summarized"):
        Quantity.from_string(str(large))


# ---------------------------------------------------------------------------
# Pickle and copies
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("quantity", QUANTITIES, ids=str)
def test_pickle_round_trip(quantity):
    _assert_same(pickle.loads(pickle.dumps(quantity)), quantity)


def test_units_are_pickled_by_name():
    assert Unit("kg m^-3").__getstate__() == {"units": "kg m^-3"}


def test_pickle_custom_units(micron_registry):
    original = micron_registry.Quantity(3.0, "micron")
    # Without a registry, the stored definition is used.
    restored = pickle.loads(pickle.dumps(original))
    assert restored.units.name == "micron"
    assert restored.to("m").value == pytest.approx(3e-6)

    # With an application registry, the unit is resolved by name.
    set_application_registry(micron_registry)
    assert pickle.loads(pickle.dumps(original)).units == micron_registry.micron

    registry = pickle.loads(pickle.dumps(micron_registry))
    assert registry.micron == micron_registry.micron


def test_unpickling_legacy_unit_state():
    legacy = Unit.__new__(Unit)
    legacy.__setstate__(dict(Unit("kg").__dict__))
    assert legacy == Unit("kg")
    assert legacy.name == "kg"


def test_copies_do_not_depend_on_registries(micron_registry):
    unit = micron_registry.micron
    for duplicate in (copy.copy(unit), copy.deepcopy(unit)):
        assert duplicate is not unit
        assert duplicate.name == "micron"
        assert duplicate == unit

    quantity = micron_registry.Quantity(np.array([1.0, 2.0]), "micron")
    duplicate = copy.deepcopy(quantity)
    assert duplicate.value is not quantity.value
    assert duplicate.units == quantity.units


# ---------------------------------------------------------------------------
# Pydantic
# ---------------------------------------------------------------------------


def test_pydantic_uses_dict_format(micron_registry):
    pydantic = pytest.importorskip("pydantic")

    class Model(pydantic.BaseModel):
        quantity: Quantity

    model = Model(quantity=micron_registry.Quantity([1.0, 2.0], "micron"))
    dumped = model.model_dump()
    assert dumped["quantity"] == {
        "value": [1.0, 2.0],
        "units": "micron",
        "unit_definition": {"composition": "m", "factor": 1e-6},
    }
    restored = Model.model_validate_json(model.model_dump_json())
    assert restored.quantity.units == micron_registry.micron
    assert restored.quantity.value.tolist() == [1.0, 2.0]
