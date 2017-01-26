#
# MainTree.py
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
# This file was originally made by Bryan Hooi et al,
# and distributed under Apache License, Version 2.0.
#

# FRAUDAR: Bounding Graph Fraud in the Face of Camouflage
# Authors: Bryan Hooi, Hyun Ah Song, Alex Beutel, Neil Shah, Kijung Shin, Christos Faloutsos
#
# This software is licensed under Apache License, Version 2.0 (the  "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Version: 1.0
# Date: Oct 3, 2016
# Main Contact: Bryan Hooi (bhooi@andrew.cmu.edu)

from __future__ import division, print_function
import math
import sys

class MinTree:
    """A tree data structure which stores a list of degrees and can quickly retrieve the min degree element,
    or modify any of the degrees, each in logarithmic time. It works by creating a binary tree with the
    given elements in the leaves, where each internal node stores the min of its two children.
    """
    def __init__(self, degrees):
        self.height = int(math.ceil(math.log(len(degrees), 2)))
        self.numLeaves = 2 ** self.height
        self.numBranches = self.numLeaves - 1
        self.n = self.numBranches + self.numLeaves
        self.nodes = [float('inf')] * self.n
        for i in range(len(degrees)):
            self.nodes[self.numBranches + i] = degrees[i]
        for i in reversed(range(self.numBranches)):
            self.nodes[i] = min(self.nodes[2 * i + 1], self.nodes[2 * i + 2])

    # @profile
    def getMin(self):
        cur = 0
        for _ in range(self.height):
            cur = (2 * cur + 1) if self.nodes[2 * cur + 1] <= self.nodes[2 * cur + 2] else (2 * cur + 2)
        # print "found min at %d: %d" % (cur, self.nodes[cur])
        return (cur - self.numBranches, self.nodes[cur])

    # @profile
    def changeVal(self, idx, delta):
        cur = self.numBranches + idx
        self.nodes[cur] += delta
        for _ in range(self.height):
            cur = (cur - 1) // 2
            nextParent = min(self.nodes[2 * cur + 1], self.nodes[2 * cur + 2])
            if self.nodes[cur] == nextParent:
                break
            self.nodes[cur] = nextParent

    def dump(self, output=sys.stdout):
        print("numLeaves: %d, numBranches: %d, n: %d, nodes: " % (self.numLeaves, self.numBranches, self.n), file=output)
        cur = 0
        for i in range(self.height + 1):
            for _ in range(2 ** i):
                print(self.nodes[cur], end="", file=output)
                cur += 1
            print('', file=output)
