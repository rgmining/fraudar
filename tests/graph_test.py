#
# graph_test.py
#
# Copyright (c) 2016 Junpei Kawamoto
#
# This file is part of rgmining-fraudar.
#
# rgmining-fraudar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rgmining-fraudar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
"""Unit tests for fraudar package.
"""
from collections import defaultdict
import random
from StringIO import StringIO
import unittest

import numpy as np

from fraudar import graph


def reviewer_name(i):
    """Returns the i-th reviewer name.
    """
    return "reviewer-{0}".format(i)


def product_name(j):
    """Returns the j-th product name.
    """
    return "product-{0}".format(j)


class TestProduct(unittest.TestCase):
    """Test case for Product class.
    """
    def setUp(self):
        """Set up for a test.
        """
        self.graph = graph.ReviewGraph()

    def test_summary(self):
        """Test summary property.

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
        reviewers = [
            self.graph.new_reviewer(reviewer_name(i)) for i in range(2)
        ]
        products = [
            self.graph.new_product(product_name(i)) for i in range(3)
        ]
        for i, r in enumerate(reviewers):
            for p in products[i:]:
                self.graph.add_review(r, p, random.random())

        self.assertAlmostEqual(
            products[2].summary,
            np.mean(self.graph.reviews[products[2]].values()))

        reviewers[0].anomalous_score = 1
        self.assertAlmostEqual(
            products[2].summary,
            self.graph.reviews[products[2]][reviewers[1]])


class TestReviewGraph(unittest.TestCase):
    """Test case for ReviewGraph class.
    """

    def setUp(self):
        """Set up for a test.
        """
        self.graph = graph.ReviewGraph()

    def test_new_reviewer(self):
        """Test new_reviewer method.
        """
        name = "test-reviewer"
        reviewer = self.graph.new_reviewer(name)
        self.assertEqual(reviewer.name, name)
        self.assertIn(reviewer, self.graph.reviewers)

    def test_new_product(self):
        """Test new_product method.
        """
        name = "test-product"
        product = self.graph.new_product(name)
        self.assertEqual(product.name, name)
        self.assertIn(product, self.graph.products)

    def test_add_review(self):
        """Test add_review method.
        """
        reviewers = [
            self.graph.new_reviewer(reviewer_name(i)) for i in range(3)
        ]
        products = [
            self.graph.new_product(product_name(i)) for i in range(3)
        ]
        reviews = defaultdict(dict)

        for r in reviewers:
            for p in products:
                rating = random.random()
                reviews[r][p] = self.graph.add_review(r, p, rating)
                self.assertEqual(reviews[r][p], rating)
        for r in reviewers:
            for p in products:
                self.assertEqual(self.graph.reviews[p][r], reviews[r][p])

    def test_store_matrix(self):
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
        reviewers = [
            self.graph.new_reviewer(reviewer_name(i)) for i in range(2)
        ]
        products = [
            self.graph.new_product(product_name(i)) for i in range(3)
        ]
        reviews = defaultdict(dict)
        for i, r in enumerate(reviewers):
            for p in products[i:]:
                self.graph.add_review(r, p, random.random())
                reviews[r][p] = True

        buf = StringIO()
        self.graph._store_matrix(buf)  # pylint: disable=protected-access

        found = False
        for line in buf.getvalue().split("\n"):
            if not line:
                break
            i, j = [int(s.strip()) for s in line.split(" ")]
            r = self.graph.reviewers[i]
            p = self.graph.products[j]
            self.assertIn(r, reviews)
            self.assertIn(p, reviews[r])
            found = True

        if not found:
            self.fail("_store_matrix returns empty file.")

    def test_update(self):
        """Test update method doesn't raise any errors.

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
        reviewers = [
            self.graph.new_reviewer(reviewer_name(i)) for i in range(2)
        ]
        products = [
            self.graph.new_product(product_name(i)) for i in range(3)
        ]
        for i, r in enumerate(reviewers):
            for p in products[i:]:
                self.graph.add_review(r, p, random.random())
        self.graph.update()


if __name__ == "__main__":
    unittest.main()
