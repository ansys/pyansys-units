.. _ref_contributing:

==========
Contribute
==========
Overall guidance on contributing to a PyAnsys library appears in the
`Contributing <https://dev.docs.pyansys.com/how-to/contributing.html>`_ topic in
the *PyAnsys Developer's Guide*. Ensure that you are thoroughly familiar with
this guide before attempting to contribute to PyAnsys Units.

The following contribution information is specific to PyAnsys Units.

Clone and install
-----------------
Clone and install the latest PyAnsys Units release in development mode with
these commands:

.. code::

    git clone https://github.com/ansys/pyansys-units.git
    cd ansunits
    pip install pip -U
    pip install -e .

Build documentation
-------------------
Build the PyAnsys Units documentation locally by running these commands in the
root directory of the repository:

.. code::

    pip install -r requirements/requirements_doc.txt
    cd doc
    make html

After the build completes, the HTML documentation is located in the
``_builds/html`` directory. You can load the ``index.html`` file in this
directory into a web browser.

You can clear all HTML files from the ``_builds/html`` directory with
this command:

.. code::

    make clean

Post issues
-----------
Use the `PyAnsys Units Issues <https://github.com/ansys/pyansys-units/issues>`_ page to
report bugs and request new features.


Adhere to code style
--------------------
PyAnsys Units is compliant with the `PyAnsys coding style
<https://dev.docs.pyansys.com/coding-style/index.html>`_. It uses
`pre-commit <https://pre-commit.com/>`_ to check the code style. You can install
and activate this tool with these commands:

.. code:: bash

   python -m pip install pre-commit
   pre-commit install

You can then directly execute ``pre-commit`` with this command:

.. code:: bash

    pre-commit run --all-files --show-diff-on-failure
