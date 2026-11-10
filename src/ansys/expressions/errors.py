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

"""Exception types for the expression builder."""

from typing_extensions import override


class ExpressionBuildError(Exception):
    """Raised when an expression tree cannot be built or rendered."""

    node: object | None
    slot: str | None

    def __init__(
        self, message: str, node: object | None = None, slot: str | None = None
    ) -> None:
        # Forward all arguments so pickle and copy.copy can reconstruct the
        # exception via ``cls(*exc.args)``; keyword-only parameters would make
        # that reconstruction impossible.
        super().__init__(message, node, slot)
        self.node = node
        self.slot = slot

    @override
    def __str__(self) -> str:
        """Return the error message."""
        return str(self.args[0])
