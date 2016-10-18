from __future__ import absolute_import
from bisect import bisect_left
from collections import defaultdict
import tempfile

from fraudar.export import greedy

class _Node(object):
    """Node of the ReviewGraph.

    A node has a name and a link to the graph. It also implements __hash__
    function so that each node can be stored in dictionaries.

    Args:
      graph: graph object this node belongs to.
      name: name of this node.

    Attributes:
      graph: graph object this node belongs to.
      name: name of this node.
    """
    def __init__(self, graph, name):
        """Construct a node instance.

        Args:
          graph: graph object this node belongs to.
          name: name of this node.
        """
        self.graph = graph
        self.name = name

    def __hash__(self):
        """Returns a hash value of this instance.
        """
        return 13 * hash(type(self)) + 17 * hash(self.name)


class Reviewer(_Node):
    """A node type representing a reviewer.

    Args:
      graph: graph object this reviewer belongs to.
      name: name of this reviewer.

    Attributes:
      name: name of this reviewer.
      anomalous_score: anomalous score.
    """
    def __init__(self, graph, name, anomalous_score=0):
        super(Reviewer, self).__init__(graph, name)
        self.anomalous_score = anomalous_score


class Product(_Node):
    """A node type representing a product.

    Args:
      graph: graph object this product belongs to.
      name: name of this product.

    Attributes:
      name: name of this product.
      summary: summary of ratings given to this product.
    """
    def __init__(self, graph, name):
        super(Product, self).__init__(graph, name)
        self.summary = None


class ReviewGraph(object):
    """ReviewGraph is a simple bipartite graph representing review relation.

    Attributes:
      reviewers: collection of reviewers.
      products: collection of products.
      reviews: dictionaly of which key is a product and value is another
        dictionaly of which key is a product and value is a rating from the
        reviewer to the product.
    """

    def __init__(self):
        self.reviewers = []
        self.products = []
        self.reviews = defaultdict(dict)
        # how many blocks assumed.
        # detect function

    def new_reviewer(self, name, **_kwargs):
        """Create a new reviewer.

        Args:
          name: name of the new reviewer.

        Returns:
          a new reviewer object.
        """
        r = Reviewer(self, name)
        self.reviewers.append(r)
        return r

    def new_product(self, name):
        """Create a new product.

        Args:
          name: name of the new product.

        Returns:
          a new product object.
        """
        p = Product(self, name)
        self.products.append(p)
        return p

    def add_review(self, reviewer, product, rating):
        """Add a review from a reviewer to a product.

        Args:
          reviewer: reviewer who posts the review.
          product: product which receives the review.
          rating: the review score.

        Returns:
          added review score.
        """
        self.reviews[reviewer][product] = rating
        return rating

    def update(self):
        """Update anomalous scores by running a greedy algorithm.

        Returns:
          0
        """

        with tempfile.NamedTemporaryFile() as fp:

            # Store this graph to a tempfile.
            self._store_matrix(fp)
            fp.seek(0)

            # Run greedy algorithm.
            M = greedy.readData(fp.name)
            res = greedy.logWeightedAveDegree(M)

            # Update anomalous scores.
            for i in res[0][0]:
                self.reviewers[i].anomalous_score = 1

        return 0

    def _store_matrix(self, fp):
        """Store this graph as a sparse matrix format.

        Args:
          fp: file-like object where the matrix to be written.
        """
        for r in self.reviews:
            i = bisect_left(self.reviewers, r)
            for p in self.reviews[r]:
                j = bisect_left(self.products, p)
                fp.write("{0} {1}\n".format(i, j))
