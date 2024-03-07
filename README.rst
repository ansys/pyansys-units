PyAnsys Units
=============
|pyansys| |pypi| |python| |GH-CI| |codecov| |MIT| |black| |pre-commit|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |python| image:: https://img.shields.io/pypi/pyversions/ansys-units?logo=pypi
   :target: https://pypi.org/project/ansys-units/
   :alt: Python

.. |pypi| image:: https://img.shields.io/pypi/v/ansys-units.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/ansys-units
   :alt: PyPI

.. |GH-CI| image:: https://github.com/ansys/pyansys-units/actions/workflows/ci_cd.yml/badge.svg
   :target: https://github.com/ansys/pyansys-units/actions/workflows/ci_cd.yml
   :alt: GH-CI

.. |codecov| image:: https://codecov.io/gh/ansys/pyansys-units/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/ansys/pyansys-units

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
   :target: https://github.com/psf/black
   :alt: Black

.. |pre-commit| image:: https://results.pre-commit.ci/badge/github/ansys/pyansys-units/main.svg
   :target: https://results.pre-commit.ci/latest/github/ansys/pyansys-units/main
   :alt: pre-commit.ci status

Overview
--------
PyAnsys Units is a Python library designed for managing physical quantities,
which are combinations of numerical values and corresponding units of
measurement. This package facilitates arithmetic operations and conversions
between various units.

With a modular design, PyAnsys Units offers the flexibility to extend or
modify its extensive list of physical units and unit systems without
altering the source code. It seamlessly integrates with NumPy mathematical
operations.

PyAnsys Units comes bundled with a comprehensive set of physical units,
prefixes, and constants and boasts complete test coverage.

Documentation and issues
------------------------

Documentation for the latest stable release of PyAnsys Units is hosted at
`PyAnsys Units documentation <https://units.docs.pyansys.com>`_.

In the upper right corner of the documentation's title bar, there is an option for
switching from viewing the documentation for the latest stable release to viewing
the documentation for the development version or previously released versions.

On the `PyAnsys Units Issues <https://github.com/ansys/pyansys-units/issues>`_ page, you can
create issues to report bugs, and request new features. On the `PyAnsys Units Discussions
<https://github.com/ansys/pyansys-units/discussions>`_ page or the `Discussions <https://discuss.ansys.com/>`_
page on the Ansys Developer portal, you can post questions, share ideas, and get community feedback.


To reach the project support team, email `pyansys.core@ansys.com <pyansys.core@ansys.com>`_.

Installation
------------

The ``ansys.units`` package supports Python 3.9 through Python 3.11 on Windows
and Linux.


Install the latest release from `PyPI <https://pypi.org/project/ansys-units>`_
with this command:

.. code:: console

   pip install ansys-units

If you plan on doing local *development* of PyAnsys Units with Git, install the latest release with
these commands:

.. code:: console

   git clone https://github.com/ansys/pyansys-units.git
   cd pyansys-units
   pip install pip -U
   pip install -e .

Getting started
---------------

PyAnsys Units supports flexible instantiation of ``Quantity`` objects:

.. code:: python

   import ansys.units as ansunits

   # Using unit strings

   volume = ansunits.Quantity(value=1, units="m^3")

   volume.value  # 1.0
   volume.units.name  # "m^3"

   # Using Unit instances

   ureg = ansunits.UnitRegistry()

   mass = ansunits.Quantity(value=1, units=ureg.kg)

   volume.value  # 1.0
   volume.units.name  # "kg"

   # Using base dimensions

   dims = ansunits.BaseDimensions
   dimensions = ansunits.Dimensions({dims.LENGTH: 1, dims.TIME: -2})

   acceleration = ansunits.Quantity(value=3, dimensions=dimensions)

   acceleration.value  # 3.0
   acceleration.units.name  # "m s^-2"

   # Using the quantity map

   torque = ansunits.Quantity(5, quantity_map={"Torque": 1})

   torque.value  # 5.0
   torque.units.name  # "N m"
   torque.si_units  # "kg m^2 s^-2"

With ``NumPy`` installed, you can instantiate a ``Quantity`` using either
a list of floats or a ``NumPy`` array:

.. code:: python

    from ansys.units import Quantity
    import numpy as np

    length_array_quantity = Quantity(value=[1.0, 6.0, 7.0], units="m")
    length_array_quantity[1]  # Quantity (6.0, "m")
    time = Quantity(value=2, units="s")
    speed = length_array_quantity / time
    speed  # Quantity ([0.5 3. 3.5], "m s^-1")

You can instantiate unit systems with one of two methods:

.. code:: python

   # Use a pre-defined unit system

   si = ansunits.UnitSystem(unit_sys="SI")

   si.base_units  # ['kg', 'm', 's', 'K', 'delta_K', 'radian', 'mol', 'cd', 'A', 'sr']

   # Define a custom unit system from a dictionary of base units. Any unspecified
   # unit will default to the SI equivalent.

   ureg = ansunits.UnitRegistry()
   dims = ansunits.BaseDimensions

   sys = ansunits.UnitSystem(
       base_units={
           dims.MASS: ureg.slug,
           dims.LENGTH: ureg.ft,
           dims.TEMPERATURE: ureg.R,
           dims.TEMPERATURE_DIFFERENCE: ureg.delta_R,
           dims.CHEMICAL_AMOUNT: ureg.slugmol,
       }
   )

   sys.base_units  # ['slug', 'ft', 's', 'R', 'delta_R', 'radian', 'slugmol', 'cd', 'A', 'sr']

Examples
~~~~~~~~

Perform arithmetic operations:

.. code:: python

   import ansys.units as ansunits

   deg = ansunits.Quantity(90, "degree")
   math.sin(deg)  # 1.0

   v1 = ansunits.Quantity(10.0, "m s^-1")
   v2 = ansunits.Quantity(5.0, "m s^-1")

   v3 = v1 - v2
   v3.value  # 5.0

   vpow = v1**2
   vpow.value  # 100.0
   vpow.units  # "m^2 s^-2"

Directly convert values to another set of units:

.. code:: python

   import ansys.units as ansunits

   flbs = ansunits.Quantity(1, "lb ft^-1 s^-1")
   flbs.value  # 1

   pas = flbs.to("Pa s")
   pas.value  # 1.4881639435695542
   pas.units.name  # 'Pa s'

Use a custom unit system to perform conversions:

.. code:: python

   import ansys.units as ansunits

   ureg = ansunits.UnitRegistry()
   dims = ansunits.BaseDimensions

   sys = ansunits.UnitSystem(
       base_units={
           dims.MASS: ureg.slug,
           dims.LENGTH: ureg.ft,
           dims.TEMPERATURE: ureg.R,
           dims.TEMPERATURE_DIFFERENCE: ureg.delta_R,
           dims.CHEMICAL_AMOUNT: ureg.slugmol,
       }
   )

   v = ansunits.Quantity(10, "kg m s^2")
   v2 = sys.convert(v)

   v2.value  # 2.2480894309971045
   v2.units.name  # 'slug ft s^2'

License
-------
PyAnsys Units is licensed under the MIT license. For more information, see the
`LICENSE <https://github.com/ansys/pyansys-units/raw/main/LICENSE>`_ file.
