# Copyright (C) 2023 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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
# This file is @generated

from typing_extensions import final

from ansys.units.base_dimensions import BaseDimensions as _B
from ansys.units.dimensions import Dimensions
from ansys.units.quantity_dimensions import QuantityDimensions as _D
from ansys.variable_descriptor.variable_descriptor import (
    ScalarVariableDescriptor,
    VariableCatalogBase,
    VectorVariableDescriptor,
)


@final
class VariableCatalog(VariableCatalogBase):
    """A catalog of variable descriptors."""

    ABSOLUTE_PRESSURE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    """Pressure measured relative to a perfect vacuum (zero reference)."""

    ABSORBANCE = ScalarVariableDescriptor(Dimensions({}))
    """Logarithmic measure of the amount of light absorbed by a material."""

    ABSORBED_DOSE_RATE = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -3.0})
    )
    """Rate at which radiation energy is absorbed per unit mass."""

    ACCELERATION = VectorVariableDescriptor(Dimensions({_B.LENGTH: 1.0, _B.TIME: -2.0}))
    """Rate of change of velocity with respect to time."""

    ACCELERATION_MAGNITUDE = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    """Magnitude of the acceleration vector."""

    ACCELERATION_X = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    """Component of acceleration along the x-axis."""

    ACCELERATION_Y = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    """Component of acceleration along the y-axis."""

    ACCELERATION_Z = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    """Component of acceleration along the z-axis."""

    ACOUSTICAL_ABSORPTION = ScalarVariableDescriptor(Dimensions({}))
    """Fraction of incident sound energy absorbed by a surface."""

    ACTION = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -1.0})
    )
    """Product of energy and time characterizing a system's dynamics."""

    ANGLE = ScalarVariableDescriptor(Dimensions({_B.ANGLE: 1.0}))
    """Measure of rotation or the figure formed by two intersecting lines."""

    ANGULAR_ACCELERATION = ScalarVariableDescriptor(Dimensions({_B.TIME: -2.0}))
    """Rate of change of angular velocity with respect to time."""

    ANGULAR_MOMENTUM = VectorVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -1.0})
    )
    """Rotational analog of linear momentum for a rotating body."""

    ANGULAR_MOMENTUM_MAGNITUDE = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -1.0})
    )
    """Magnitude of the angular momentum vector."""

    ANGULAR_MOMENTUM_X = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -1.0})
    )
    """Component of angular momentum about the x-axis."""

    ANGULAR_MOMENTUM_Y = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -1.0})
    )
    """Component of angular momentum about the y-axis."""

    ANGULAR_MOMENTUM_Z = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -1.0})
    )
    """Component of angular momentum about the z-axis."""

    ANGULAR_VELOCITY = ScalarVariableDescriptor(Dimensions({_B.TIME: -1.0}))
    """Rate of change of angular position with respect to time."""

    AREA = ScalarVariableDescriptor(Dimensions({_B.LENGTH: 2.0}))
    """Extent of a two-dimensional surface or region."""

    AREA_DENSITY = ScalarVariableDescriptor(Dimensions({_B.MASS: 1.0, _B.LENGTH: -2.0}))
    """Mass per unit area of a surface."""

    ATOMIC_MASS = ScalarVariableDescriptor(Dimensions({_B.MASS: 1.0}))
    """Mass of a single atom."""

    ATOMIC_NUMBER = ScalarVariableDescriptor(Dimensions({}))
    """Number of protons in the nucleus of an atom."""

    ATTENUATION_COEFFICIENT = ScalarVariableDescriptor(Dimensions({_B.LENGTH: -1.0}))
    """Rate at which a quantity decreases as it passes through a medium."""

    AXIAL_VELOCITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    """Velocity component along the axial direction."""

    BIREFRINGENCE = ScalarVariableDescriptor(Dimensions({}))
    """Difference in refractive index seen by light of different polarizations."""

    BULK_MODULUS = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    """Resistance of a material to uniform compression."""

    CAPACITANCE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: -1.0, _B.LENGTH: -2.0, _B.TIME: 4.0, _B.CURRENT: 2.0})
    )
    """Ability of a system to store electric charge per unit voltage."""

    CATALYTIC_EFFICIENCY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 3.0, _B.CHEMICAL_AMOUNT: -1.0, _B.TIME: -1.0})
    )
    """Measure of how effectively an enzyme converts substrate to product."""

    CELL_REYNOLDS_NUMBER = ScalarVariableDescriptor(Dimensions({}))
    """Reynolds number evaluated at the length scale of a mesh cell."""

    CHEMICAL_AMOUNT = ScalarVariableDescriptor(Dimensions({_B.CHEMICAL_AMOUNT: 1.0}))
    """Quantity of substance measured in moles."""

    COEFFICIENT_OF_RESTITUTION = ScalarVariableDescriptor(Dimensions({}))
    """Ratio of relative speeds after and before an impact."""

    COLOR = ScalarVariableDescriptor(Dimensions({}))
    """Qualitative visual property determined by the wavelength of light."""

    COMPRESSIBILITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: -1.0, _B.LENGTH: 1.0, _B.TIME: 2.0})
    )
    """Relative volume change of a fluid or solid in response to pressure."""

    COMPRESSIVE_STRENGTH = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    """Maximum compressive stress a material can withstand before failure."""

    CONVECTIVE_COURANT_NUMBER = ScalarVariableDescriptor(Dimensions({}))
    """Ratio of flow distance to cell size over a time step, indicating numerical
    stability."""

    CORROSION_RESISTANCE = ScalarVariableDescriptor(Dimensions({}))
    """Ability of a material to resist degradation by chemical reaction."""

    CREEP = ScalarVariableDescriptor(Dimensions({_B.TIME: -1.0}))
    """Slow, time-dependent deformation of a material under sustained stress."""

    CURIE_TEMPERATURE = ScalarVariableDescriptor(Dimensions({_B.TEMPERATURE: 1.0}))
    """Temperature above which a material loses its permanent magnetism."""

    CURRENT = ScalarVariableDescriptor(Dimensions({_B.CURRENT: 1.0}))
    """Flow of electric charge per unit time."""

    DENSITY = ScalarVariableDescriptor(Dimensions({_B.MASS: 1.0, _B.LENGTH: -3.0}))
    """Mass per unit volume of a substance."""

    DIAMAGNETISM = ScalarVariableDescriptor(Dimensions({}))
    """Tendency of a material to be weakly repelled by a magnetic field."""

    DIELECTRIC_CONSTANT = ScalarVariableDescriptor(Dimensions({}))
    """Relative permittivity of a material compared with vacuum."""

    DIELECTRIC_STRENGTH = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -3.0, _B.CURRENT: -1.0})
    )
    """Maximum electric field a material can withstand without breaking down."""

    DUCTILITY = ScalarVariableDescriptor(Dimensions({}))
    """Ability of a material to deform plastically before fracture."""

    DURABILITY = ScalarVariableDescriptor(Dimensions({}))
    """Ability of a material to withstand wear, pressure, or damage over time."""

    DYNAMIC_PRESSURE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    """Kinetic energy per unit volume of a moving fluid."""

    DYNAMIC_VISCOSITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -1.0})
    )
    """Measure of a fluid's resistance to shear flow."""

    EFFECTIVE_PRANDTL_NUMBER = ScalarVariableDescriptor(Dimensions({}))
    """Prandtl number adjusted for turbulent transport effects."""

    EFFECTIVE_THERMAL_CONDUCTIVITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.MASS: 1.0, _B.TIME: -3.0, _B.TEMPERATURE: -1.0})
    )
    """Thermal conductivity including the effect of turbulent mixing."""

    EFFECTIVE_VISCOSITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -1.0})
    )
    """Total viscosity combining molecular and turbulent contributions."""

    ELASTICITY = ScalarVariableDescriptor(Dimensions({}))
    """Ability of a material to return to its original shape after deformation."""

    ELECTRICAL_CAPACITANCE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: -1.0, _B.LENGTH: -2.0, _B.TIME: 4.0, _B.CURRENT: 2.0})
    )
    """Ability of a component to store electric charge per unit voltage."""

    ELECTRICAL_CONDUCTANCE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: -1.0, _B.LENGTH: -2.0, _B.TIME: 3.0, _B.CURRENT: 2.0})
    )
    """Ease with which electric current flows through a conductor."""

    ELECTRICAL_CONDUCTIVITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: -1.0, _B.LENGTH: -3.0, _B.TIME: 3.0, _B.CURRENT: 2.0})
    )
    """Material's ability to conduct electric current per unit length."""

    ELECTRICAL_IMPEDANCE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0, _B.TIME: -3.0, _B.CURRENT: -2.0})
    )
    """Opposition of a circuit to alternating current, including resistance and
    reactance."""

    ELECTRICAL_INDUCTANCE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0, _B.TIME: -2.0, _B.CURRENT: -2.0})
    )
    """Property of a conductor that opposes changes in electric current."""

    ELECTRICAL_POTENTIAL = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0, _B.TIME: -3.0, _B.CURRENT: -1.0})
    )
    """Electric potential energy per unit charge (voltage)."""

    ELECTRICAL_REACTANCE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0, _B.TIME: -3.0, _B.CURRENT: -2.0})
    )
    """Opposition to alternating current due to capacitance or inductance."""

    ELECTRICAL_RESISTANCE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0, _B.TIME: -3.0, _B.CURRENT: -2.0})
    )
    """Opposition of a material to the flow of electric current."""

    ELECTRICAL_RESISTIVITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 3.0, _B.TIME: -3.0, _B.CURRENT: -2.0})
    )
    """Intrinsic resistance of a material per unit length and area."""

    ELECTRIC_CHARGE = ScalarVariableDescriptor(
        Dimensions({_B.TIME: 1.0, _B.CURRENT: 1.0})
    )
    """Fundamental property of matter that causes electromagnetic interaction."""

    ELECTRIC_SUSCEPTIBILITY = ScalarVariableDescriptor(Dimensions({}))
    """Degree to which a material becomes polarized in an electric field."""

    ELECTROCALORIC_COEFFICIENT = ScalarVariableDescriptor(
        Dimensions(
            {
                _B.TEMPERATURE: 1.0,
                _B.MASS: -1.0,
                _B.LENGTH: -2.0,
                _B.TIME: 3.0,
                _B.CURRENT: 1.0,
            }
        )
    )
    """Temperature change of a material per unit applied electric field."""

    ELECTROSTRICTION = ScalarVariableDescriptor(Dimensions({}))
    """Strain produced in a dielectric material by an applied electric field."""

    ELECTRO_OPTIC_EFFECT = ScalarVariableDescriptor(Dimensions({}))
    """Change in a material's refractive index caused by an electric field."""

    EMISSIVITY = ScalarVariableDescriptor(Dimensions({}))
    """Effectiveness of a surface in emitting thermal radiation relative to a
    blackbody."""

    ENERGY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    """Capacity to do work or produce heat."""

    ENERGY_DENSITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: -1.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    """Amount of energy stored per unit volume."""

    ENERGY_FLUX_DENSITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.TIME: -3.0})
    )
    """Rate of energy transfer per unit area."""

    ENTHALPY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    """Total heat content of a system at constant pressure."""

    ENTROPY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0, _B.TEMPERATURE: -1.0})
    )
    """Measure of the disorder or unavailable energy in a system."""

    FATIGUE_LIMIT = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    """Maximum stress a material can endure for an infinite number of loading cycles."""

    FLEXURAL_MODULUS = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    """Material's resistance to bending deformation."""

    FLEXURAL_STRENGTH = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    """Maximum bending stress a material can withstand before failure."""

    FORCE = VectorVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    """Interaction that changes the motion of a body."""

    FORCE_MAGNITUDE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    """Magnitude of the force vector."""

    FORCE_X = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    """Component of force along the x-axis."""

    FORCE_Y = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    """Component of force along the y-axis."""

    FORCE_Z = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -2.0})
    )
    """Component of force along the z-axis."""

    FRACTURE_TOUGHNESS = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.TIME: -2.0})
    )
    """Resistance of a material to crack propagation."""

    FREQUENCY = ScalarVariableDescriptor(Dimensions({_B.TIME: -1.0}))
    """Number of occurrences of a repeating event per unit time."""

    FREQUENCY_DRIFT = ScalarVariableDescriptor(Dimensions({_B.TIME: -2.0}))
    """Rate of change of frequency over time."""

    FRICTION_COEFFICIENT = ScalarVariableDescriptor(Dimensions({}))
    """Ratio of frictional force to normal force between surfaces."""

    FUEL_EFFICIENCY = ScalarVariableDescriptor(Dimensions({_B.LENGTH: -2.0}))
    """Distance traveled per unit volume of fuel consumed."""

    HALF_LIFE = ScalarVariableDescriptor(Dimensions({_B.TIME: 1.0}))
    """Time required for a quantity to reduce to half its initial value."""

    HALL_COEFFICIENT = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 3.0, _B.CURRENT: -1.0, _B.TIME: -1.0})
    )
    """Measure of the voltage developed across a conductor in a magnetic field."""

    HARDNESS = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    """Resistance of a material to localized plastic deformation."""

    HEAT_CAPACITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0, _B.TEMPERATURE: -1.0})
    )
    """Amount of heat required to change a body's temperature by one degree."""

    HEAT_FLUX_DENSITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.TIME: -3.0})
    )
    """Rate of heat transfer per unit area."""

    HEAT_OF_VAPORIZATION = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    """Energy required to vaporize a unit mass of a substance."""

    HYGROSCOPY = ScalarVariableDescriptor(Dimensions({}))
    """Tendency of a material to absorb moisture from the air."""

    HYSTERESIS = ScalarVariableDescriptor(Dimensions({}))
    """Dependence of a system's state on its history of applied conditions."""

    ILLUMINANCE = ScalarVariableDescriptor(
        Dimensions({_B.LIGHT: 1.0, _B.SOLID_ANGLE: 1.0, _B.LENGTH: -2.0})
    )
    """Luminous flux incident on a surface per unit area."""

    INTERNAL_ENERGY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    """Total energy contained within a thermodynamic system."""

    JERK = ScalarVariableDescriptor(Dimensions({_B.LENGTH: 1.0, _B.TIME: -3.0}))
    """Rate of change of acceleration with respect to time."""

    KINEMATIC_VISCOSITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -1.0})
    )
    """Ratio of dynamic viscosity to fluid density."""

    LENGTH = ScalarVariableDescriptor(Dimensions({_B.LENGTH: 1.0}))
    """Measure of distance or extent in one dimension."""

    LIGHT = ScalarVariableDescriptor(Dimensions({_B.LIGHT: 1.0}))
    """Luminous intensity of a light source."""

    LINEAR_MASS_DENSITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0})
    )
    """Mass per unit length of an object."""

    LUMINANCE = ScalarVariableDescriptor(Dimensions({_B.LIGHT: 1.0, _B.LENGTH: -2.0}))
    """Luminous intensity per unit area of a surface."""

    LUMINOSITY = ScalarVariableDescriptor(
        Dimensions({_B.LIGHT: 1.0, _B.SOLID_ANGLE: 1.0})
    )
    """Total luminous flux emitted by a source."""

    LUMINOUS_EXPOSURE = ScalarVariableDescriptor(
        Dimensions({_B.LIGHT: 1.0, _B.SOLID_ANGLE: 1.0, _B.LENGTH: -2.0, _B.TIME: 1.0})
    )
    """Illuminance accumulated over a period of time."""

    LUMINOUS_FLUX = ScalarVariableDescriptor(
        Dimensions({_B.LIGHT: 1.0, _B.SOLID_ANGLE: 1.0})
    )
    """Total perceived power of light emitted by a source."""

    MAGNETIC_FLUX = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0, _B.TIME: -2.0, _B.CURRENT: -1.0})
    )
    """Total magnetic field passing through a given area."""

    MAGNETIC_INDUCTION = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.TIME: -2.0, _B.CURRENT: -1.0})
    )
    """Magnetic flux density, or strength of a magnetic field."""

    MAGNETIC_PERMEABILITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.MASS: 1.0, _B.TIME: -2.0, _B.CURRENT: -2.0})
    )
    """Ability of a material to support the formation of a magnetic field."""

    MAGNETIC_VECTOR_POTENTIAL = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.MASS: 1.0, _B.TIME: -2.0, _B.CURRENT: -1.0})
    )
    """Vector field whose curl gives the magnetic flux density."""

    MAGNETOCALORIC_COEFFICIENT = ScalarVariableDescriptor(
        Dimensions({_B.TEMPERATURE: 1.0, _B.MASS: -1.0, _B.TIME: 2.0, _B.CURRENT: 1.0})
    )
    """Temperature change of a material per unit applied magnetic field."""

    MAGNETOELECTRIC_POLARIZABILITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: -1.0, _B.TIME: -1.0})
    )
    """Coupling between electric polarization and magnetic field in a material."""

    MAGNETORESISTANCE = ScalarVariableDescriptor(Dimensions({}))
    """Change in electrical resistance of a material in a magnetic field."""

    MAGNETOSTRICTION = ScalarVariableDescriptor(Dimensions({}))
    """Change in a material's dimensions due to magnetization."""

    MAGNETOTHERMOELECTRIC_POWER = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -1.0, _B.TEMPERATURE: -1.0})
    )
    """Thermoelectric voltage generated per unit temperature and magnetic field."""

    MALLEABILITY = ScalarVariableDescriptor(Dimensions({}))
    """Ability of a material to be deformed under compression without fracture."""

    MASS = ScalarVariableDescriptor(Dimensions({_B.MASS: 1.0}))
    """Measure of the amount of matter in a body."""

    MASS_CONTROL = ScalarVariableDescriptor(Dimensions({_B.MASS: 1.0, _B.TIME: -3.0}))
    """Control quantity representing the third time derivative of mass."""

    MASS_DIFFUSIVITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -1.0})
    )
    """Rate at which mass diffuses through a medium."""

    MASS_FLOW_RATE = ScalarVariableDescriptor(Dimensions({_B.MASS: 1.0, _B.TIME: -1.0}))
    """Mass of fluid passing through a section per unit time."""

    MAXIMUM_ENERGY_PRODUCT = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: -1.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    """Maximum energy density stored in a permanent magnet."""

    MELTING_POINT = ScalarVariableDescriptor(Dimensions({_B.TEMPERATURE: 1.0}))
    """Temperature at which a solid becomes a liquid."""

    MESH_VELOCITY = VectorVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    """Velocity of mesh nodes in a moving or deforming grid."""

    MESH_VELOCITY_MAGNITUDE = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    """Magnitude of the mesh velocity vector."""

    MESH_VELOCITY_X = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    """Component of mesh velocity along the x-axis."""

    MESH_VELOCITY_Y = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    """Component of mesh velocity along the y-axis."""

    MESH_VELOCITY_Z = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    """Component of mesh velocity along the z-axis."""

    MIXTURE_DENSITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -3.0})
    )
    """Density of the combined multiphase mixture."""

    MOLALITY = ScalarVariableDescriptor(
        Dimensions({_B.CHEMICAL_AMOUNT: 1.0, _B.MASS: -1.0})
    )
    """Amount of solute per unit mass of solvent."""

    MOLARITY = ScalarVariableDescriptor(
        Dimensions({_B.CHEMICAL_AMOUNT: 1.0, _B.LENGTH: -3.0})
    )
    """Amount of solute per unit volume of solution."""

    MOLAR_ENERGY = ScalarVariableDescriptor(
        Dimensions(
            {_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0, _B.CHEMICAL_AMOUNT: -1.0}
        )
    )
    """Energy per mole of substance."""

    MOLAR_ENTROPY = ScalarVariableDescriptor(
        Dimensions(
            {
                _B.LENGTH: 2.0,
                _B.MASS: 1.0,
                _B.TIME: -2.0,
                _B.TEMPERATURE: -1.0,
                _B.CHEMICAL_AMOUNT: -1.0,
            }
        )
    )
    """Entropy per mole of substance."""

    MOLAR_HEAT_CAPACITY = ScalarVariableDescriptor(
        Dimensions(
            {
                _B.LENGTH: 2.0,
                _B.MASS: 1.0,
                _B.TIME: -2.0,
                _B.TEMPERATURE: -1.0,
                _B.CHEMICAL_AMOUNT: -1.0,
            }
        )
    )
    """Heat required to raise one mole of substance by one degree."""

    MOLAR_MASS = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.CHEMICAL_AMOUNT: -1.0})
    )
    """Mass of one mole of a substance."""

    MOLAR_VOLUME = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 3.0, _B.CHEMICAL_AMOUNT: -1.0})
    )
    """Volume occupied by one mole of a substance."""

    MOMENTUM = VectorVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    """Product of mass and velocity of a body."""

    MOMENTUM_MAGNITUDE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    """Magnitude of the momentum vector."""

    MOMENTUM_X = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    """Component of momentum along the x-axis."""

    MOMENTUM_Y = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    """Component of momentum along the y-axis."""

    MOMENTUM_Z = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    """Component of momentum along the z-axis."""

    MOMENT_OF_INERTIA = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0})
    )
    """Resistance of a body to angular acceleration about an axis."""

    NERNST_COEFFICIENT = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -1.0, _B.TEMPERATURE: -1.0})
    )
    """Transverse voltage generated per unit temperature gradient and magnetic field."""

    NEUTRON_CROSS_SECTION = ScalarVariableDescriptor(Dimensions({_B.LENGTH: 2.0}))
    """Effective area quantifying the probability of a neutron interaction."""

    NORMALIZED_Q_CRITERION = ScalarVariableDescriptor(Dimensions({}))
    """Dimensionless form of the Q-criterion for identifying vortices."""

    OPTICAL_ACTIVITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.MASS: -1.0})
    )
    """Ability of a substance to rotate the plane of polarized light."""

    PERMEABILITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.MASS: 1.0, _B.TIME: -2.0, _B.CURRENT: -2.0})
    )
    """Ability of a material to support a magnetic field within it."""

    PERMITTIVITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: -1.0, _B.LENGTH: -3.0, _B.TIME: 4.0, _B.CURRENT: 2.0})
    )
    """Ability of a material to store electrical energy in an electric field."""

    PH = ScalarVariableDescriptor(Dimensions({}))
    """Measure of the acidity or alkalinity of a solution."""

    PHOTOELASTICITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: -1.0, _B.LENGTH: 1.0, _B.TIME: 2.0})
    )
    """Change in a material's optical properties under mechanical stress."""

    PHOTOSENSITIVITY = ScalarVariableDescriptor(Dimensions({}))
    """Degree to which a material responds to incident light."""

    PIEZOELECTRIC_CONSTANTS = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -1.0, _B.CURRENT: -1.0})
    )
    """Coefficients relating mechanical stress to generated electric field."""

    PIEZOMAGNETISM = ScalarVariableDescriptor(
        Dimensions({_B.CURRENT: -1.0, _B.LENGTH: 1.0})
    )
    """Magnetization induced in a material by applied mechanical stress."""

    PLASTICITY = ScalarVariableDescriptor(Dimensions({}))
    """Ability of a material to undergo permanent deformation without fracture."""

    POISSON_RATIO = ScalarVariableDescriptor(Dimensions({}))
    """Ratio of transverse to axial strain in a deformed material."""

    POSITION = VectorVariableDescriptor(Dimensions({_B.LENGTH: 1.0}))
    """Location of a point in space relative to a reference."""

    POSITION_MAGNITUDE = ScalarVariableDescriptor(Dimensions({_B.LENGTH: 1.0}))
    """Distance of a point from the reference origin."""

    POSITION_X = ScalarVariableDescriptor(Dimensions({_B.LENGTH: 1.0}))
    """Position coordinate along the x-axis."""

    POSITION_Y = ScalarVariableDescriptor(Dimensions({_B.LENGTH: 1.0}))
    """Position coordinate along the y-axis."""

    POSITION_Z = ScalarVariableDescriptor(Dimensions({_B.LENGTH: 1.0}))
    """Position coordinate along the z-axis."""

    POWER = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -3.0})
    )
    """Rate at which energy is transferred or work is done."""

    PRANDTL_NUMBER = ScalarVariableDescriptor(Dimensions({}))
    """Ratio of momentum diffusivity to thermal diffusivity in a fluid."""

    PRESSURE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    """Force applied perpendicular to a surface per unit area."""

    PRESSURE_COEFFICIENT = ScalarVariableDescriptor(Dimensions({}))
    """Dimensionless number relating local pressure to dynamic pressure."""

    PRESSURE_HESSIAN_INDICATOR = ScalarVariableDescriptor(Dimensions({}))
    """Pressure-Hessian-based indicator used to drive mesh adaption."""

    PRODUCTION_OF_TURBULENT_KINETIC_ENERGY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -3.0})
    )
    """Rate at which turbulent kinetic energy is generated in a flow."""

    PYROELECTRICITY = ScalarVariableDescriptor(
        Dimensions({_B.CURRENT: 1.0, _B.LENGTH: -2.0, _B.TEMPERATURE: -1.0})
    )
    """Generation of electric charge in a material due to temperature change."""

    PYROMAGNETIC_COEFFICIENT = ScalarVariableDescriptor(
        Dimensions(
            {_B.MASS: 1.0, _B.TIME: -2.0, _B.CURRENT: -1.0, _B.TEMPERATURE: -1.0}
        )
    )
    """Change in magnetization of a material per unit temperature change."""

    Q_CRITERION = ScalarVariableDescriptor(Dimensions({_B.TIME: -2.0}))
    """Vortex identification criterion based on the velocity gradient tensor."""

    RADIAL_VELOCITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    """Velocity component in the radial direction."""

    RADIANCE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.TIME: -3.0, _B.SOLID_ANGLE: -1.0})
    )
    """Radiant power per unit solid angle per unit projected area."""

    RADIANT_EXPOSURE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.TIME: -2.0})
    )
    """Radiant energy received per unit area."""

    RADIANT_INTENSITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -3.0, _B.SOLID_ANGLE: -1.0})
    )
    """Radiant power emitted per unit solid angle."""

    REACTIVITY = ScalarVariableDescriptor(Dimensions({}))
    """Tendency of a substance to undergo chemical reaction."""

    REFLECTIVITY = ScalarVariableDescriptor(Dimensions({}))
    """Fraction of incident radiation reflected by a surface."""

    REFRACTIVE_INDEX = ScalarVariableDescriptor(Dimensions({}))
    """Ratio of the speed of light in vacuum to its speed in a medium."""

    RELATIVE_ATOMIC_MASS = ScalarVariableDescriptor(Dimensions({}))
    """Mass of an atom relative to one-twelfth the mass of carbon-12."""

    RESILIENCE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    """Energy absorbed per unit volume during elastic deformation."""

    SCATTERING = ScalarVariableDescriptor(Dimensions({}))
    """Deflection of radiation or particles by a medium."""

    SEEBECK_COEFFICIENT = ScalarVariableDescriptor(
        Dimensions(
            {
                _B.MASS: 1.0,
                _B.LENGTH: 2.0,
                _B.TIME: -3.0,
                _B.CURRENT: -1.0,
                _B.TEMPERATURE: -1.0,
            }
        )
    )
    """Voltage generated per unit temperature difference in a material."""

    SHEAR_MODULUS = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    """Material's resistance to shear deformation."""

    SHEAR_STRENGTH = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    """Maximum shear stress a material can withstand before failure."""

    SKIN_FRICTION_COEFFICIENT = ScalarVariableDescriptor(Dimensions({}))
    """Dimensionless wall shear stress normalized by dynamic pressure."""

    SLIP = ScalarVariableDescriptor(Dimensions({}))
    """Relative motion between contacting surfaces or phases."""

    SNAP = ScalarVariableDescriptor(Dimensions({_B.LENGTH: 1.0, _B.TIME: -4.0}))
    """Rate of change of jerk with respect to time."""

    SOLID_ANGLE = ScalarVariableDescriptor(Dimensions({_B.SOLID_ANGLE: 1.0}))
    """Two-dimensional angle subtended at a point by a surface."""

    SOUND_REFLECTION = ScalarVariableDescriptor(Dimensions({}))
    """Fraction of incident sound energy reflected by a surface."""

    SOUND_TRANSFER = ScalarVariableDescriptor(Dimensions({}))
    """Fraction of sound energy transmitted through a medium."""

    SPECIFIC_ACTIVITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: -1.0, _B.TIME: -1.0})
    )
    """Radioactive activity per unit mass of a sample."""

    SPECIFIC_ANGULAR_MOMENTUM = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -1.0})
    )
    """Angular momentum per unit mass."""

    SPECIFIC_DISSIPATION_RATE = ScalarVariableDescriptor(Dimensions({_B.TIME: -1.0}))
    """Rate of dissipation of turbulent kinetic energy per unit energy."""

    SPECIFIC_ENERGY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    """Energy per unit mass."""

    SPECIFIC_ENTHALPY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    """Enthalpy per unit mass."""

    SPECIFIC_ENTROPY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0, _B.TEMPERATURE: -1.0})
    )
    """Entropy per unit mass."""

    SPECIFIC_HEAT_CAPACITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0, _B.TEMPERATURE: -1.0})
    )
    """Heat required to raise unit mass of a substance by one degree."""

    SPECIFIC_INTERNAL_ENERGY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    """Internal energy per unit mass."""

    SPECIFIC_INTERNAL_SURFACE_AREA = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: -1.0})
    )
    """Internal surface area per unit volume of a porous material."""

    SPECIFIC_MODULUS = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    """Elastic modulus per unit density of a material."""

    SPECIFIC_STRENGTH = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    """Material strength per unit density."""

    SPECIFIC_TOTAL_ENERGY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    """Total energy per unit mass."""

    SPECIFIC_TOTAL_ENTHALPY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    """Total enthalpy per unit mass."""

    SPECIFIC_VOLUME = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 3.0, _B.MASS: -1.0})
    )
    """Volume per unit mass, the inverse of density."""

    SPECIFIC_WEIGHT = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -2.0, _B.TIME: -2.0})
    )
    """Weight per unit volume of a substance."""

    SPECTRAL_INTENSITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.MASS: 1.0, _B.TIME: -3.0, _B.SOLID_ANGLE: -1.0})
    )
    """Radiant intensity per unit wavelength."""

    SPECTRAL_IRRADIANCE = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: -1.0, _B.MASS: 1.0, _B.TIME: -3.0})
    )
    """Radiant power received per unit area per unit wavelength."""

    SPECTRAL_POWER = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.MASS: 1.0, _B.TIME: -3.0})
    )
    """Radiant power per unit wavelength."""

    SPEED_OF_SOUND = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    """Speed at which sound waves propagate through a medium."""

    SPIN_HALL_EFFECT = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 2.0, _B.TIME: -3.0, _B.CURRENT: -2.0})
    )
    """Generation of a transverse spin current by an electric field."""

    STANDARD_ATOMIC_WEIGHT = ScalarVariableDescriptor(Dimensions({}))
    """Average atomic mass of an element's isotopes relative to carbon-12."""

    STATIC_PRESSURE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    """Pressure of a fluid at rest relative to the flow."""

    STRAIN_RATE = ScalarVariableDescriptor(Dimensions({_B.TIME: -1.0}))
    """Rate of deformation of a material per unit time."""

    STRESS = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    """Internal force per unit area within a deformable body."""

    SURFACE_ENERGY = ScalarVariableDescriptor(Dimensions({_B.MASS: 1.0, _B.TIME: -2.0}))
    """Excess energy at the surface of a material per unit area."""

    SURFACE_HEAT_FLUX = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.TIME: -3.0})
    )
    """Rate of heat transfer per unit area at a surface."""

    SURFACE_HEAT_TRANSFER_COEFFICIENT = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.TIME: -3.0, _B.TEMPERATURE: -1.0})
    )
    """Heat transfer rate per unit area per unit temperature difference at a surface."""

    SURFACE_NUSSELT_NUMBER = ScalarVariableDescriptor(Dimensions({}))
    """Ratio of convective to conductive heat transfer at a surface."""

    SURFACE_ROUGHNESS = ScalarVariableDescriptor(Dimensions({_B.LENGTH: 1.0}))
    """Measure of the fine irregularities on a surface."""

    SURFACE_STANTON_NUMBER = ScalarVariableDescriptor(Dimensions({}))
    """Ratio of heat transferred to the thermal capacity of the fluid at a surface."""

    SURFACE_TENSION = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.TIME: -2.0})
    )
    """Elastic tendency of a fluid surface to minimize its area."""

    TANGENTIAL_VELOCITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    """Velocity component in the tangential direction."""

    TEMPERATURE = ScalarVariableDescriptor(Dimensions({_B.TEMPERATURE: 1.0}))
    """Measure of the thermal energy or hotness of a body."""

    TEMPERATURE_DIFFERENCE = ScalarVariableDescriptor(
        Dimensions({_B.TEMPERATURE_DIFFERENCE: 1.0})
    )
    """Difference between two temperatures."""

    TEMPERATURE_GRADIENT = ScalarVariableDescriptor(
        Dimensions({_B.TEMPERATURE: 1.0, _B.LENGTH: -1.0})
    )
    """Rate of temperature change with distance."""

    TENSILE_STRENGTH = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    """Maximum tensile stress a material can withstand before breaking."""

    THERMAL_CONDUCTIVITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.MASS: 1.0, _B.TIME: -3.0, _B.TEMPERATURE: -1.0})
    )
    """Ability of a material to conduct heat."""

    THERMAL_DIFFUSIVITY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -1.0})
    )
    """Rate at which heat diffuses through a material."""

    THERMAL_EXPANSION_COEFFICIENT = ScalarVariableDescriptor(
        Dimensions({_B.TEMPERATURE: -1.0})
    )
    """Fractional change in size of a material per unit temperature change."""

    THERMAL_RESISTANCE = ScalarVariableDescriptor(
        Dimensions({_B.TEMPERATURE: 1.0, _B.LENGTH: -2.0, _B.MASS: -1.0, _B.TIME: 3.0})
    )
    """Resistance of a material to the flow of heat."""

    THIRD_ORDER_ELASTICITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    """Higher-order elastic response describing nonlinear stress-strain behavior."""

    TIME = ScalarVariableDescriptor(Dimensions({_B.TIME: 1.0}))
    """Measure of the progression of events."""

    TORQUE = VectorVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    """Rotational force that causes a body to rotate about an axis."""

    TORQUE_MAGNITUDE = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    """Magnitude of the torque vector."""

    TORQUE_X = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    """Component of torque about the x-axis."""

    TORQUE_Y = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    """Component of torque about the y-axis."""

    TORQUE_Z = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    """Component of torque about the z-axis."""

    TOTAL_ENERGY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    """Sum of internal and kinetic energy of a system."""

    TOTAL_PRESSURE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    """Sum of static and dynamic pressure in a flowing fluid."""

    TOTAL_TEMPERATURE = ScalarVariableDescriptor(Dimensions({_B.TEMPERATURE: 1.0}))
    """Temperature a fluid attains when brought to rest adiabatically."""

    TOUGHNESS = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: -1.0, _B.MASS: 1.0, _B.TIME: -2.0})
    )
    """Energy a material can absorb before fracturing."""

    TRANSMITTANCE = ScalarVariableDescriptor(Dimensions({}))
    """Fraction of incident radiation that passes through a material."""

    TURBULENT_DISSIPATION_RATE = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: 3.0})
    )
    """Rate at which turbulent kinetic energy is converted to heat."""

    TURBULENT_INTENSITY = ScalarVariableDescriptor(Dimensions({}))
    """Ratio of velocity fluctuations to the mean flow velocity."""

    TURBULENT_KINETIC_ENERGY = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 2.0, _B.TIME: -2.0})
    )
    """Kinetic energy per unit mass of turbulent velocity fluctuations."""

    TURBULENT_REYNOLDS_NUMBER = ScalarVariableDescriptor(Dimensions({}))
    """Reynolds number based on turbulent quantities."""

    TURBULENT_VISCOSITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -1.0})
    )
    """Apparent viscosity arising from turbulent momentum transport."""

    TURBULENT_VISCOSITY_RATIO = ScalarVariableDescriptor(Dimensions({}))
    """Ratio of turbulent to molecular viscosity."""

    VAPOR_PRESSURE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    """Pressure exerted by a vapor in equilibrium with its liquid."""

    VELOCITY = VectorVariableDescriptor(Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0}))
    """Rate of change of position with respect to time."""

    VELOCITY_MAGNITUDE = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0})
    )
    """Magnitude of the velocity vector (speed)."""

    VELOCITY_X = ScalarVariableDescriptor(Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0}))
    """Component of velocity along the x-axis."""

    VELOCITY_Y = ScalarVariableDescriptor(Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0}))
    """Component of velocity along the y-axis."""

    VELOCITY_Z = ScalarVariableDescriptor(Dimensions({_B.LENGTH: 1.0, _B.TIME: -1.0}))
    """Component of velocity along the z-axis."""

    VISCOSITY = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -1.0})
    )
    """Measure of a fluid's resistance to flow."""

    VOLUME = ScalarVariableDescriptor(Dimensions({_B.LENGTH: 3.0}))
    """Amount of three-dimensional space occupied by a substance."""

    VOLUMETRIC_FLOW = ScalarVariableDescriptor(
        Dimensions({_B.LENGTH: 3.0, _B.TIME: -1.0})
    )
    """Volume of fluid passing through a section per unit time."""

    VOLUME_FRACTION = ScalarVariableDescriptor(Dimensions({}))
    """Fraction of a total volume occupied by a given phase."""

    VORTICITY = VectorVariableDescriptor(Dimensions({_B.TIME: -1.0}))
    """Local spinning motion of a fluid, the curl of the velocity field."""

    VORTICITY_MAGNITUDE = ScalarVariableDescriptor(Dimensions({_B.TIME: -1.0}))
    """Magnitude of the vorticity vector."""

    VORTICITY_X = ScalarVariableDescriptor(Dimensions({_B.TIME: -1.0}))
    """Component of vorticity about the x-axis."""

    VORTICITY_Y = ScalarVariableDescriptor(Dimensions({_B.TIME: -1.0}))
    """Component of vorticity about the y-axis."""

    VORTICITY_Z = ScalarVariableDescriptor(Dimensions({_B.TIME: -1.0}))
    """Component of vorticity about the z-axis."""

    WALL_ADJACENT_HEAT_TRANSFER_COEFFICIENT = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.TIME: -3.0, _B.TEMPERATURE: -1.0})
    )
    """Heat transfer coefficient evaluated in the cell adjacent to a wall."""

    WALL_ADJACENT_TEMPERATURE = ScalarVariableDescriptor(
        Dimensions({_B.TEMPERATURE: 1.0})
    )
    """Fluid temperature in the cell adjacent to a wall."""

    WALL_SHEAR_STRESS = VectorVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    """Shear stress exerted by a fluid on a wall surface."""

    WALL_SHEAR_STRESS_MAGNITUDE = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    """Magnitude of the wall shear stress vector."""

    WALL_SHEAR_STRESS_X = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    """Component of wall shear stress along the x-axis."""

    WALL_SHEAR_STRESS_Y = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    """Component of wall shear stress along the y-axis."""

    WALL_SHEAR_STRESS_Z = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    """Component of wall shear stress along the z-axis."""

    WALL_TEMPERATURE = ScalarVariableDescriptor(Dimensions({_B.TEMPERATURE: 1.0}))
    """Temperature at a wall surface."""

    WALL_TEMPERATURE_THIN = ScalarVariableDescriptor(Dimensions({_B.TEMPERATURE: 1.0}))
    """Wall temperature computed for a thin-wall thermal model."""

    WALL_Y_PLUS = ScalarVariableDescriptor(Dimensions({}))
    """Dimensionless wall distance used in turbulence modeling."""

    WALL_Y_STAR = ScalarVariableDescriptor(Dimensions({}))
    """Dimensionless wall distance based on turbulent kinetic energy."""

    WAVENUMBER = ScalarVariableDescriptor(Dimensions({_B.LENGTH: -1.0}))
    """Number of wave cycles per unit distance."""

    YANK = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: 1.0, _B.TIME: -3.0})
    )
    """Rate of change of force with respect to time."""

    YIELD_STRENGTH = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    """Stress at which a material begins to deform plastically."""

    YOUNG_MODULUS = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.LENGTH: -1.0, _B.TIME: -2.0})
    )
    """Measure of a material's stiffness under tensile or compressive load."""

    Y_PLUS_BASED_HEAT_TRANSFER_COEFFICIENT = ScalarVariableDescriptor(
        Dimensions({_B.MASS: 1.0, _B.TIME: -3.0, _B.TEMPERATURE: -1.0})
    )
    """Heat transfer coefficient derived from the wall y-plus value."""

    HELICITY = ScalarVariableDescriptor(_D.ANGULAR_MOMENTUM)
    """In particle physics, the projection of a particle's spin onto its direction of
    motion."""

    HYDRODYNAMICAL_HELICITY = ScalarVariableDescriptor(_D.ACCELERATION)
    """In fluid dynamics, a measure of the knottedness and/or linkage of the vortex
    lines of a flow."""

    MAGNETIC_HELICITY = ScalarVariableDescriptor(
        _D.MAGNETIC_VECTOR_POTENTIAL * _D.MAGNETIC_INDUCTION
    )
    """In plasma physics and magnetohydrodynamics, a measure of the twist, linkage, and
    writhe of magnetic field lines within a volume."""

    LAMBDA_2_CRITERION = ScalarVariableDescriptor(_D.TIME**-2)
    """The lambda 2 criterion, which concerns the definition of the scalar lambda2 and
    how turbulent structures can be visualized by proper iso-surfaces of lambda2 (like
    for the Q criterion)."""

    TOTAL_ENTHALPY_DEVIATION = ScalarVariableDescriptor(_D.SPECIFIC_ENTHALPY)
    """Deviation of total enthalpy from a reference value."""

    MASS_IMBALANCE = ScalarVariableDescriptor(_D.MASS * _D.TIME**-1)
    """Residual mass source indicating continuity error in a solution."""

    VELOCITY_ANGLE = ScalarVariableDescriptor(_D.ANGLE)
    """Angle of the velocity vector relative to a reference direction."""

    DVELOCITY_DX = ScalarVariableDescriptor(_D.TIME**-1)
    """Spatial derivative of velocity with respect to the x-coordinate."""

    DVELOCITY_DX_MAGNITUDE = ScalarVariableDescriptor(_D.TIME**-1)
    """Magnitude of the velocity derivative with respect to x."""

    DVELOCITY_DX_X = ScalarVariableDescriptor(_D.TIME**-1)
    """X-component of the velocity derivative with respect to x."""

    DVELOCITY_DX_Y = ScalarVariableDescriptor(_D.TIME**-1)
    """Y-component of the velocity derivative with respect to x."""

    DVELOCITY_DX_Z = ScalarVariableDescriptor(_D.TIME**-1)
    """Z-component of the velocity derivative with respect to x."""

    DVELOCITY_DY = ScalarVariableDescriptor(_D.TIME**-1)
    """Spatial derivative of velocity with respect to the y-coordinate."""

    DVELOCITY_DY_MAGNITUDE = ScalarVariableDescriptor(_D.TIME**-1)
    """Magnitude of the velocity derivative with respect to y."""

    DVELOCITY_DY_X = ScalarVariableDescriptor(_D.TIME**-1)
    """X-component of the velocity derivative with respect to y."""

    DVELOCITY_DY_Y = ScalarVariableDescriptor(_D.TIME**-1)
    """Y-component of the velocity derivative with respect to y."""

    DVELOCITY_DY_Z = ScalarVariableDescriptor(_D.TIME**-1)
    """Z-component of the velocity derivative with respect to y."""

    DVELOCITY_DZ = ScalarVariableDescriptor(_D.TIME**-1)
    """Spatial derivative of velocity with respect to the z-coordinate."""

    DVELOCITY_DZ_MAGNITUDE = ScalarVariableDescriptor(_D.TIME**-1)
    """Magnitude of the velocity derivative with respect to z."""

    DVELOCITY_DZ_X = ScalarVariableDescriptor(_D.TIME**-1)
    """X-component of the velocity derivative with respect to z."""

    DVELOCITY_DZ_Y = ScalarVariableDescriptor(_D.TIME**-1)
    """Y-component of the velocity derivative with respect to z."""

    DVELOCITY_DZ_Z = ScalarVariableDescriptor(_D.TIME**-1)
    """Z-component of the velocity derivative with respect to z."""

    VOLUME_FRACTION_PRIMARY_PHASE = ScalarVariableDescriptor(_D.VOLUME_FRACTION)
    """Volume fraction occupied by the primary phase."""

    VOLUME_FRACTION_SECONDARY_PHASE = ScalarVariableDescriptor(_D.VOLUME_FRACTION)
    """Volume fraction occupied by the secondary phase."""

    MESH_ANISOTROPIC_ADAPTION_CELLS = ScalarVariableDescriptor(Dimensions())
    """Number of cells marked for anisotropic mesh adaption."""

    MESH_BOUNDARY_CELL_DISTANCE = ScalarVariableDescriptor(Dimensions())
    """Number of cells between a cell and the nearest boundary."""

    MESH_BOUNDARY_LAYER_CELLS = ScalarVariableDescriptor(Dimensions())
    """Count of cells within the boundary layer region."""

    MESH_BOUNDARY_NORMAL_DISTANCE = ScalarVariableDescriptor(Dimensions())
    """Normal distance from a cell to the nearest boundary."""

    MESH_BOUNDARY_VOLUME_DISTANCE = ScalarVariableDescriptor(Dimensions())
    """Volume-weighted distance from a cell to the boundary."""

    MESH_CELL_EQUIANGLE_SKEW = ScalarVariableDescriptor(Dimensions())
    """Measure of cell skewness based on deviation from ideal angles."""

    MESH_CELL_EQUIVOLUME_SKEW = ScalarVariableDescriptor(Dimensions())
    """Measure of cell skewness based on deviation from ideal volume."""

    MESH_CELL_PARENT_INDEX = ScalarVariableDescriptor(Dimensions())
    """Index of the parent cell in a refined mesh."""

    MESH_CELL_REFINE_LEVEL = ScalarVariableDescriptor(Dimensions())
    """Refinement level of a mesh cell."""

    MESH_CELL_VOLUME = ScalarVariableDescriptor(_D.VOLUME)
    """Volume of a mesh cell."""

    MESH_CELL_VOLUME_CHANGE = ScalarVariableDescriptor(Dimensions())
    """Relative change in cell volume between mesh states."""

    MESH_ELEMENT_ASPECT_RATIO = ScalarVariableDescriptor(Dimensions())
    """Ratio of the longest to shortest dimension of a mesh element."""

    MESH_ELEMENT_WALL_DISTANCE = ScalarVariableDescriptor(_D.LENGTH)
    """Distance from a mesh element to the nearest wall."""

    MESH_FACE_AREA_MAGNITUDE = ScalarVariableDescriptor(_D.AREA)
    """Magnitude of the area of a mesh face."""

    MESH_FACE_HANDEDNESS = ScalarVariableDescriptor(Dimensions())
    """Orientation consistency of a mesh face."""

    MESH_INTERFACE_OVERLAP_FRACTION = ScalarVariableDescriptor(Dimensions())
    """Fraction of overlap between mesh interfaces."""

    MESH_MARK_POOR_ELEMENTS = ScalarVariableDescriptor(Dimensions())
    """Flag identifying mesh elements of poor quality."""

    MESH_SMOOTHED_CELL_REFINE_LEVEL = ScalarVariableDescriptor(Dimensions())
    """Smoothed refinement level across neighboring cells."""

    MESH_X_FACE_AREA = ScalarVariableDescriptor(_D.AREA)
    """X-component of a mesh face area vector."""

    MESH_Y_FACE_AREA = ScalarVariableDescriptor(_D.AREA)
    """Y-component of a mesh face area vector."""

    MESH_Z_FACE_AREA = ScalarVariableDescriptor(_D.AREA)
    """Z-component of a mesh face area vector."""

    MESH_ACTIVE_CELL_PARTITION = ScalarVariableDescriptor(Dimensions())
    """Active partition index assigned to a mesh cell."""

    MESH_CELL_ELEMENT_TYPE = ScalarVariableDescriptor(Dimensions())
    """Geometric element type of a mesh cell."""

    MESH_CELL_ID = ScalarVariableDescriptor(Dimensions())
    """Unique identifier of a mesh cell."""

    MESH_CELL_WEIGHT = ScalarVariableDescriptor(Dimensions())
    """Computational weight assigned to a mesh cell for load balancing."""

    MESH_CELL_ZONE_INDEX = ScalarVariableDescriptor(Dimensions())
    """Index of the zone to which a mesh cell belongs."""

    MESH_CELL_ZONE_TYPE = ScalarVariableDescriptor(Dimensions())
    """Type of the zone to which a mesh cell belongs."""

    MESH_PARTITION_NEIGHBOURS = ScalarVariableDescriptor(Dimensions())
    """Number of neighboring partitions for a mesh cell."""

    MESH_STORED_CELL_PARTITION = ScalarVariableDescriptor(Dimensions())
    """Stored partition index assigned to a mesh cell."""
