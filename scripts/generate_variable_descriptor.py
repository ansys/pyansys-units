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
variables = {
    "fluent": [
        # velocity
        # The dominant meaning of helicity comes from
        # particle physics where it is dimensionless.
        # In CFD, where it has a different
        # meaning, it usually has dimension L^2 T^-2.
        # In Fluent it is L T^-2.
        ("HELICITY", "_D.ACCELERATION"),
        # Lambda 2 criterion is documented as dimensionless
        # but is T^-2 in Fluent.
        ("LAMBDA_2_CRITERION", "_D.TIME**-2"),
        ("DENSITY_ALL", "_D.DENSITY"),
        (
            "Y_PLUS_BASED_HEAT_TRANSFER_COEFFICIENT",
            "_D.POWER * _D.LENGTH**-2 * _D.TEMPERATURE**-1",
        ),
        ("TOTAL_ENTHALPY_DEVIATION", "_D.SPECIFIC_ENTHALPY"),
        # residuals
        ("MASS_IMBALANCE", "_D.MASS * _D.TIME**-1"),
        # derivatives
        ("PRESSURE_HESSIAN_INDICATOR", "Dimensions()"),
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
        ("VOLUME_FRACTION_PRIMARY_PHASE", "_D.VOLUME_FRACTION"),
        ("VOLUME_FRACTION_SECONDARY_PHASE", "_D.VOLUME_FRACTION"),
    ],
    "mesh": [
        # mesh
        ("ANISOTROPIC_ADAPTION_CELLS", "Dimensions()"),
        ("BOUNDARY_CELL_DISTANCE", "Dimensions()"),
        ("BOUNDARY_LAYER_CELLS", "Dimensions()"),
        ("BOUNDARY_NORMAL_DISTANCE", "Dimensions()"),
        ("BOUNDARY_VOLUME_DISTANCE", "Dimensions()"),
        ("CELL_EQUIANGLE_SKEW", "Dimensions()"),
        ("CELL_EQUIVOLUME_SKEW", "Dimensions()"),
        ("CELL_PARENT_INDEX", "Dimensions()"),
        ("CELL_REFINE_LEVEL", "Dimensions()"),
        ("CELL_VOLUME", "_D.VOLUME"),
        ("CELL_VOLUME_CHANGE", "Dimensions()"),
        ("ELEMENT_ASPECT_RATIO", "Dimensions()"),
        ("ELEMENT_WALL_DISTANCE", "_D.LENGTH"),
        ("FACE_AREA_MAGNITUDE", "_D.AREA"),
        ("FACE_HANDEDNESS", "Dimensions()"),
        ("INTERFACE_OVERLAP_FRACTION", "Dimensions()"),
        ("MARK_POOR_ELEMENTS", "Dimensions()"),
        ("SMOOTHED_CELL_REFINE_LEVEL", "Dimensions()"),
        ("X_FACE_AREA", "_D.AREA"),
        ("Y_FACE_AREA", "_D.AREA"),
        ("Z_FACE_AREA", "_D.AREA"),
        # cell info
        ("ACTIVE_CELL_PARTITION", "Dimensions()"),
        ("CELL_ELEMENT_TYPE", "Dimensions()"),
        ("CELL_ID", "Dimensions()"),
        ("CELL_WEIGHT", "Dimensions()"),
        ("CELL_ZONE_INDEX", "Dimensions()"),
        ("CELL_ZONE_TYPE", "Dimensions()"),
        ("PARTITION_NEIGHBOURS", "Dimensions()"),
        ("STORED_CELL_PARTITION", "Dimensions()"),
    ],
}


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


def _generate_subcategory_class(
    category_name: str, variables_list: list[tuple[str, str]]
) -> str:
    """Generate a static subcategory class with typed variable descriptors."""
    lines = [
        f"    @final",  # noqa: F541
        f"    class {category_name}:",
        f'        """Dictionary of variable descriptors for {category_name}-related quantities."""',
        "",
    ]

    for var_name, dimension in variables_list:
        kind = (
            "VectorVariableDescriptor"
            if var_name in QuantityDimensions._vector_quantities
            else "ScalarVariableDescriptor"
        )
        lines.append(f"        {var_name} = {kind}({dimension})")

    return "\n".join(lines)


attributes = list[str]()
# First, generate main catalog variables from QuantityDimensions
attributes.append(_generate_main_variables())
attributes.append("")

# Then, generate each subcategory as a nested class
for category, vars_list in variables.items():
    attributes.append(_generate_subcategory_class(category, vars_list))
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
