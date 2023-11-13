.. _frequently:

==========================
Frequently Asked Questions
==========================

How is PyAnsys Units different from pint?
"""""""""""""""""""""""""""""""""""""""""

In contrast to pint, the ``UnitRegistry`` is only a container of ``Unit`` objects. The
registry does not contain additional information. Notably the ``UnitSystem`` is a
standalone class. When creating a ``Unit`` using ``Dimensions`` it requires a unit
system parameter to be passed in for non-SI units.

PyAnsys Units treats all angles as dimensioned units. With this behavior the conversion
from rad/s to Hz is not allowed.