#
# __init__.py
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
"""A wrapper of Fraudar algorithm for the review graph mining project.

The Fraudar has been introduced by Bryan Hooi, *et al.* in
ACM SIGKDD 2016 Conference on Knowledge Discovery & Data Mining (KDD 2016).

http://www.kdd.org/kdd2016/subtopic/view/fraudar-bounding-graph-fraud-in-the-face-of-camouflage

"""
from graph import ReviewGraph
from fraudar.export.greedy import aveDegree
from fraudar.export.greedy import sqrtWeightedAveDegree
from fraudar.export.greedy import logWeightedAveDegree
