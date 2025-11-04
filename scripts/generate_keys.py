# /// script
# requires-python = ">=3.12"
# ///
# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
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

from collections import defaultdict
from pathlib import Path

import yaml
import black

from ansys.units._constants import _base_units, _derived_units

src = Path(__file__).parent.parent / "src"
units = src / "ansys" / "units"
si_table = units / "quantity_tables" / "si_table.yaml"
keys_path = units / "quantity_tables" / "keys.py"

with si_table.open("r") as fp:
    table_data = yaml.safe_load(fp)

common = Path(__file__).parent.parent / "src" / "ansys" / "units" / "common.py"
all = (*_base_units, *_derived_units)

dims = defaultdict[str, list[str]](list)
for key, value in _base_units.items():
    dims[value["type"]].append(key)


keys_path.touch(exist_ok=True)
keys_path.write_text(
    black.format_file_contents(
        f"""\
# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.

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

from typing import Literal

UnitKey = Literal[
{"\n".join(f'    "{key}",' for key in all)}
]

{
            "\n\n".join(
                f'''{dim.title().replace("_", "")}Key = Literal[
{"\n".join(f'    "{unit}",' for unit in values)}
]'''
                for dim, values in dims.items()
            )
        }

QuantityKey = Literal[
{"\n".join(f'    "{key}",' for key in table_data["quantity_units_table"])}
]
""",
        fast=True,
        mode=black.Mode(),
    )
)
