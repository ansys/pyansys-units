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

from ansys.units import BaseDimensions, Quantity, Unit, UnitSystem
from ansys.units.preferred_units import (
    PreferredUnitAlreadyRegistered,
    PreferredUnits,
    UnconfiguredPreferredUnit,
)
from ansys.units.variable_descriptor import VariableCatalog

# ---------------------------------------------------------------------------
# PreferredUnits is a conversion policy, independent of UnitSystem. These
# tests exercise it directly and via Quantity.convert()/Unit.convert().
# ---------------------------------------------------------------------------


def _mm_tonne_second_system():
    dims = BaseDimensions
    return UnitSystem(
        base_units={
            dims.MASS: "tonne",
            dims.LENGTH: "mm",
            dims.TIME: "s",
        }
    )


def test_convert_without_preferred_units_keeps_expanded_unit():
    us = _mm_tonne_second_system()
    youngs_modulus = Quantity(210e9, "Pa").convert(us)
    assert youngs_modulus.units.name == "tonne mm^-1 s^-2"


def test_convert_prefers_mpa_for_pressure():
    us = _mm_tonne_second_system()
    youngs_modulus = Quantity(210e9, "Pa").convert(us, preferred_units=["MPa"])

    assert youngs_modulus.units.name == "MPa"
    assert youngs_modulus.value == pytest.approx(210000.0)

    pressure_unit = Unit(
        dimensions=Quantity(1, "Pa").units.dimensions,
        system=us,
        preferred_units=["MPa"],
    )
    assert pressure_unit.name == "MPa"


def test_convert_prefers_newton_for_force():
    us = _mm_tonne_second_system()
    force = Quantity(5000, "N").convert(us, preferred_units=["N"])

    assert force.units.name == "N"
    assert force.value == pytest.approx(5000.0)


def test_convert_combines_preferred_derived_units():
    us = _mm_tonne_second_system()
    prefs = PreferredUnits(["MPa", "N"])

    youngs_modulus = Quantity(210e9, "Pa").convert(us, preferred_units=prefs)
    force = Quantity(5000, "N").convert(us, preferred_units=prefs)

    assert youngs_modulus.units.name == "MPa"
    assert youngs_modulus.value == pytest.approx(210000.0)
    assert force.units.name == "N"
    assert force.value == pytest.approx(5000.0)


def test_convert_accepts_single_preferred_unit_string():
    us = _mm_tonne_second_system()
    youngs_modulus = Quantity(210e9, "Pa").convert(us, preferred_units="MPa")

    assert youngs_modulus.units.name == "MPa"
    assert youngs_modulus.value == pytest.approx(210000.0)


def test_convert_accepts_single_preferred_unit_object():
    us = _mm_tonne_second_system()
    youngs_modulus = Quantity(210e9, "Pa").convert(us, preferred_units=Unit("MPa"))

    assert youngs_modulus.units.name == "MPa"
    assert youngs_modulus.value == pytest.approx(210000.0)


def test_preferred_unit_only_applies_to_matching_dimensions():
    us = _mm_tonne_second_system()
    length = Quantity(0.05, "m").convert(us, preferred_units=["MPa"])

    assert length.units.name == "mm"
    assert length.value == pytest.approx(50.0)


def test_preferred_unit_with_no_matching_quantity_has_no_effect():
    us = _mm_tonne_second_system()
    prefs = PreferredUnits(["MPa"])

    length = Quantity(0.05, "m").convert(us, preferred_units=prefs)

    assert length.units.name == "mm"
    assert length.value == pytest.approx(50.0)


def test_same_system_gives_different_output_for_different_preferred_units():
    # Substitutability fix: the same UnitSystem now yields different output
    # depending on the PreferredUnits passed to convert(), instead of baking a
    # single, fixed presentation choice into the system itself.
    us = _mm_tonne_second_system()
    q = Quantity(210e9, "Pa")

    expanded = q.convert(us)
    simplified = q.convert(us, preferred_units=["MPa"])

    assert expanded.units.name == "tonne mm^-1 s^-2"
    assert simplified.units.name == "MPa"


def test_rejects_conflicting_preferred_units():
    with pytest.raises(PreferredUnitAlreadyRegistered):
        PreferredUnits(["Pa", "MPa"])


def test_rejects_unconfigured_preferred_unit():
    with pytest.raises(UnconfiguredPreferredUnit):
        PreferredUnits(["not-a-unit"])


def test_conflicting_construction_leaves_no_partial_state():
    # Construction is atomic: a failed PreferredUnits(...) call must not leave
    # behind any partial state that could leak into another instance.
    with pytest.raises(PreferredUnitAlreadyRegistered):
        PreferredUnits(["Pa", "MPa", "N"])

    # An independent, valid PreferredUnits still works normally afterwards.
    prefs = PreferredUnits(["N"])
    assert prefs.unit_for(Quantity(1, "N").units.dimensions) == "N"


def test_with_units_returns_independent_new_object():
    base = PreferredUnits(["MPa"])
    combined = base.with_units(["N"])

    assert base is not combined
    assert base.unit_for(Quantity(1, "N").units.dimensions) is None
    assert combined.unit_for(Quantity(1, "Pa").units.dimensions) == "MPa"
    assert combined.unit_for(Quantity(1, "N").units.dimensions) == "N"


def test_with_units_detects_new_conflicts():
    base = PreferredUnits(["MPa"])
    with pytest.raises(PreferredUnitAlreadyRegistered):
        base.with_units(["Pa"])


def test_equality_and_hash():
    assert PreferredUnits(["MPa", "N"]) == PreferredUnits(["N", "MPa"])
    assert hash(PreferredUnits(["MPa", "N"])) == hash(PreferredUnits(["N", "MPa"]))
    assert PreferredUnits(["MPa"]) != PreferredUnits(["kPa"])
    assert PreferredUnits() == PreferredUnits()


# ---------------------------------------------------------------------------
# Dimension-only matching cannot distinguish quantities that share dimensions
# but are conceptually different. This is a documented, inherent limitation
# of a bare (non-descriptor) PreferredUnits entry: torque and energy both
# have dimensions M L^2 T^-2, and stress and energy density both have
# dimensions M L^-1 T^-2, so a dimension-only preferred unit is applied to
# both alike. See the "Quantity-type-aware matching" tests below for how a
# `(VariableDescriptor, unit)` entry resolves this when `quantity_type` is
# supplied to convert().
# ---------------------------------------------------------------------------


def test_dimension_only_preferred_unit_labels_torque_and_energy_the_same():
    prefs = PreferredUnits(["J"])

    torque = Quantity(50, "N m").convert(UnitSystem(), preferred_units=prefs)
    energy = Quantity(50, "J").convert(UnitSystem(), preferred_units=prefs)

    assert torque.units.name == "J"
    assert energy.units.name == "J"


def test_dimension_only_preferred_unit_labels_stress_and_energy_density_the_same():
    prefs = PreferredUnits(["MPa"])

    stress = Quantity(210e9, "Pa").convert(UnitSystem(), preferred_units=prefs)
    energy_density = Quantity(210e9, "J m^-3").convert(
        UnitSystem(), preferred_units=prefs
    )

    assert stress.units.name == "MPa"
    assert energy_density.units.name == "MPa"


# ---------------------------------------------------------------------------
# Quantity-type-aware matching: dimensions alone cannot distinguish torque
# from energy (both M L^2 T^-2), or stress from energy density (both
# M L^-1 T^-2). `(VariableDescriptor, unit)` entries resolve this, but only
# when the caller tells convert() which quantity type it is converting.
# ---------------------------------------------------------------------------


def test_quantity_type_disambiguates_torque_from_energy():
    VariableCatalog.add(
        "TORQUE_TEST",
        VariableCatalog.ENERGY.dimension,
        subcategory="preferred_units_test",
    )
    prefs = PreferredUnits(
        [
            (VariableCatalog.preferred_units_test.TORQUE_TEST, "N m"),
            (VariableCatalog.ENERGY, "J"),
        ]
    )

    work = Quantity(1000, "J")

    as_torque = work.convert(
        UnitSystem(),
        preferred_units=prefs,
        quantity_type=VariableCatalog.preferred_units_test.TORQUE_TEST,
    )
    as_energy = work.convert(
        UnitSystem(), preferred_units=prefs, quantity_type=VariableCatalog.ENERGY
    )

    assert as_torque.units.name == "N m"
    assert as_energy.units.name == "J"


def test_quantity_type_disambiguates_stress_from_energy_density():
    # Both have dimensions M L^-1 T^-2.
    prefs = PreferredUnits(
        [
            (VariableCatalog.ENERGY_DENSITY, "J m^-3"),
            "MPa",
        ]
    )

    stress = Quantity(210e9, "Pa")

    as_energy_density = stress.convert(
        UnitSystem(),
        preferred_units=prefs,
        quantity_type=VariableCatalog.ENERGY_DENSITY,
    )
    as_generic_pressure = stress.convert(UnitSystem(), preferred_units=prefs)

    assert as_energy_density.units.name == "J m^-3"
    assert as_generic_pressure.units.name == "MPa"


def test_quantity_type_entry_does_not_conflict_with_dimension_entry():
    # A descriptor-keyed entry for one specific quantity type does not
    # conflict with a bare, dimension-keyed entry sharing the same
    # dimensions - that is the intended way to override the generic default
    # for a single quantity type.
    prefs = PreferredUnits(
        [
            "MPa",
            (VariableCatalog.ENERGY_DENSITY, "J m^-3"),
        ]
    )

    assert prefs.unit_for(Quantity(1, "Pa").units.dimensions) == "MPa"
    assert (
        prefs.unit_for(
            Quantity(1, "Pa").units.dimensions,
            quantity_type=VariableCatalog.ENERGY_DENSITY,
        )
        == "J m^-3"
    )


def test_quantity_type_without_quantity_type_falls_back_to_dimension_match():
    prefs = PreferredUnits([(VariableCatalog.ENERGY, "kJ")])

    work = Quantity(1000, "J")
    result = work.convert(UnitSystem(), preferred_units=prefs)

    # No quantity_type was given, so the descriptor-only entry does not apply
    # and the quantity falls back to the expanded base-unit expression.
    assert result.units.name == "kg m^2 s^-2"


def test_conflicting_quantity_type_entries_raise():
    with pytest.raises(PreferredUnitAlreadyRegistered):
        PreferredUnits(
            [
                (VariableCatalog.ENERGY, "J"),
                (VariableCatalog.ENERGY, "kJ"),
            ]
        )
