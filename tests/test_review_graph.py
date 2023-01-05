#
#  test_review_graph.py
#
#  Copyright (c) 2016-2023 Junpei Kawamoto
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
from collections import defaultdict
from io import StringIO
from random import random

import pytest

from fraudar import ReviewGraph
from fraudar.graph import Product, Reviewer


def test_new_reviewer(review_graph: ReviewGraph) -> None:
    """Test new_reviewer method."""
    name = "test-reviewer"
    reviewer = review_graph.new_reviewer(name)
    assert reviewer.name == name
    assert reviewer in review_graph.reviewers


def test_new_product(review_graph: ReviewGraph) -> None:
    """Test new_product method."""
    name = "test-product"
    product = review_graph.new_product(name)
    assert product.name == name
    assert product in review_graph.products


def test_add_review() -> None:
    """Test add_review method."""
    graph = ReviewGraph()
    reviewers = [graph.new_reviewer(f"reviewer-{i}") for i in range(3)]
    products = [graph.new_product(f"product-{i}") for i in range(3)]
    reviews = defaultdict[Reviewer, dict[Product, float]](dict)

    for r in reviewers:
        for p in products:
            rating = random()
            reviews[r][p] = graph.add_review(r, p, rating)
            assert reviews[r][p] == rating
    for r in reviewers:
        for p in products:
            assert graph.reviews[p][r] == reviews[r][p]


def test_store_matrix() -> None:
    """Test store matrix method.

    This function creates a graph and makes a sample graph defiend as

    .. graphviz::

       digraph bipartite {
          graph [rankdir = LR];
          "reviewer-0";
          "reviewer-1";
          "product-0";
          "product-1";
          "product-2";
          "reviewer-0" -> "product-0";
          "reviewer-0" -> "product-1";
          "reviewer-0" -> "product-2";
          "reviewer-1" -> "product-1";
          "reviewer-1" -> "product-2";
       }

    """
    graph = ReviewGraph()
    reviewers = [graph.new_reviewer(f"reviewer-{i}") for i in range(2)]
    products = [graph.new_product(f"product-{i}") for i in range(3)]
    reviews = defaultdict[Reviewer, dict[Product, bool]](dict)
    for i, r in enumerate(reviewers):
        for p in products[i:]:
            graph.add_review(r, p, random())
            reviews[r][p] = True

    buf = StringIO()
    graph._store_matrix(buf)  # pylint: disable=protected-access

    found = False
    for line in buf.getvalue().split("\n"):
        if not line:
            break
        i, j = [int(s.strip()) for s in line.split(" ")]
        r = graph.reviewers[i]
        p = graph.products[j]
        assert r in reviews
        assert p in reviews[r]
        found = True

    if not found:
        pytest.fail("_store_matrix returns empty file.")


def test_update(review_graph: ReviewGraph) -> None:
    """Test update method doesn't raise any errors."""
    review_graph.update()
