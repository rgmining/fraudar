#
#  conftest.py
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
from random import random

import pytest

from fraudar import ReviewGraph


@pytest.fixture
def review_graph() -> ReviewGraph:
    """Returns a sample review graph.

    This function creates a graph and makes a sample graph defined as

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
    g = ReviewGraph()
    for i in range(2):
        g.new_reviewer(f"reviewer-{i}")
    for j in range(3):
        g.new_product(f"product-{j}")
    for i, r in enumerate(g.reviewers):
        for p in g.products[i:]:
            g.add_review(r, p, random())
    return g
