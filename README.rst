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
PyAnsys Units provides a Pythonic interface for units, unit systems, and unit
conversions. Its features enable seamless setup and usage of physical
quantities, enabling you to perform these tasks:

- Instantiate physical quantities from a unit string, list of dimensions, or
  quantity map.
- Perform unit conversions and arithmetic operations between quantity objects or
  real values.
- Create custom units and unit systems.

Documentation and issues
------------------------

Documentation for the latest stable release of PyAnsys Units is hosted at `PyAnsys Units documentation
<https://units.docs.pyansys.com>`_.

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

The ``ansys.units`` package supports Python 3.8 through Python 3.11 on Windows
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

Basic usage
~~~~~~~~~~~

Import the `ansys.units`` package:

.. code:: python

   import ansys.units as ansunits

You can instantiate quantities with one of three methods:

.. code:: python

   # unit string

   volume = ansunits.Quantity(value=1, units="m^3")

   volume.value  # 1.0
   volume.units  # "m^3"

   # dimensions

   acceleration = ansunits.Quantity(value=3, dimensions=[0, 1, -2])

   acceleration.value  # 3.0
   acceleration.units  # "m s^-2"

   # quantity map

   torque = ansunits.Quantity(5, quantity_map={"Torque": 1})

   torque.value  # 5.0
   torque.units  # "N m"

You can instantiate unit systems with one of two methods:

.. code:: python

   # custom unit systems

   sys = ansunits.UnitSystem(
       name="sys",
       base_units=["slug", "ft", "s", "R", "radian", "slugmol", "cd", "A", "sr"],
   )

   # pre-defined unit systems

   si = ansunits.UnitSystem(unit_sys="SI")

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

   fps = ansunits.Quantity(1, "lb ft^-1 s^-1")
   fps.value  # 1

   pas = fps.to("Pa s")
   pas.value  # 1.4881639435695542
   pas.units  # 'Pa s'

Use a custom unit system to perform conversions:

.. code:: python

   import ansys.units as ansunits

   sys = ansunits.UnitSystem(
       name="sys",
       base_units=["slug", "ft", "s", "R", "radian", "slugmol", "cd", "A", "sr"],
   )

   v = ansunits.Quantity(10, "kg m s^2")
   v2 = sys.convert(v)

   v2.value  # 2.2480894309971045
   v2.units  # 'slug ft s^2'

License
-------
PyAnsys Units is licensed under the MIT license. For more information, see the
`LICENSE <https://github.com/ansys/pyansys-units/raw/main/LICENSE>`_ file.
