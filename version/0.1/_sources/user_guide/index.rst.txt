.. _ref_user_guide:

==========
User guide
==========

Anyone who wants to use PyAnsys Units can import its Python modules and develop Python
code to work with physical quantities.

Overview
--------
To initialize a physical quantity, import the ``ansunits`` library and create a
new ``Quantity`` object:

.. code:: python

    import ansys.units as ansunits

    meter = ansunits.Quantity(value=1, units="m")

All ``Quantity`` objects work intuitively with arithmetic operators. Simply
insert them within an equation to perform mathematical operations.

.. code:: python


    import ansys.units as ansunits

    meter = ansunits.Quantity(value=1, units="m")

    m_ad = meter + 2  # 3
    m_sb = meter - 2  # -1
    m_ml = meter * 2  # 2
    m_dv = meter / 2  # 0.5
    m_sq = meter**2  # 1

The default unit system used when performing quantity operations is ``SI``. This
ensures consistency between ``Quantity`` objects using different unit systems, such
as CGS or BT.

To define a new unit system or create custom quantities, manually update the
``cfg.yaml`` file with your desired data. Once saved, these changes are reflected
throughout PyAnsys Units.

