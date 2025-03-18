#
#  graph.py
#
#  Copyright (c) 2016-2025 Junpei Kawamoto
#
#  This file is part of rgmining-fraudar.
#
#  rgmining-fraudar is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  rgmining-fraudar is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with rgmining-fraudar. If not, see <http://www.gnu.org/licenses/>.
#
"""Provide a review graph which runs Fraudar algorithm."""

import tempfile
from bisect import bisect_left
from collections import defaultdict
from typing import Any, Final, Protocol

import numpy as np

from fraudar.export import greedy
from fraudar.export.greedy import logWeightedAveDegree


class Node:
    """Node of the ReviewGraph.

    A node has a name and a link to the graph. It also implements
    :meth:`__hash__` function so that each node can be stored in
    dictionaries.

    Args:
      graph: graph object this node belongs to.
      name: name of this node.
    """

    graph: Final["ReviewGraph"]
    """The graph object this node belongs to."""
    name: Final[str]
    """Name of this node."""

    __slots__ = ("graph", "name")

    def __init__(self, graph: "ReviewGraph", name: str) -> None:
        """Construct a node instance.

        Args:
          graph: graph object this node belongs to.
          name: name of this node.
        """
        self.graph = graph
        self.name = name

    def __hash__(self) -> int:
        """Returns a hash value of this instance."""
        return 13 * hash(type(self)) + 17 * hash(self.name)

    def __lt__(self, other: "Node") -> bool:
        return self.name.__lt__(other.name)


class Reviewer(Node):
    """A node type representing a reviewer.

    Use :meth:`ReviewGraph.new_reviewer` to create a new reviewer object
    instead of using this constructor directory.

    Args:
      graph: graph object this reviewer belongs to.
      name: name of this reviewer.
    """

    anomalous_score: float
    """anomalous score of this reviewer."""

    __slots__ = ("anomalous_score",)

    def __init__(self, graph: "ReviewGraph", name: str, anomalous_score: float = 0) -> None:
        super().__init__(graph, name)
        self.anomalous_score = anomalous_score


class Product(Node):
    """A node type representing a product.

    Use :meth:`ReviewGraph.new_product` to create a new product object
    instead of using this constructor directory.

    Args:
      graph: graph object this product belongs to.
      name: name of this product.
    """

    __slots__ = ()

    @property
    def summary(self) -> float:
        """Summary of ratings given to this product."""
        reviewers = self.graph.reviews[self].keys()
        ratings = [self.graph.reviews[self][r] for r in reviewers]
        weights = [1 - r.anomalous_score for r in reviewers]
        if sum(weights) == 0:
            return float(np.mean(ratings))
        else:
            return float(np.average(ratings, weights=weights))


class _Writable(Protocol):
    def write(self, s: str, /) -> int: ...


class ReviewGraph:
    """ReviewGraph is a simple bipartite graph representing review relation.

    Args:
      blocks: how many blocks to be detected. (default: 1)
      algo: algorithm used in fraudar, chosen from
        :meth:`aveDegree <fraudar.export.greedy.aveDegree>`,
        :meth:`sqrtWeightedAveDegree <fraudar.export.greedy.sqrtWeightedAveDegree>`,
        and
        :meth:`logWeightedAveDegree <fraudar.export.greedy.logWeightedAveDegree>`.
        (default: logWeightedAveDegree)
    """

    reviewers: Final[list[Reviewer]]
    """Collection of reviewers."""
    products: Final[list[Product]]
    """Collection of products."""
    reviews: Final[defaultdict[Product, dict[Reviewer, float]]]
    """Collection of reviews.

    reviews is a dictionary of which key is a product and value is another
    dictionary of which key is a reviewer and value is a rating from the
    reviewer to the product.
    """
    _algo: Final[Any]
    _blocks: Final[int]

    def __init__(self, blocks: int = 1, algo: Any = logWeightedAveDegree) -> None:
        self.reviewers = []
        self.products = []
        self.reviews = defaultdict(dict)

        self._algo = algo
        self._blocks = blocks

    def new_reviewer(self, name: str) -> Reviewer:
        """Create a new reviewer.

        Args:
          name: name of the new reviewer.

        Returns:
          a new reviewer object.
        """
        r = Reviewer(self, name)
        self.reviewers.append(r)
        return r

    def new_product(self, name: str) -> Product:
        """Create a new product.

        Args:
          name: name of the new product.

        Returns:
          a new product object.
        """
        p = Product(self, name)
        self.products.append(p)
        return p

    def add_review(self, reviewer: Reviewer, product: Product, rating: float) -> float:
        """Add a review from a reviewer to a product.

        Args:
          reviewer: reviewer who posts the review.
          product: product which receives the review.
          rating: the review score.

        Returns:
          added review score.
        """
        self.reviews[product][reviewer] = rating
        return rating

    def update(self) -> float:
        """Update anomalous scores by running a greedy algorithm.

        Returns:
          0
        """
        with tempfile.NamedTemporaryFile(mode="w") as fp:
            # Store this graph to a temporal file.
            self._store_matrix(fp)
            fp.seek(0)

            # Run greedy algorithm.
            M = greedy.readData(fp.name)
            res = greedy.detectMultiple(M, self._algo, self._blocks)

            # Update anomalous scores.
            for block in res:
                for i in block[0][0]:
                    self.reviewers[i].anomalous_score = 1

        return 0

    def _store_matrix(self, fp: _Writable) -> None:
        """Store this graph as a sparse matrix format.

        Args:
          fp: file-like object where the matrix to be written.
        """
        self.reviewers.sort()
        self.products.sort()
        for p in self.reviews:
            j = bisect_left(self.products, p)
            for r in self.reviews[p]:
                i = bisect_left(self.reviewers, r)
                fp.write("{0} {1}\n".format(i, j))
