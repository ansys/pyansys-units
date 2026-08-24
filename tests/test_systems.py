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

from ansys.units import BaseDimensions, Quantity, Unit, UnitRegistry, UnitSystem
from ansys.units.systems import (
    IncompleteUnitSystem,
    IncorrectUnitType,
    InvalidUnitSystem,
    NotBaseUnit,
    UnitSystemAlreadyRegistered,
)


def test_pre_defined_unit_system():
    us = UnitSystem(system="SI")
    assert us.MASS == "kg"
    assert us.LENGTH == "m"
    assert us.TIME == "s"
    assert us.TEMPERATURE == "K"
    assert us.TEMPERATURE_DIFFERENCE == "delta_K"
    assert us.ANGLE == "radian"
    assert us.CHEMICAL_AMOUNT == "mol"
    assert us.LIGHT == "cd"
    assert us.CURRENT == "A"
    assert us.SOLID_ANGLE == "sr"


def test_repr():
    us = UnitSystem()
    us_dict = """MASS: kg
LENGTH: m
TIME: s
TEMPERATURE: K
TEMPERATURE_DIFFERENCE: delta_K
ANGLE: radian
CHEMICAL_AMOUNT: mol
LIGHT: cd
CURRENT: A
SOLID_ANGLE: sr
"""

    assert repr(us) == str(us_dict)


def test_copy():
    us = UnitSystem(system="BT")
    us1 = UnitSystem(copy_from=us)
    assert us1 == us


def test_update():
    ureg = UnitRegistry()
    dims = BaseDimensions
    us = UnitSystem(system="SI")
    base_units = {
        dims.MASS: ureg.slug,
        dims.LENGTH: ureg.ft,
        dims.TIME: "s",
        dims.TEMPERATURE: "R",
        dims.TEMPERATURE_DIFFERENCE: "delta_R",
        dims.ANGLE: "degree",
        dims.CHEMICAL_AMOUNT: ureg.slugmol,
        dims.LIGHT: "cd",
        dims.CURRENT: "A",
        dims.SOLID_ANGLE: "sr",
    }
    us.update(base_units=base_units)
    assert us.MASS.name == "slug"  # pyright: ignore[reportAttributeAccessIssue]
    assert us.LENGTH.name == "ft"  # pyright: ignore[reportAttributeAccessIssue]
    assert us.TIME == "s"
    assert us.TEMPERATURE == "R"
    assert us.TEMPERATURE_DIFFERENCE == "delta_R"
    assert us.ANGLE == "degree"
    assert (
        us.CHEMICAL_AMOUNT.name  # pyright: ignore[reportAttributeAccessIssue]
        == "slugmol"
    )
    assert us.LIGHT == "cd"
    assert us.CURRENT == "A"
    assert us.SOLID_ANGLE == "sr"


def test_eq():
    us1 = UnitSystem(system="BT")
    us2 = UnitSystem()
    us3 = UnitSystem(system="SI")
    assert us1 != us2
    assert us2 == us3


def test_set_type():
    ureg = UnitRegistry()
    us = UnitSystem(system="SI")
    us.MASS = ureg.slug
    us.LENGTH = "ft"
    us.TEMPERATURE = "R"
    us.TEMPERATURE_DIFFERENCE = ureg.delta_R
    us.ANGLE = "degree"
    us.CHEMICAL_AMOUNT = "slugmol"
    assert us.MASS.name == "slug"
    assert us.LENGTH == "ft"
    assert us.TEMPERATURE == "R"
    assert us.TEMPERATURE_DIFFERENCE.name == "delta_R"
    assert us.ANGLE == "degree"
    assert us.CHEMICAL_AMOUNT == "slugmol"


def test_custom_unit_system():
    dims = BaseDimensions
    us = UnitSystem(
        base_units={
            dims.MASS: "slug",
            dims.LENGTH: "ft",
            dims.TIME: "s",
            dims.TEMPERATURE: "R",
            dims.TEMPERATURE_DIFFERENCE: "delta_R",
            dims.ANGLE: "radian",
            dims.CHEMICAL_AMOUNT: "slugmol",
            dims.LIGHT: "cd",
            dims.CURRENT: "A",
            dims.SOLID_ANGLE: "sr",
        }
    )
    assert us.MASS == "slug"
    assert us.LENGTH == "ft"
    assert us.TIME == "s"
    assert us.TEMPERATURE == "R"
    assert us.TEMPERATURE_DIFFERENCE == "delta_R"
    assert us.ANGLE == "radian"
    assert us.CHEMICAL_AMOUNT == "slugmol"
    assert us.LIGHT == "cd"
    assert us.CURRENT == "A"
    assert us.SOLID_ANGLE == "sr"


def test_not_base_unit_init():
    dims = BaseDimensions

    with pytest.raises(NotBaseUnit):
        UnitSystem(base_units={dims.LENGTH: "N"})


def test_not_base_unit_update():
    dims = BaseDimensions
    us = UnitSystem(system="SI")

    with pytest.raises(NotBaseUnit):
        us.update(base_units={dims.MASS: "N"})


def test_invalid_unit_sys():
    with pytest.raises(InvalidUnitSystem):
        UnitSystem(system="Standard")


def test_wrong_unit_type():
    us = UnitSystem()

    with pytest.raises(IncorrectUnitType):
        us.TIME = "m"
    with pytest.raises(IncorrectUnitType):
        us.LIGHT = "sr"
    with pytest.raises(IncorrectUnitType):
        us.CURRENT = "ft"
    with pytest.raises(IncorrectUnitType):
        us.SOLID_ANGLE = "radian"


def test_error_messages():
    e1 = NotBaseUnit("kg s^-1")
    expected_str = (
        "`kg s^-1` is not a base unit. To use `kg s^-1`, add it to the "
        "`base_units` table within the cfg.yaml file."
    )
    assert str(e1) == expected_str

    e2 = InvalidUnitSystem("ham sandwich")
    assert str(e2) == "`ham sandwich` is not a supported unit system."

    e3 = IncorrectUnitType(unit="ft", unit_type=BaseDimensions.MASS)
    assert str(e3) == "The unit `ft` is incompatible with unit system type: `MASS`"


# ---------------------------------------------------------------------------
# Custom unit system support: prefixed base units (e.g. "mm") and
# single-composition derived units (e.g. "tonne") as unit system slots, plus
# named custom unit system registration (e.g. "MMGS").
# ---------------------------------------------------------------------------


def test_custom_unit_system_with_prefixed_length_unit():
    dims = BaseDimensions
    us = UnitSystem(base_units={dims.MASS: "g", dims.LENGTH: "mm"})
    assert us.MASS == "g"
    assert us.LENGTH == "mm"
    # Unspecified slots fall back to the default ("SI") system.
    assert us.TIME == "s"


def test_custom_unit_system_with_derived_mass_unit():
    dims = BaseDimensions
    us = UnitSystem(base_units={dims.MASS: "tonne", dims.LENGTH: "mm"})
    assert us.MASS == "tonne"
    assert us.LENGTH == "mm"


def test_custom_unit_system_rejects_compound_unit_as_pressure_slot():
    dims = BaseDimensions
    with pytest.raises(NotBaseUnit):
        UnitSystem(base_units={dims.LENGTH: "MPa"})
    with pytest.raises(NotBaseUnit):
        UnitSystem(base_units={dims.MASS: "Pa"})


def test_custom_unit_system_rejects_prefixed_unit_of_wrong_type():
    dims = BaseDimensions
    us = UnitSystem()
    with pytest.raises(IncorrectUnitType):
        us.TIME = "mm"
    with pytest.raises(IncorrectUnitType):
        UnitSystem(base_units={dims.TIME: "mm"})


def test_mmgs_material_database_unit_system():
    dims = BaseDimensions
    mmgs = UnitSystem(
        base_units={
            dims.MASS: "g",
            dims.LENGTH: "mm",
            dims.TIME: "s",
        }
    )
    assert mmgs.MASS == "g"
    assert mmgs.LENGTH == "mm"
    assert mmgs.TIME == "s"


def test_mm_tonne_second_system_is_mpa_consistent():
    dims = BaseDimensions
    us = UnitSystem(
        base_units={
            dims.MASS: "tonne",
            dims.LENGTH: "mm",
            dims.TIME: "s",
        }
    )
    pressure_unit = Unit(dimensions=Quantity(1, "Pa").units.dimensions, system=us)
    one_in_system = Quantity(1, pressure_unit)
    assert one_in_system.to("MPa").value == pytest.approx(1.0)


def test_register_system_enables_named_lookup():
    dims = BaseDimensions
    base_units = {
        dims.MASS: "g",
        dims.LENGTH: "mm",
        dims.TIME: "s",
        dims.TEMPERATURE: "K",
        dims.TEMPERATURE_DIFFERENCE: "delta_K",
        dims.ANGLE: "radian",
        dims.CHEMICAL_AMOUNT: "mol",
        dims.LIGHT: "cd",
        dims.CURRENT: "A",
        dims.SOLID_ANGLE: "sr",
    }
    UnitSystem.register_system(name="MMGS_TEST", base_units=base_units)

    us = UnitSystem(system="MMGS_TEST")
    assert us.MASS == "g"
    assert us.LENGTH == "mm"
    assert us.TIME == "s"

    # The registered system behaves like any other predefined system.
    us_copy = UnitSystem(copy_from=us)
    assert us_copy == us


def test_register_system_duplicate_name_raises():
    dims = BaseDimensions
    base_units = {dim: getattr(UnitSystem(system="SI"), dim.name) for dim in dims}
    UnitSystem.register_system(name="DUPLICATE_TEST", base_units=base_units)
    with pytest.raises(UnitSystemAlreadyRegistered):
        UnitSystem.register_system(name="DUPLICATE_TEST", base_units=base_units)


def test_register_system_rejects_builtin_name():
    dims = BaseDimensions
    base_units = {dim: getattr(UnitSystem(system="SI"), dim.name) for dim in dims}
    with pytest.raises(UnitSystemAlreadyRegistered):
        UnitSystem.register_system(name="SI", base_units=base_units)


def test_register_system_incomplete_raises():
    dims = BaseDimensions
    with pytest.raises(IncompleteUnitSystem):
        UnitSystem.register_system(
            name="INCOMPLETE_TEST", base_units={dims.MASS: "g", dims.LENGTH: "mm"}
        )


def test_register_system_rejects_compound_unit():
    dims = BaseDimensions
    base_units = {dim: getattr(UnitSystem(system="SI"), dim.name) for dim in dims}
    base_units[dims.LENGTH] = "MPa"
    with pytest.raises(NotBaseUnit):
        UnitSystem.register_system(name="INVALID_UNIT_TEST", base_units=base_units)


def test_register_system_rejects_wrong_type():
    dims = BaseDimensions
    base_units = {dim: getattr(UnitSystem(system="SI"), dim.name) for dim in dims}
    base_units[dims.TIME] = "mm"
    with pytest.raises(IncorrectUnitType):
        UnitSystem.register_system(name="WRONG_TYPE_TEST", base_units=base_units)


# ---------------------------------------------------------------------------
# Regression safety: predefined systems (SI, CGS, BT) must keep working
# exactly as before, and must not be affected by custom system registration.
# ---------------------------------------------------------------------------


def test_cgs_predefined_unit_system():
    us = UnitSystem(system="CGS")
    assert us.MASS == "g"
    assert us.LENGTH == "cm"
    assert us.TIME == "s"
    assert us.TEMPERATURE == "K"
    assert us.ANGLE == "radian"


def test_bt_predefined_unit_system():
    us = UnitSystem(system="BT")
    assert us.MASS == "slug"
    assert us.LENGTH == "ft"
    assert us.TIME == "s"
    assert us.TEMPERATURE == "R"


def test_custom_base_units_override_non_default_named_system():
    dims = BaseDimensions
    us = UnitSystem(system="CGS", base_units={dims.LENGTH: "mm"})
    assert us.MASS == "g"  # inherited from CGS
    assert us.LENGTH == "mm"  # overridden
    assert us.TIME == "s"  # inherited from CGS


def test_predefined_systems_unaffected_by_custom_registration():
    dims = BaseDimensions
    base_units = {
        dims.MASS: "g",
        dims.LENGTH: "mm",
        dims.TIME: "s",
        dims.TEMPERATURE: "K",
        dims.TEMPERATURE_DIFFERENCE: "delta_K",
        dims.ANGLE: "radian",
        dims.CHEMICAL_AMOUNT: "mol",
        dims.LIGHT: "cd",
        dims.CURRENT: "A",
        dims.SOLID_ANGLE: "sr",
    }
    UnitSystem.register_system(name="ISOLATION_TEST", base_units=base_units)

    assert UnitSystem(system="SI") == UnitSystem(system="SI")
    si = UnitSystem(system="SI")
    assert si.MASS == "kg"
    assert si.LENGTH == "m"
    cgs = UnitSystem(system="CGS")
    assert cgs.MASS == "g"
    assert cgs.LENGTH == "cm"
    bt = UnitSystem(system="BT")
    assert bt.MASS == "slug"
    assert bt.LENGTH == "ft"


def test_custom_named_system_instance_independence():
    dims = BaseDimensions
    base_units = {
        dims.MASS: "g",
        dims.LENGTH: "mm",
        dims.TIME: "s",
        dims.TEMPERATURE: "K",
        dims.TEMPERATURE_DIFFERENCE: "delta_K",
        dims.ANGLE: "radian",
        dims.CHEMICAL_AMOUNT: "mol",
        dims.LIGHT: "cd",
        dims.CURRENT: "A",
        dims.SOLID_ANGLE: "sr",
    }
    UnitSystem.register_system(name="INDEPENDENCE_TEST", base_units=base_units)

    us1 = UnitSystem(system="INDEPENDENCE_TEST")
    us1.LENGTH = "cm"

    us2 = UnitSystem(system="INDEPENDENCE_TEST")
    assert us2.LENGTH == "mm"
    assert us1.LENGTH == "cm"


def test_property_setter_still_rejects_compound_unit():
    us = UnitSystem()
    with pytest.raises(NotBaseUnit):
        us.MASS = "N"


# ---------------------------------------------------------------------------
# Additional robustness for the dimensional-atomicity fallback: aliases,
# atomic derived units beyond "tonne", bad/garbage strings, and multiple
# dimensions exercised with prefixes.
# ---------------------------------------------------------------------------


def test_custom_unit_system_accepts_alias_for_base_unit():
    dims = BaseDimensions
    us = UnitSystem(base_units={dims.TIME: "sec"})
    assert us.TIME == "sec"


def test_custom_unit_system_accepts_atomic_derived_time_unit():
    dims = BaseDimensions
    us = UnitSystem(base_units={dims.TIME: "h"})
    assert us.TIME == "h"


def test_custom_unit_system_accepts_prefixed_units_across_dimensions():
    dims = BaseDimensions
    us = UnitSystem(
        base_units={
            dims.LENGTH: "km",
            dims.TIME: "ms",
            dims.CURRENT: "mA",
        }
    )
    assert us.LENGTH == "km"
    assert us.TIME == "ms"
    assert us.CURRENT == "mA"


def test_custom_unit_system_rejects_garbage_string():
    dims = BaseDimensions
    with pytest.raises(NotBaseUnit):
        UnitSystem(base_units={dims.LENGTH: "totally-not-a-unit"})


def test_custom_unit_system_rejects_unrecognized_prefix_like_string():
    dims = BaseDimensions
    with pytest.raises(NotBaseUnit):
        UnitSystem(base_units={dims.LENGTH: "zz"})


def test_custom_unit_system_rejects_empty_string():
    dims = BaseDimensions
    with pytest.raises(NotBaseUnit):
        UnitSystem(base_units={dims.LENGTH: ""})


# ---------------------------------------------------------------------------
# Custom units (UnitRegistry.register_unit) combined with custom unit
# systems: the original motivating use case for this feature.
# ---------------------------------------------------------------------------


def test_custom_unit_system_accepts_instance_registered_unit_object():
    """A ``Unit`` instance for a custom, instance-scoped unit (not known globally by
    name) is validated using its own precomputed dimensions."""
    dims = BaseDimensions
    ureg = UnitRegistry()
    ureg.register_unit(unit="micron", composition="m", factor=1e-6)

    us = UnitSystem(
        base_units={dims.LENGTH: ureg.micron}  # pyright: ignore[reportArgumentType]
    )
    assert us.LENGTH.name == "micron"  # pyright: ignore[reportAttributeAccessIssue]


def test_custom_unit_system_rejects_instance_registered_unit_of_wrong_type():
    dims = BaseDimensions
    ureg = UnitRegistry()
    ureg.register_unit(unit="micron", composition="m", factor=1e-6)

    with pytest.raises(IncorrectUnitType):
        UnitSystem(
            base_units={dims.MASS: ureg.micron}  # pyright: ignore[reportArgumentType]
        )


def test_register_system_accepts_unit_objects():
    """
    ``register_system`` accepts ``Unit`` instances for globally-known.

    units (it stores their resolved name, so only globally-resolvable units
    -- not instance-scoped custom ones -- survive re-construction later).
    """
    dims = BaseDimensions
    base_units = {
        dims.MASS: Unit("g"),
        dims.LENGTH: Unit("mm"),
        dims.TIME: "s",
        dims.TEMPERATURE: "K",
        dims.TEMPERATURE_DIFFERENCE: "delta_K",
        dims.ANGLE: "radian",
        dims.CHEMICAL_AMOUNT: "mol",
        dims.LIGHT: "cd",
        dims.CURRENT: "A",
        dims.SOLID_ANGLE: "sr",
    }
    UnitSystem.register_system(
        name="UNIT_OBJECT_TEST",
        base_units=base_units,  # pyright: ignore[reportArgumentType]
    )

    us = UnitSystem(system="UNIT_OBJECT_TEST")
    assert us.MASS == "g"
    assert us.LENGTH == "mm"


def test_register_system_cannot_later_resolve_instance_scoped_custom_unit():
    """
    ``register_system`` only persists the resolved unit *name*.

    Since
    instance-scoped custom units (``UnitRegistry.register_unit``) are not
    known globally by name, registration succeeds but reconstructing the
    system later fails, exactly like looking up that name directly would.
    """
    dims = BaseDimensions
    ureg = UnitRegistry()
    ureg.register_unit(unit="hectogram", composition="g", factor=100)

    base_units = {
        dims.MASS: ureg.hectogram,
        dims.LENGTH: "mm",
        dims.TIME: "s",
        dims.TEMPERATURE: "K",
        dims.TEMPERATURE_DIFFERENCE: "delta_K",
        dims.ANGLE: "radian",
        dims.CHEMICAL_AMOUNT: "mol",
        dims.LIGHT: "cd",
        dims.CURRENT: "A",
        dims.SOLID_ANGLE: "sr",
    }
    # Registration itself succeeds: at this point ``ureg.hectogram``'s own
    # dimensions are used to validate it.
    UnitSystem.register_system(
        name="HECTOGRAM_TEST",
        base_units=base_units,  # pyright: ignore[reportArgumentType]
    )

    # But reconstructing the system later only has the bare name "hectogram"
    # to go on, which is not resolvable outside of ``ureg``.
    with pytest.raises(NotBaseUnit):
        UnitSystem(system="HECTOGRAM_TEST")


# ---------------------------------------------------------------------------
# register_system: name handling edge cases.
# ---------------------------------------------------------------------------


def _si_like_base_units():
    dims = BaseDimensions
    return {dim: getattr(UnitSystem(system="SI"), dim.name) for dim in dims}


def test_register_system_strips_name_whitespace():
    UnitSystem.register_system(
        name="  PADDED_NAME_TEST  ", base_units=_si_like_base_units()
    )
    us = UnitSystem(system="PADDED_NAME_TEST")
    assert us.MASS == "kg"


def test_register_system_empty_name_raises():
    with pytest.raises(ValueError):
        UnitSystem.register_system(name="", base_units=_si_like_base_units())
    with pytest.raises(ValueError):
        UnitSystem.register_system(name="   ", base_units=_si_like_base_units())


def test_register_system_names_are_case_sensitive():
    UnitSystem.register_system(
        name="case_sensitive_test", base_units=_si_like_base_units()
    )
    # A differently-cased name is a distinct, unregistered system.
    UnitSystem.register_system(
        name="CASE_SENSITIVE_TEST",
        base_units={**_si_like_base_units(), BaseDimensions.LENGTH: "mm"},
    )
    lower = UnitSystem(system="case_sensitive_test")
    upper = UnitSystem(system="CASE_SENSITIVE_TEST")
    assert lower.LENGTH == "m"
    assert upper.LENGTH == "mm"


# ---------------------------------------------------------------------------
# Quantity conversions through a custom unit system.
# ---------------------------------------------------------------------------


def test_custom_unit_system_velocity_round_trip():
    dims = BaseDimensions
    mmgs = UnitSystem(base_units={dims.MASS: "g", dims.LENGTH: "mm", dims.TIME: "s"})
    velocity_unit = Unit(dimensions=Quantity(1, "m s^-1").units.dimensions, system=mmgs)
    assert velocity_unit.name == "mm s^-1"

    quantity = Quantity(1000, velocity_unit)
    assert quantity.to("m s^-1").value == pytest.approx(1.0)
