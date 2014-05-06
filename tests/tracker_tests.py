#!/usr/bin/env python2
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import unittest
import keeper


class TrackerTests(unittest.TestCase):

    def test_tracker(self):
        classifier = keeper.DepthClassifier(600, min_blob_size=10000)
        drawer = keeper.KinectDrawer()
        tracker = keeper.KinectTracker(classifier, drawer)
        for i in xrange(1000):
            print tracker.track()


if __name__ == "__main__":
    unittest.main()


