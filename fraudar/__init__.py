#
#  __init__.py
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
"""A wrapper of Fraudar algorithm for the review graph mining project.

The Fraudar has been introduced by Bryan Hooi, *et al.* in
ACM SIGKDD 2016 Conference on Knowledge Discovery & Data Mining (KDD 2016).

This package exports :class:`ReviewGraph <graph.ReviewGraph>` class,
which implements interfaces expected in other APIs of
`Review Graph Mining project <https://rgmining.github.io/>`_,
and three sub algorithms used in FRAUDER:

* :meth:`aveDegree <export.greedy.aveDegree>` computes average degree on a matrix,
* :meth:`sqrtWeightedAveDegree <export.greedy.sqrtWeightedAveDegree>`
  computes square-weighted average degree on a matrix,
* :meth:`logWeightedAveDegree <export.greedy.logWeightedAveDegree>`
  computes logarithm-weighted average degree on a matrix.

:meth:`ReviewGraph <graph.ReviewGraph>` takes keyword argument ``algo`` to
be set the sub algorithm to be used.
"""

from typing import Final

from fraudar.__version__ import __version__
from fraudar.export.greedy import aveDegree, logWeightedAveDegree, sqrtWeightedAveDegree
from fraudar.graph import ReviewGraph

__all__: Final = (
    "ReviewGraph",
    "aveDegree",
    "sqrtWeightedAveDegree",
    "logWeightedAveDegree",
    "__version__",
)
