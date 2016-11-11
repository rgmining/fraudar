.. _top:

A wrapper of FRAUDAR algorithm
=================================
.. raw:: html

   <div class="addthis_inline_share_toolbox"></div>

This package implements a wrapper of
`FRAUDAR <https://www.andrew.cmu.edu/user/bhooi/projects/fraudar/index.html>`_
algorithm to provide APIs defined in
`Review Graph Mining project`_.


Installation
--------------
Use `pip` to install this package.

.. code-block:: bash

   pip install --upgrade rgmining-fraudar


Usage
-------
This package provides a review graph class
:class:`ReviewGraph <fraudar.graph.ReviewGraph>`, and it takes two arguments;
a number of blocks and a sub algorithm computing degree of a matrix.
See `the original article <http://www.andrew.cmu.edu/user/bhooi/papers/fraudar_kdd16.pdf>`_
for more information about those arguments.

To construct a review graph instance with :math:`n` blocks and
:meth:`aveDegree <fraudar.export.greedy.aveDegree>` algorithm,

.. code-block:: python

  import fraudar
  graph = fraudar.ReviewGraph(n, fraudar.aveDegree)

The constructed graph object has as same interface as other graph classes in
`Review Graph Mining project`_.


API Reference
---------------
.. toctree::
  :glob:
  :maxdepth: 2

  modules/*


License
---------
This software is released under The GNU General Public License Version 3,
see `COPYING <https://github.com/rgmining/fraudar/blob/master/COPYING>`_ for more detail.

The original FRAUDAR source code, which is in ``fraudar/export``, are made by
`Bryan Hooi <https://www.andrew.cmu.edu/user/bhooi/index.html>`_,
`Hyun Ah Song <http://www.cs.cmu.edu/~hyunahs/>`_,
`Alex Beutel <http://alexbeutel.com/>`_,
`Neil Shah <http://www.cs.cmu.edu/~neilshah/>`_,
`Kijung Shin <http://www.cs.cmu.edu/~kijungs/>`_, and
`Christos Faloutsos <http://www.cs.cmu.edu/~christos/>`_,
and licensed under `Apache License, Version 2.0 <https://github.com/rgmining/fraudar/blob/master/LICENSE-2.0>`_.


.. _Review Graph Mining project: https://rgmining.github.io/
