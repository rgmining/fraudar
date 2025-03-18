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
# Version: 1.1
# Date: June 12, 2018
# Main Contact: Bryan Hooi (bhooi@andrew.cmu.edu)
#
# mypy: ignore-errors

import sys

# Runs the greedy algorithm.
# Command line arguments: first argument is path to data file. Second argument is path to save output.
# Third argument (*optional*) is path where the node suspiciousness values are stored.
import time

import numpy as np

from fraudar.export.greedy import logWeightedAveDegree, readData


def main():
    start_time = time.time()
    M = readData(sys.argv[1])
    # The example data is a 500 x 500 matrix with an injected dense block among the first 20 nodes
    print("finished reading data: shape = %d, %d @ %d" % (M.shape[0], M.shape[1], time.time() - start_time))

    if len(sys.argv) > 3:  # node suspiciousness present
        print("using node suspiciousness")
        rowSusp = np.loadtxt("%s.rows" % (sys.argv[3],))
        colSusp = np.loadtxt("%s.cols" % (sys.argv[3],))
        lwRes = logWeightedAveDegree(M, (rowSusp, colSusp))
    else:
        lwRes = logWeightedAveDegree(M)

    print(lwRes)
    np.savetxt("%s.rows" % (sys.argv[2],), np.array(list(lwRes[0][0])), fmt="%d")
    np.savetxt("%s.cols" % (sys.argv[2],), np.array(list(lwRes[0][1])), fmt="%d")
    print("score obtained is %f" % (lwRes[1],))
    print("done @ %f" % (time.time() - start_time,))

    # When no node suspiciousness values are passed, we detect the injected block.
    # However, when adding large suspiciousness values to the first 10 rows and columns,
    # the new detected block becomes the first 10 rows and columns.
    # Intuitively, the first 10 rows and columns are now suspiciousness enough that it no longer becomes worth it
    # for the algorithm to include the remaining 10 rows and columns.


if __name__ == "__main__":
    main()
