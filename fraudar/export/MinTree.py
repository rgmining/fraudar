#
#  MinTree.py
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
#  This file was originally made by Bryan Hooi et al,
#  and distributed under Apache License, Version 2.0.
#
# mypy: ignore-errors
import math


class MinTree:
    """
    A tree data structure which stores a list of degrees and can quickly retrieve the min degree element,
    or modify any of the degrees, each in logarithmic time. It works by creating a binary tree with the
    given elements in the leaves, where each internal node stores the min of its two children.
    """

    def __init__(self, degrees):
        self.height = int(math.ceil(math.log(len(degrees), 2)))
        self.numLeaves = 2**self.height
        self.numBranches = self.numLeaves - 1
        self.n = self.numBranches + self.numLeaves
        self.nodes = [float("inf")] * self.n
        for i in range(len(degrees)):
            self.nodes[self.numBranches + i] = degrees[i]
        for i in reversed(range(self.numBranches)):
            self.nodes[i] = min(self.nodes[2 * i + 1], self.nodes[2 * i + 2])

    # @profile
    def getMin(self):
        cur = 0
        for i in range(self.height):
            cur = (2 * cur + 1) if self.nodes[2 * cur + 1] <= self.nodes[2 * cur + 2] else (2 * cur + 2)
        # print "found min at %d: %d" % (cur, self.nodes[cur])
        return (cur - self.numBranches, self.nodes[cur])

    # @profile
    def changeVal(self, idx, delta):
        cur = self.numBranches + idx
        self.nodes[cur] += delta
        for i in range(self.height):
            cur = (cur - 1) // 2
            nextParent = min(self.nodes[2 * cur + 1], self.nodes[2 * cur + 2])
            if self.nodes[cur] == nextParent:
                break
            self.nodes[cur] = nextParent

    def dump(self):
        print(f"numLeaves: {self.numLeaves}, numBranches: {self.numBranches}, n: {self.n}, nodes: ")
        cur = 0
        for i in range(self.height + 1):
            for j in range(2**i):
                print(self.nodes[cur], end=" ")
                cur += 1
            print("")
