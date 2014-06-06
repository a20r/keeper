#!/usr/bin/env python2
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import unittest
import keeper
import pylab as plt
import numpy as np
import collections
import time
import traceback


class LivePredictorTests(unittest.TestCase):

    def setUp(self):
        self.num_iter = 1000
        self.min_depth = 600
        self.min_blob_size = 10000
        self.how_far = 5
        self.num_parts = 1000
        self.len_data = 20
        fitters = [
            keeper.ParametricModel(self.len_data, keeper.models, name="X"),
            keeper.ParametricModel(self.len_data, keeper.models, name="Y")
        ]

        self.positions = collections.deque(list(), self.len_data)

        self.pd = keeper.Predictor(*fitters)


    def test_predictor(self):
        classifier = keeper.DepthClassifier(
            self.min_depth, min_blob_size=self.min_blob_size
        )
        drawer = keeper.KinectDrawer()
        tracker = keeper.KinectTracker(classifier, drawer)
        for i in xrange(self.num_iter):
            try:
                tr_points = tracker.track()
                print self.pd

                if len(tr_points) == 0:
                    self.pd.clear()
                    self.positions = collections.deque(list(), self.len_data)
                    continue

                tr_point = tr_points[0]
                self.positions.append(tr_point)
                self.pd.push(640 - tr_point.x, 480 - tr_point.y)

                XS = list()
                YS = list()
                current_time = time.time()
                for t in np.linspace(
                    current_time - self.pd.start_time,
                    current_time - self.pd.start_time + self.how_far,
                    self.num_parts
                ):
                    ret_list = self.pd(t)
                    XS.append(ret_list[0])
                    YS.append(ret_list[1])

                PXS = list()
                PYS = list()
                for position in self.positions:
                    PXS.append(640 - position.x)
                    PYS.append(480 - position.y)

                try:
                    self.graph.set_xdata(XS)
                    self.graph.set_ydata(YS)
                except:
                    self.graph = plt.plot(XS, YS, "r")[0]

                try:
                    self.pgraph.set_xdata(PXS)
                    self.pgraph.set_ydata(PYS)
                except:
                    self.pgraph = plt.plot(PXS, PYS, "g")[0]

                plt.xlim(0, 640)
                plt.ylim(0, 480)

                plt.draw()
                plt.pause(0.001)
            except Exception as e:
                if str(e) != "Not enough data":
                    traceback.print_exc()
                    exit(1)


if __name__ == "__main__":
    unittest.main()


