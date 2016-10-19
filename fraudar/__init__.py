"""A wrapper of Fraudar algorithm for the review graph mining project.

The Fraudar has been introduced by Bryan Hooi, *et al.* in
ACM SIGKDD 2016 Conference on Knowledge Discovery & Data Mining (KDD 2016).

http://www.kdd.org/kdd2016/subtopic/view/fraudar-bounding-graph-fraud-in-the-face-of-camouflage

"""
from graph import ReviewGraph
from fraudar.export.greedy import aveDegree
from fraudar.export.greedy import sqrtWeightedAveDegree
from fraudar.export.greedy import logWeightedAveDegree
