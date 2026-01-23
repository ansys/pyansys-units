PyUnits
=======
|pyansys| |pypi| |GH-CI| |codecov| |MIT| |black| |pre-commit|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |pypi| image:: https://img.shields.io/pypi/v/ansys-units.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/ansys-units
   :alt: PyPI

.. |GH-CI| image:: https://github.com/ansys/pyunits/actions/workflows/ci_cd.yml/badge.svg
   :target: https://github.com/ansys/pyunits/actions/workflows/ci_cd.yml
   :alt: GH-CI

.. |codecov| image:: https://codecov.io/gh/ansys/pyunits/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/ansys/pyunits

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
   :target: https://github.com/psf/black
   :alt: Black

.. |pre-commit| image:: https://results.pre-commit.ci/badge/github/ansys/pyunits/main.svg
   :target: https://results.pre-commit.ci/latest/github/ansys/pyunits/main
   :alt: pre-commit.ci status

Overview
--------
PyUnits provides a pythonic interface for units, unit systems, and unit conversions. Its
features enable seamless setup and usage of physical quantities, including the ability to:

- Instantiate physical quantities from a unit string, list of dimensions, or quantity map.
- Perform unit conversions and arithmetic operations between quantity objects or real values.
- Create custom units and unit systems.

Documentation and Issues
------------------------

For comprehensive information on PyUnits, see the latest release
`documentation <https://pyunits.docs.pyansys.com>`_.

On the `PyUnits Issues <https://github.com/ansys/pyunits/issues>`_ page, you can create
issues to submit questions, report bugs, and request new features. To reach
the project support team, email `pyansys.core@ansys.com <pyansys.core@ansys.com>`_.

Installation
------------

The ``ansys.units`` package supports Python 3.8 through Python 3.11 on Windows and Linux.


Install the latest release from `PyPI <https://pypi.org/project/ansys-units>`_ with:

.. code:: console

   pip install ansys-units

If you plan on doing local *development* of PyUnits with Git, install the latest release with:

.. code:: console

   git clone https://github.com/ansys/pyunits.git
   cd pyunits
   pip install pip -U
   pip install -e .

Getting Started
---------------

Basic Usage
~~~~~~~~~~~

Import the pyunits library:

.. code:: python

   import ansys.units as q

Quantities can be instantiated with 1 of 3 methods:

.. code:: python

   # unit string

   volume = q.Quantity(value=1, units="m^3")

   volume.value >>> 1
   volume.units >>> "m^3"

   # dimensions

   acceleration = q.Quantity(value=3, dimensions=[0, 1, -2])

   acceleration.value >>> 3
   acceleration.units >>> "m s^-2"

   # quantity map

   torque = q.Quantity(5, quantity_map={"Torque": 1})

   torque.value >>> 5
   torque.units >>> "N m"

Unit systems can be instantiated with 1 of 2 methods:

.. code:: python

   # custom unit systems

   sys = q.UnitSystem(
      name="sys",
      base_units=["slug", "ft", "s", "R", "radian", "slugmol", "cd", "A", "sr"]
   )

   # pre-defined unit systems

   si = q.UnitSystem(unit_sys="SI")

Examples
~~~~~~~~~~~

Arithmetic

.. code:: python

   import ansys.units as q

   deg = q.Quantity(90, "degree")
   math.sin(deg) >>> 1.0

   v1 = q.Quantity(10.0, "m s^-1")
   v2 = q.Quantity(5.0, "m s^-1")

   v3 = v1 - v2
   v3.value >>> 5

   vpow = v1**2
   vpow.value >>> 100
   vpow.units >>> "m^2 s^-2"

Conversions

.. code:: python

   import ansys.units as q

   fps = q.Quantity(1, "lb ft^-1 s^-1")
   fps.value >>> 1

   pas = fps.to("Pa s")
   pas.value >>> 1.488164


Unit Systems

.. code:: python

   import ansys.units as q

   sys = q.UnitSystem(
      name="sys",
      base_units=["slug", "ft", "s", "R", "radian", "slugmol", "cd", "A", "sr"],
   )

   v = q.Quantity(10, "kg m s^2")
   v2 = sys.convert(v)

   v2.value >>> 10
   v2.units >>> "slug ft s^2"

License and acknowledgments
---------------------------