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

"""Plot Quantity objects with matplotlib."""

import matplotlib.pyplot as plt

from ansys.units import Quantity


class QuantityPlotter:
    """
    Plot a Quantity object.

    Parameters
    ----------
    x_quantity : Quantity
        The x-axis quantity.
    y_quantity : Quantity
        The y-axis quantity.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from ansys.units import Quantity, QuantityPlotter, UnitRegistry
    >>> x_quantity = Quantity([1, 2, 3], 'm')
    >>> y_quantity = Quantity([4, 5, 6], 'kg')
    >>> data = QuantityPlotter(x_quantity, y_quantity)
    >>> fig, ax = plt.subplots()
    >>> data.plot(ax)
    >>> plt.show()
    >>> # Example usage with numpy arrays
    >>> ureg = UnitRegistry()
    >>> y = Quantity(value=np.linspace(0, 30), units=ureg.m)
    >>> x = Quantity(value=np.linspace(0, 5), units=ureg.kg)
    >>> data = QuantityPlotter(x, y)
    >>> fig, ax = plt.subplots()
    >>> ax.axhline(Quantity(10, ureg.m).value, color='tab:red')
    >>> ax.axvline(Quantity(2, ureg.kg).value, color='tab:green')
    >>> data.plot(ax)
    >>> plt.show()
    """

    def __init__(self, x_quantity, y_quantity):
        if isinstance(x_quantity, Quantity):
            self.x_quantity_value = x_quantity.value
            self.x_quantity_unit = x_quantity.units._name
        else:
            self.x_quantity_value = x_quantity
            self.x_quantity_unit = None

        if isinstance(y_quantity, Quantity):
            self.y_quantity_value = y_quantity.value
            self.y_quantity_unit = y_quantity.units._name
        else:
            self.y_quantity_value = y_quantity
            self.y_quantity_unit = None

    def plot(self, ax=None, **kwargs):
        """
        Plot the Quantity object.

        Parameters
        ----------
        ax : matplotlib.axes.Axes, optional
            The matplotlib axes to plot on. If None, the current axes will be used.
        **kwargs
            Additional keyword arguments to pass to matplotlib.pyplot.plot.
        """
        if ax is None:
            ax = plt.gca()

        ax.plot(self.x_quantity_value, self.y_quantity_value, **kwargs)

        if self.x_quantity_unit:
            ax.set_xlabel(f"X ({self.x_quantity_unit})")
        if self.y_quantity_unit:
            ax.set_ylabel(f"Y ({self.y_quantity_unit})")

        return ax
