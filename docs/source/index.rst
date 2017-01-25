:description: This package implements a wrapper of FRAUDAR algorithm to provide
  APIs defined in `Review Graph Mining project`_.

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


.. _graph_model:

Graph model
------------
FRAUDAR algorithm assumes review data are represented by a bipartite graph.
This graph has two kinds of nodes, reviewers and products.
A reviewer node and a product node are tied by an edge if the reviewer reviews
the product.
We extend the bipartite graph so that we can compute summary of rating scores.
In our bipartite graph, each review, i.e. edge, has a normalized rating score,
which means all scores are in :math:`[0, 1]`.

.. graphviz::

   digraph bipartite {
      graph [label="Bipartite graph example.", rankdir = LR];
      "reviewer-0";
      "reviewer-1";
      "product-0";
      "product-1";
      "product-2";
      "reviewer-0" -> "product-0" [label="0.2"];
      "reviewer-0" -> "product-1" [label="0.9"];
      "reviewer-0" -> "product-2" [label="0.6"];
      "reviewer-1" -> "product-1" [label="0.1"];
      "reviewer-1" -> "product-2" [label="0.7"];
  }

In the above bipartite graph example, there are two reviewers and three products.
Both reviewers review product 1 and product 2, but product 0 is only reviewed by
reviewer 0.


Usage
-------

Graph Construction
^^^^^^^^^^^^^^^^^^^
This package provides a review graph class
:class:`fraudar.ReviewGraph <fraudar.graph.ReviewGraph>`
which represents the above bipartite graph.
The constructor of this class takes two arguments:
the number of kinds of fraudulent patterns this algorithm assumes,
and a type of subroutine.
Currently, you can pick one from the following three functions as the type of
subroutine:

* :meth:`aveDegree <fraudar.export.greedy.aveDegree>` (default),
* :meth:`sqrtWeightedAveDegree <fraudar.export.greedy.sqrtWeightedAveDegree>`,
* :meth:`logWeightedAveDegree <fraudar.export.greedy.logWeightedAveDegree>`.

See :doc:`API references <modules/fraudar>` and
`the original article <http://www.andrew.cmu.edu/user/bhooi/papers/fraudar_kdd16.pdf>`_
for more information about the subroutines.

To construct a review graph instance with assuming :math:`n` kinds of fraudulent
patterns and using :meth:`aveDegree <fraudar.export.greedy.aveDegree>` as the
subroutine,

.. code-block:: python

  import fraudar
  graph = fraudar.ReviewGraph(n, fraudar.aveDegree)

The constructed graph object implements the
:ref:`graph interface <dataset-io:graph-interface>`.

After constructing a graph instance, you need to add reviewer nodes, product
nodes, and review edges.
Two methods, :meth:`new_reviewer() <fraudar.graph.ReviewGraph.new_reviewer>` and
:meth:`new_product() <fraudar.graph.ReviewGraph.new_product>`,
create a reviewer node and a product node, respectively.
Both methods take one argument `name` i.e. ID of the node.
This name must be unique in a graph.

Method :meth:`add_review() <fraudar.graph.ReviewGraph.add_review>` adds a review
to the graph.
It takes a reviewer object, a product object, and a rating score.
The reviewer object and the product object must be created by the above two
methods, and the rating score takes a float value in :math:`[0, 1]`.

For example, let us construct a review graph instance which represents the
bipartite graph example in the :ref:`Graph Model section<graph_model>`.
The graph construction code is

.. code-block:: python

  import fraudar

  # Construct a Review Graph instance.
  # In this example, we choose 1 as the `n`.
  n = 1
  graph = fraudar.ReviewGraph(n, fraudar.aveDegree)

  # Create reviewers and products.
  reviewers = [graph.new_reviewer("reviewer-{0}".format(i)) for i in range(2)]
  products = [graph.new_product("product-{0}".format(i)) for i in range(3)]

  # Add reviews.
  graph.add_review(reviewers[0], products[0], 0.2)
  graph.add_review(reviewers[0], products[1], 0.9)
  graph.add_review(reviewers[0], products[2], 0.6)
  graph.add_review(reviewers[1], products[0], 0.1)
  graph.add_review(reviewers[1], products[1], 0.7)


Analysis
^^^^^^^^^
Method :meth:`update()<fraudar.graph.ReviewGraph.update>` starts the
FRAUDAR algorithm.

.. code-block:: python

  # Run one iteration.
  graph.update()


Result
^^^^^^^^
Each reviewer has an anomalous score.
If the anomalous score of a reviewer is 1, the reviewer is classified
in `FRAUD`, otherwise `HONEST`.
Property :meth:`anomalous_score <fraudar.graph.Reviewer.anomalous_score>`
returns the anomalous score.

The :class:`ReviewGraph <fraudar.graph.ReviewGraph>` has
property :meth:`reviewers<fraudar.graph.ReviewGraph.reviewers>`,
which returns a collection of reviewers,
and you can list up `FRAUD` reviewer names by

.. code-block:: python

  for r in graph.reviewers:
    if r.anomalous_score == 1:
      print(r.name)

On the other hand, each product has a summarized rating score.
The summarized rating score of a product is the average of rating scores posted
to the product from `HONEST` reviewers.
Property :meth:`summary<fraud_eagle.graph.Product.summary>` returns the
summarized rating score.

The :class:`ReviewGraph<fraud_eagle.graph.ReviewGraph>` also has
property :meth:`products<fraud_eagle.graph.ReviewGraph.products>`,
which returns a collection of products,
and you can print summarized rating scores of all products by

.. code-block:: python

   for p in graph.products:
       print(p.name, p.summary)


Script
^^^^^^^
As the summary of the above usage, we make an executable script which takes
the parameter ``n`` as a command line option, and analyze the above graph.
Let us save the following script as ``analyze.py``.

.. code-block:: python

  #!/usr/bin/env python
  import click
  import fraudar

  @click.command()
  @click.argument("n", type=int)
  def analyze(n):
      graph = fraudar.ReviewGraph(n, fraudar.aveDegree)

      # Create reviewers and products.
      reviewers = [graph.new_reviewer("reviewer-{0}".format(i)) for i in range(2)]
      products = [graph.new_product("product-{0}".format(i)) for i in range(3)]

      # Add reviews.
      graph.add_review(reviewers[0], products[0], 0.2)
      graph.add_review(reviewers[0], products[1], 0.9)
      graph.add_review(reviewers[0], products[2], 0.6)
      graph.add_review(reviewers[1], products[0], 0.1)
      graph.add_review(reviewers[1], products[1], 0.7)

      # Run the algorithm.
      graph.update()

      # Print anomalous reviewers.
      print("Anomalous reviewers.")
      for r in graph.reviewers:
        if r.anomalous_score == 1:
          print(r.name)

      # Print summarized rating scores.
      print("Summaries.")
      for p in graph.products:
          print(p.name, p.summary)


  if __name__ == "__main__":
      analyze()

Note that, the above script uses `click <http://click.pocoo.org/>`_.
If you didn't install it, you need to run ``pip install click``.

Then, you can analyze the graph with a specific :math:`n`, for example 5,
run the script by

.. code-block:: bash

  ./analyze.py 5


Parameter tuning
^^^^^^^^^^^^^^^^^^
Basically, bigger :math:`n` produces a better result, too big :math:`n` causes
a worse result.
You need to find the best parameter :math:`n` to obtain the best result.
The best parameter is highly depended on the data you want to analyze.
You should run the algorithm many times.
:ref:`project:parallel_evaluation` may help to evaluation time.


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
