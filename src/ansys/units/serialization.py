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
"""
Serialization of ``Unit`` and ``Quantity`` objects.

Supported formats:

* Plain dictionaries: :meth:`Quantity.to_dict` and :meth:`Quantity.from_dict`
  (and the ``Unit`` equivalents). This is also the format used by the pydantic
  integration, which provides JSON support (``model_dump_json``,
  ``TypeAdapter(Quantity).dump_json``). Without pydantic, use
  ``json.dumps(quantity.to_dict())`` and
  ``Quantity.from_dict(json.loads(text))``.
* Strings: :meth:`Quantity.from_string` parses the output of ``str(quantity)``.
* Pickle: units are pickled by name and resolved again when unpickled.

Units are always stored by name. When loading, a name is resolved against an
explicitly given :class:`~ansys.units.UnitRegistry`, then against the
*application registry* (see :func:`set_application_registry`), and finally
against the built-in units. Custom units that are only known to a registry are
stored together with their definition so that they can be restored even when
no registry defines them.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import math
from typing import Any, cast

from ansys.units.quantity import Quantity
from ansys.units.unit import Unit
from ansys.units.unit_registry import UnitRegistry

_RESERVED_KEYS = frozenset({"value", "units", "unit_definition"})

_application_registry: UnitRegistry | None = None


def _check_type(value: object, expected: type, message: str) -> None:
    """Raise a ``TypeError`` for input, such as loaded data, of the wrong type."""
    if not isinstance(value, expected):
        raise TypeError(message)


# ---------------------------------------------------------------------------
# Application registry
# ---------------------------------------------------------------------------


def set_application_registry(registry: UnitRegistry | None) -> None:
    """
    Set the registry used to resolve unit names when loading serialized data.

    The application registry is used by unpickling and by any loading function
    called without an explicit ``registry``. This
    allows custom units registered with
    :meth:`~ansys.units.UnitRegistry.register_unit` to be restored by name.

    Parameters
    ----------
    registry : UnitRegistry or None
        Registry to use, or ``None`` to use only the built-in units.

    Examples
    --------
    >>> import pickle
    >>> from ansys.units import UnitRegistry, set_application_registry
    >>> ur = UnitRegistry()
    >>> micron = ur.register_unit(unit="micron", composition="m", factor=1e-6)
    >>> set_application_registry(ur)
    >>> q = pickle.loads(pickle.dumps(ur.Quantity(3, "micron")))
    >>> q.units == ur.micron
    True
    """
    if registry is not None:
        _check_type(
            registry,
            UnitRegistry,
            "`registry` must be a UnitRegistry instance or None.",
        )
    global _application_registry
    _application_registry = registry


def get_application_registry() -> UnitRegistry | None:
    """Return the registry set with :func:`set_application_registry`, if any."""
    return _application_registry


# ---------------------------------------------------------------------------
# Units
# ---------------------------------------------------------------------------


def unit_to_dict(unit: Unit) -> dict[str, Any]:
    """
    Serialize a unit to a dictionary.

    See :meth:`Unit.to_dict`.
    """
    data: dict[str, Any] = {"units": unit.name}
    if not _resolvable_by_name(unit):
        data["unit_definition"] = {
            "composition": unit.si_units,
            "factor": unit.si_scaling_factor,
        }
    return data


def unit_from_dict(
    data: Mapping[str, Any], registry: UnitRegistry | None = None
) -> Unit:
    """
    Create a unit from a dictionary.

    See :meth:`Unit.from_dict`.
    """
    _check_type(data, Mapping, f"Expected a mapping, got {type(data).__name__}.")
    name = data.get("units", "")
    if not isinstance(name, str):
        raise TypeError("`units` must be a string.")
    return resolve_unit(name, data.get("unit_definition"), registry)


def resolve_unit(
    name: str,
    definition: Mapping[str, Any] | None = None,
    registry: UnitRegistry | None = None,
) -> Unit:
    """
    Resolve a unit name for deserialization.

    Parameters
    ----------
    name : str
        Unit name.
    definition : dict, optional
        Definition with ``composition`` (SI unit string) and ``factor`` (SI
        scaling factor), used when the name cannot be resolved otherwise.
    registry : UnitRegistry, optional
        Registry to resolve the name against. Defaults to the application
        registry.

    Returns
    -------
    Unit
        The resolved unit.

    Raises
    ------
    UnresolvableUnit
        If the name cannot be resolved and no definition is given.
    ConflictingUnitDefinition
        If the resolved unit does not match the given definition.
    """
    registry = registry if registry is not None else _application_registry
    unit: Unit | None = None
    if registry is not None:
        try:
            unit = registry.get_unit(name)
        except AttributeError:
            unit = None
    if unit is None:
        try:
            unit = Unit(name)
        except (ValueError, TypeError, KeyError) as error:
            if definition is None:
                raise UnresolvableUnit(name) from error
            return _unit_from_definition(name, definition)

    if definition is not None:
        expected = _unit_from_definition(name, definition)
        if not _same_definition(unit, expected):
            raise ConflictingUnitDefinition(name)
    return unit


def _resolvable_by_name(unit: Unit) -> bool:
    """True if the unit is rebuilt exactly from its name without a registry."""
    try:
        return _same_definition(Unit(unit.name), unit)
    except (ValueError, TypeError, KeyError):
        return False


def _same_definition(first: Unit, second: Unit) -> bool:
    return (
        first.dimensions == second.dimensions
        and first.si_offset == second.si_offset
        and math.isclose(first.si_scaling_factor, second.si_scaling_factor)
    )


def _unit_from_definition(name: str, definition: Mapping[str, Any]) -> Unit:
    _check_type(definition, Mapping, "`unit_definition` must be a mapping.")
    composition = definition.get("composition", "")
    factor = definition.get("factor")
    if not isinstance(composition, str):
        raise TypeError("`unit_definition.composition` must be a string.")
    if (
        isinstance(factor, bool)
        or not isinstance(factor, (int, float))
        or not math.isfinite(factor)
        or factor <= 0
    ):
        raise ValueError("`unit_definition.factor` must be a positive finite number.")
    unit = Unit(copy_from=Unit(composition))
    unit._si_scaling_factor = float(factor)
    unit._name = name
    return unit


# ---------------------------------------------------------------------------
# Quantities
# ---------------------------------------------------------------------------


def quantity_to_dict(quantity: Quantity) -> dict[str, Any]:
    """
    Serialize a quantity to a dictionary.

    See :meth:`Quantity.to_dict`.
    """
    reserved = _RESERVED_KEYS.intersection(quantity.extra_fields)
    if reserved:
        raise ValueError(
            f"Extra fields {sorted(reserved)} use reserved serialization keys."
        )
    value = quantity.value
    tolist = getattr(value, "tolist", None)
    plain: Any = tolist() if tolist is not None else value
    return {"value": plain, **unit_to_dict(quantity.units), **quantity.extra_fields}


def quantity_from_dict(
    data: Mapping[str, Any], registry: UnitRegistry | None = None
) -> Quantity:
    """
    Create a quantity from a dictionary.

    See :meth:`Quantity.from_dict`.
    """
    _check_type(data, Mapping, f"Expected a mapping, got {type(data).__name__}.")
    if "value" not in data:
        raise ValueError("A serialized quantity requires a `value` key.")
    if _contains_none(data["value"]):
        raise ValueError(
            "A serialized quantity value contains null. NaN and infinity are written "
            + "as null by pydantic's default JSON mode; set "
            + "`ser_json_inf_nan='constants'` in the model config to preserve them."
        )
    unit = unit_from_dict(data, registry)
    extra_fields = {key: val for key, val in data.items() if key not in _RESERVED_KEYS}
    return Quantity(data["value"], unit, **extra_fields)


def _contains_none(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, (list, tuple)):
        items = cast("Sequence[Any]", value)
        return any(_contains_none(item) for item in items)
    return False


def quantity_from_string(text: str, registry: UnitRegistry | None = None) -> Quantity:
    """
    Parse the output of ``str(quantity)``.

    See :meth:`Quantity.from_string`.
    """
    _check_type(text, str, f"Expected a string, got {type(text).__name__}.")
    text = text.strip()
    if not text:
        raise ValueError("Cannot parse a quantity from an empty string.")
    if text.startswith("["):
        end = text.rfind("]")
        if end < 0:
            raise ValueError(f"Unbalanced brackets in {text!r}.")
        value: Any = _parse_array(text[: end + 1])
        name = text[end + 1 :].strip()
    else:
        number, _, name = text.partition(" ")
        try:
            value = float(number)
        except ValueError:
            raise ValueError(f"Cannot parse a number from {number!r}.") from None
        name = name.strip()
    return Quantity(value, resolve_unit(name, None, registry))


def _parse_array(text: str) -> list[Any]:
    """Parse nested, bracketed numbers as printed by NumPy or Python lists."""
    if "..." in text:
        raise ValueError(
            "Cannot parse a summarized array. Use to_dict for large arrays."
        )
    parts = text.replace("[", " [ ").replace("]", " ] ").replace(",", " ").split()
    stack: list[list[Any]] = []
    result: list[Any] | None = None
    for part in parts:
        if result is not None:
            raise ValueError(f"Unexpected content after array in {text!r}.")
        if part == "[":
            stack.append([])
        elif part == "]":
            # The text starts with "[", so the stack is never empty here.
            items = stack.pop()
            if stack:
                stack[-1].append(items)
            else:
                result = items
        else:
            try:
                stack[-1].append(float(part))
            except ValueError:
                raise ValueError(f"Cannot parse a number from {part!r}.") from None
    if result is None:
        raise ValueError(f"Unbalanced brackets in {text!r}.")
    return result


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class UnresolvableUnit(ValueError):
    """Raised when a serialized unit name cannot be resolved."""

    def __init__(self, name: str):
        super().__init__(
            f"Unit `{name}` cannot be resolved. Pass the UnitRegistry that defines "
            + "it, or set it with `set_application_registry`."
        )


class ConflictingUnitDefinition(ValueError):
    """Raised when a serialized unit definition differs from the registry's unit."""

    def __init__(self, name: str):
        super().__init__(
            f"The serialized definition of `{name}` does not match the unit with "
            + "the same name in the registry."
        )
