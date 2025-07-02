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

from pydantic import BaseModel

from ansys.units import Quantity


class PydanticQuantityModel(BaseModel):
    quantity: Quantity


def test_pydantic_quantity():
    """Test the PydanticQuantityModel serialization and deserialization."""

    # Create an instance of PydanticQuantityModel
    measurement = PydanticQuantityModel(
        quantity={"value": 42.0, "units": "m s^-1", "source": "any"}
    )

    # Serialize the object to a dict
    serialized = measurement.model_dump()

    # Assert that the serialized data matches the expected structure
    assert serialized == {
        "quantity": {"value": 42.0, "units": "m s^-1", "source": "any"}
    }

    # Deserialize back to an object
    deserialized = PydanticQuantityModel(**serialized)

    # Assert that the deserialized object matches the original
    assert deserialized == measurement


def test_pydantic_quantity_array():
    """Test the PydanticQuantityModel serialization and deserialization."""

    # Create an instance of PydanticQuantityModel
    measurement = PydanticQuantityModel(
        quantity={"value": [42.0, 43.0, 44.0], "units": "m s^-1", "source": "any"}
    )

    # Serialize the object to a dict
    serialized = measurement.model_dump()

    # Deserialize back to an object
    deserialized = PydanticQuantityModel(**serialized)

    # Assert that the deserialized object matches the original
    assert deserialized == measurement
