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
"""
Defines the ConversionStrategy base class for translating `VariableDescriptor` objects.

Each concrete strategy maps `VariableDescriptor` instances to the string representations
required by a specific system.
"""

from abc import ABC, abstractmethod
import types

from ansys.units.variable_descriptor.variable_descriptor import VariableDescriptor


class ConversionStrategy(ABC):
    """
    Abstract base class for `VariableDescriptor` conversion strategies.

    This class defines the interface for all conversion strategies. Derived classes
    must implement the methods defined here to handle the conversion of `VariableDescriptor`
    objects to and from their string representations, as well as to check if a
    `VariableDescriptor` is supported.
    """

    @abstractmethod
    def to_string(self, variable: VariableDescriptor | str | None) -> str | None:
        """
        Convert a `VariableDescriptor` to its string representation.

        Parameters
        ----------
        variable : VariableDescriptor | str
            The `VariableDescriptor` to convert, or a string representation.

        Returns
        -------
        str
            The string representation of the `VariableDescriptor`.

        Raises
        ------
        NotImplementedError
            If the method is not implemented in a derived class.
        """
        pass

    @abstractmethod
    def to_variable_descriptor(
        self, variable: VariableDescriptor | str
    ) -> VariableDescriptor:
        """
        Convert a string to its corresponding `VariableDescriptor`.

        Parameters
        ----------
        variable : VariableDescriptor | str
            The string representation to convert, or a `VariableDescriptor`.

        Returns
        -------
        VariableDescriptor
            The corresponding `VariableDescriptor` instance.

        Raises
        ------
        NotImplementedError
            If the method is not implemented in a derived class.
        """
        pass

    @abstractmethod
    def supports(self, variable: VariableDescriptor) -> bool:
        """
        Check if the given `VariableDescriptor` is supported by the strategy.

        Parameters
        ----------
        variable : VariableDescriptor
            The `VariableDescriptor` to check.

        Returns
        -------
        bool
            `True` if the `VariableDescriptor` is supported, `False` otherwise.

        Raises
        ------
        NotImplementedError
            If the method is not implemented in a derived class.
        """
        pass


class MappingConversionStrategy(ConversionStrategy):
    """
    Intermediate base class for implementing VariableDescriptor conversion strategies.

    This class simplifies the creation of concrete strategy classes by providing
    default implementations for common methods. Classes inheriting from this base
    class only need to define a `_mapping` dictionary that maps `VariableDescriptor`
    instances to their corresponding string representations.

    Attributes
    ----------
    _reverse_mapping : dict
        A lazily initialized reverse mapping of `_mapping`, used for converting
        strings back to `VariableDescriptor` instances.

    Methods
    -------
    to_string(variable: VariableDescriptor | str) -> str
        Converts a `VariableDescriptor` to its string representation. Raises a
        `ValueError` if the variable is not supported.
    to_variable_descriptor(variable: VariableDescriptor | str) -> VariableDescriptor
        Converts a string to its corresponding `VariableDescriptor`.
    supports(variable: VariableDescriptor) -> bool
        Checks if the given `VariableDescriptor` is supported by the strategy.

    Raises
    ------
    ValueError
        If a `VariableDescriptor` is not supported during conversion to a string.
    """

    def __init__(self):
        """
        Initialize the MappingConversionStrategy.

        This constructor initializes the reverse mapping attribute to `None`.
        The reverse mapping is lazily initialized when accessed via the `_reverse_mapping` property.
        """
        self.__reverse_mapping = None

    @property
    def _reverse_mapping(self):
        """
        Get the reverse mapping of `_mapping`.

        The reverse mapping is a dictionary that maps string representations
        back to their corresponding `VariableDescriptor` instances. It is lazily
        initialized on first access.

        Returns
        -------
        dict
            A dictionary mapping string representations to `VariableDescriptor` instances.
        """
        if self.__reverse_mapping is None:
            self.__reverse_mapping = {x: y for y, x in self._mapping.items()}
        return self.__reverse_mapping

    def to_string(self, variable: VariableDescriptor | str | None) -> str | None:
        """
        Convert a `VariableDescriptor` to its string representation.

        If the input is already a string, it is returned as-is. If the input
        is a `VariableDescriptor` and is supported by the strategy, its string
        representation is returned. Otherwise, a `ValueError` is raised.

        Parameters
        ----------
        variable : VariableDescriptor | str
            The `VariableDescriptor` to convert, or a string representation.

        Returns
        -------
        str
            The string representation of the `VariableDescriptor`.

        Raises
        ------
        ValueError
            If the `VariableDescriptor` is not supported by the strategy.
        """
        if isinstance(variable, (str, types.NoneType)):
            return variable
        if not self.supports(variable):
            raise ValueError(f"{variable.name} not supported.")
        return self._mapping[variable]

    def to_variable_descriptor(
        self, variable: VariableDescriptor | str
    ) -> VariableDescriptor:
        """
        Convert a string to its corresponding `VariableDescriptor`.

        If the input is already a `VariableDescriptor`, it is returned as-is.
        Otherwise, the string is converted to a `VariableDescriptor` using the
        reverse mapping.

        Parameters
        ----------
        variable : VariableDescriptor | str
            The string representation to convert, or a `VariableDescriptor`.

        Returns
        -------
        VariableDescriptor
            The corresponding `VariableDescriptor` instance, or `None` if the
            string is not found in the reverse mapping.
        """
        if isinstance(variable, VariableDescriptor):
            return variable
        return self._reverse_mapping.get(variable)

    def supports(self, variable: VariableDescriptor) -> bool:
        """
        Check if the given `VariableDescriptor` is supported by the strategy.

        Parameters
        ----------
        variable : VariableDescriptor
            The `VariableDescriptor` to check.

        Returns
        -------
        bool
            `True` if the `VariableDescriptor` is supported, `False` otherwise.
        """
        return variable in self._mapping
