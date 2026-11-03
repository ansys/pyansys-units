# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "black",
#     "PyYAML",
#     "typing-extensions>=4.5.0",
# ]
# ///
# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
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

import inspect
from pathlib import Path
import re
import sys

import black

src = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src))

from ansys.units.base_dimensions import BaseDimensions
from ansys.units.dimensions import Dimensions
from ansys.units.quantity_dimensions import QuantityDimensions

variable_descriptor_file = (
    src
    / "ansys"
    / "units"
    / "variable_descriptor"
    / "_generated_variable_descriptor.py"
)

# Define the custom variables structure
_D = QuantityDimensions

# Additional top-level catalog variables for general CFD quantities that are
# not derived from QuantityDimensions introspection.
additional_variables: list[tuple[str, str]] = [
    # Helicity density is the dot product of velocity and vorticity, so it has
    # the dimension of velocity times vorticity (L T^-2).
    ("HELICITY", "_D.ACCELERATION"),
    # The lambda-2 criterion is the second eigenvalue of S^2 + Omega^2, where
    # the strain-rate and vorticity tensors have dimension T^-1, giving T^-2.
    ("LAMBDA_2_CRITERION", "_D.TIME**-2"),
    ("TOTAL_ENTHALPY_DEVIATION", "_D.SPECIFIC_ENTHALPY"),
    # residuals
    ("MASS_IMBALANCE", "_D.MASS * _D.TIME**-1"),
    # velocity angle and gradient components
    ("VELOCITY_ANGLE", "_D.ANGLE"),
    ("DVELOCITY_DX", "_D.TIME**-1"),
    ("DVELOCITY_DX_MAGNITUDE", "_D.TIME**-1"),
    ("DVELOCITY_DX_X", "_D.TIME**-1"),
    ("DVELOCITY_DX_Y", "_D.TIME**-1"),
    ("DVELOCITY_DX_Z", "_D.TIME**-1"),
    ("DVELOCITY_DY", "_D.TIME**-1"),
    ("DVELOCITY_DY_MAGNITUDE", "_D.TIME**-1"),
    ("DVELOCITY_DY_X", "_D.TIME**-1"),
    ("DVELOCITY_DY_Y", "_D.TIME**-1"),
    ("DVELOCITY_DY_Z", "_D.TIME**-1"),
    ("DVELOCITY_DZ", "_D.TIME**-1"),
    ("DVELOCITY_DZ_MAGNITUDE", "_D.TIME**-1"),
    ("DVELOCITY_DZ_X", "_D.TIME**-1"),
    ("DVELOCITY_DZ_Y", "_D.TIME**-1"),
    ("DVELOCITY_DZ_Z", "_D.TIME**-1"),
    # multiphase
    ("VOLUME_FRACTION_PRIMARY_PHASE", "_D.VOLUME_FRACTION"),
    ("VOLUME_FRACTION_SECONDARY_PHASE", "_D.VOLUME_FRACTION"),
    # mesh
    ("MESH_ANISOTROPIC_ADAPTION_CELLS", "Dimensions()"),
    ("MESH_BOUNDARY_CELL_DISTANCE", "Dimensions()"),
    ("MESH_BOUNDARY_LAYER_CELLS", "Dimensions()"),
    ("MESH_BOUNDARY_NORMAL_DISTANCE", "Dimensions()"),
    ("MESH_BOUNDARY_VOLUME_DISTANCE", "Dimensions()"),
    ("MESH_CELL_EQUIANGLE_SKEW", "Dimensions()"),
    ("MESH_CELL_EQUIVOLUME_SKEW", "Dimensions()"),
    ("MESH_CELL_PARENT_INDEX", "Dimensions()"),
    ("MESH_CELL_REFINE_LEVEL", "Dimensions()"),
    ("MESH_CELL_VOLUME", "_D.VOLUME"),
    ("MESH_CELL_VOLUME_CHANGE", "Dimensions()"),
    ("MESH_ELEMENT_ASPECT_RATIO", "Dimensions()"),
    ("MESH_ELEMENT_WALL_DISTANCE", "_D.LENGTH"),
    ("MESH_FACE_AREA_MAGNITUDE", "_D.AREA"),
    ("MESH_FACE_HANDEDNESS", "Dimensions()"),
    ("MESH_INTERFACE_OVERLAP_FRACTION", "Dimensions()"),
    ("MESH_MARK_POOR_ELEMENTS", "Dimensions()"),
    ("MESH_SMOOTHED_CELL_REFINE_LEVEL", "Dimensions()"),
    ("MESH_X_FACE_AREA", "_D.AREA"),
    ("MESH_Y_FACE_AREA", "_D.AREA"),
    ("MESH_Z_FACE_AREA", "_D.AREA"),
    # cell info
    ("MESH_ACTIVE_CELL_PARTITION", "Dimensions()"),
    ("MESH_CELL_ELEMENT_TYPE", "Dimensions()"),
    ("MESH_CELL_ID", "Dimensions()"),
    ("MESH_CELL_WEIGHT", "Dimensions()"),
    ("MESH_CELL_ZONE_INDEX", "Dimensions()"),
    ("MESH_CELL_ZONE_TYPE", "Dimensions()"),
    ("MESH_PARTITION_NEIGHBOURS", "Dimensions()"),
    ("MESH_STORED_CELL_PARTITION", "Dimensions()"),
]


def _dimension_to_string(dimension: Dimensions) -> str:
    """Convert a Dimension object to its string representation."""
    return re.sub(
        f"'({'|'.join(BaseDimensions.__members__)})'", r"_B.\1", repr(dimension)
    )


def _generate_main_variables() -> str:
    """Generate main catalog variables from QuantityDimensions."""
    lines = list[str]()

    # Get all Dimensions attributes from QuantityDimensions
    for attr_name, dimension in inspect.getmembers(
        QuantityDimensions,
        predicate=lambda x: isinstance(x, Dimensions),
    ):
        dimension: Dimensions
        dim_str = _dimension_to_string(dimension)
        kind = (
            "VectorVariableDescriptor"
            if attr_name in QuantityDimensions._vector_quantities
            else "ScalarVariableDescriptor"
        )
        lines.append(f"    {attr_name} = {kind}(Dimensions({dim_str}))")

    return "\n".join(lines)


def _generate_additional_variables(variables_list: list[tuple[str, str]]) -> str:
    """Generate additional top-level catalog variables with typed descriptors."""
    lines = list[str]()
    for var_name, dimension in variables_list:
        kind = (
            "VectorVariableDescriptor"
            if var_name in QuantityDimensions._vector_quantities
            else "ScalarVariableDescriptor"
        )
        lines.append(f"    {var_name} = {kind}({dimension})")

    return "\n".join(lines)


attributes = list[str]()
# First, generate main catalog variables from QuantityDimensions
attributes.append(_generate_main_variables())
# Then, append additional top-level variables
attributes.append(_generate_additional_variables(additional_variables))
attributes.append("")

auto_generated_attributes = "\n".join(attributes)

content = f'''\
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
# This file is @generated

from typing_extensions import final

from ansys.units.base_dimensions import BaseDimensions as _B
from ansys.units.dimensions import Dimensions
from ansys.units.quantity_dimensions import QuantityDimensions as _D
from ansys.units.variable_descriptor.variable_descriptor import (
    ScalarVariableDescriptor,
    VariableCatalogBase,
    VectorVariableDescriptor,
)


@final
class VariableCatalog(VariableCatalogBase):
    """A catalog of variable descriptors."""
{auto_generated_attributes}
'''


# Format with black and write
variable_descriptor_file.write_text(
    black.format_str(
        content,
        mode=black.Mode(),
    )
)
