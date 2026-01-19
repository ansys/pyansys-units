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

from pathlib import Path
import sys

import black

src = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src))

from ansys.units.quantity_dimensions import QuantityDimensions

quantity_dimensions = src / "ansys" / "units" / "quantity_dimensions.py"

# Read the existing file content
existing_content = quantity_dimensions.read_text()

# Generate the expanded vector quantities
expanded_lines = list[str]()
for name in QuantityDimensions._vector_quantities:
    # cartesian only added by default
    expanded_lines.append(f"    {name}_X = {name}")
    expanded_lines.append(f"    {name}_Y = {name}")
    expanded_lines.append(f"    {name}_Z = {name}")
    # magnitude
    expanded_lines.append(f"    {name}_MAGNITUDE = {name}")
    expanded_lines.append("")

expanded_section = "\n".join(expanded_lines)
# Marker to identify where to insert the expanded quantities
inset_marker = "    # anything after this will be replaced by the script"
parts = existing_content.split(inset_marker, maxsplit=1)
new_content = (
    parts[0]
    + inset_marker
    + "\n\n    # Expanded vector quantities\n"
    + expanded_section
)


# Format with black and write
quantity_dimensions.write_text(
    black.format_str(
        new_content,
        mode=black.Mode(),
    )
)
