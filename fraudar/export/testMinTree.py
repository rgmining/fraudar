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

# mypy: ignore-errors
from .MinTree import MinTree


def main():
    T = MinTree([1, 4, 2, 5, 3])
    T.dump()
    T.popMin()
    T.dump()
    T.popMin()
    T.dump()
    T.changeVal(4, 3)
    T.dump()
    T.popMin()
    T.dump()
    T.popMin()
    T.dump()
    T.changeVal(4, 10)
    T.dump()
    T.popMin()
    T.dump()

    # T = SamplingTree([10, 40, 12, 50, 30], 1)
    # T.dump()
    # T.sample()
    # T.dump()
    # T.sample()
    # T.dump()
    # T.changeVal(3, 3)
    # T.dump()
    # T.sample()
    # T.dump()
    # T.sample()
    # T.dump()
    # T.changeVal(4, 10)
    # T.dump()
    # T.sample()
    # T.dump()


if __name__ == "__main__":
    main()
