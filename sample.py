#!/usr/bin/env python
#
# sample.py
#
# Copyright (c) 2016-2017 Junpei Kawamoto
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
# along with rgmining-fraudar. If not, see <http://www.gnu.org/licenses/>.
#
"""A simple sample script running FRAUDAR with a synthetic data set.

This script requires `rgmining-synthetic-dataset`.
To install that package, run

.. code-block:: shell

    $ pip install --upgrade rgmining-synthetic-dataset

"""
from __future__ import print_function, division
from os import path
import sys
import click
import synthetic  # pylint: disable=import-error

sys.path.append(path.join(path.dirname(__file__), "../"))
import fraudar  # pylint: disable=import-error, wrong-import-position


@click.command()
@click.argument("blocks", type=int)
def analyze(blocks):
    """Analyze a synthetic data set with a given number of blocks.

    Args:
      blocks: the number of blocks.
    """
    graph = fraudar.ReviewGraph(blocks)
    synthetic.load(graph)

    graph.update()

    detected = [r for r in graph.reviewers if r.anomalous_score]
    correct = [r for r in detected if "anomaly" in r.name]

    print(
        len(correct) / len(detected),
        len(correct) / synthetic.ANOMALOUS_REVIEWER_SIZE)


if __name__ == "__main__":
    analyze()  # pylint: disable=no-value-for-parameter
