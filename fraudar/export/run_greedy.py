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


# runs the greedy algorithm. first argument is path to data file. second argument is name to save
# pickle containing results.
import time
start_time = time.time()
from greedy import *
import sys
M = readData(sys.argv[1])
print "finished reading data: shape = ", M.shape, " @ ", time.time() - start_time

# (m, n) = (500, 500)
# M = M[0:m, 0:n]
# M[0:20, 0:20] = 1
# M2 = M.toarray().astype(int)
# print np.transpose(np.nonzero(M2))
# np.savetxt('example.txt', np.transpose(np.nonzero(M2)), fmt='%d')

# M, rowFilter, colFilter = subsetAboveDegree(M, int(sys.argv[3]), int(sys.argv[4]))
# filter_name = "output/%s_%s_%s_filter.pickle" % (sys.argv[2], sys.argv[3], sys.argv[4])
# pickle.dump((rowFilter, colFilter), open(filter_name, "wb" ))
# print "finished subsetting: shape = ", M.shape, " @ ", time.time() - start_time
# subset_filepath = '%s_%s_%s.txt' % (sys.argv[2], sys.argv[3], sys.argv[4])
# pickle.dump(M, open(subset_filepath, "wb"))
# np.savetxt(subset_filepath, M.nonzero().transpose(), fmt='%i')

print "finished writing data", " @ ", time.time() - start_time
lwRes = logWeightedAveDegree(M)
print lwRes
np.savetxt("%s.rows" % (sys.argv[2], ), np.array(list(lwRes[0][0])), fmt='%d')
np.savetxt("%s.cols" % (sys.argv[2], ), np.array(list(lwRes[0][1])), fmt='%d')
print "score obtained is ", lwRes[1]
print "done @ ", time.time() - start_time
