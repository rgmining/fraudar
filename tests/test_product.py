#
#  test_product.py
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
import numpy as np
from numpy.testing import assert_almost_equal

from fraudar import ReviewGraph


def test_summary(review_graph: ReviewGraph) -> None:
    """Test summary property."""
    assert_almost_equal(
        review_graph.products[2].summary, np.mean(list(review_graph.reviews[review_graph.products[2]].values()))
    )

    review_graph.reviewers[0].anomalous_score = 1
    assert_almost_equal(
        review_graph.products[2].summary, review_graph.reviews[review_graph.products[2]][review_graph.reviewers[1]]
    )
