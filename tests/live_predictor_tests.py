#!/usr/bin/env python2
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import unittest
import keeper
import pylab as plt
import numpy as np


class LivePredictorTests(unittest.TestCase):

    def setUp(self):
        self.num_iter = 1000
        self.min_depth = 600
        self.min_blob_size = 10000
        self.how_far = 20
        self.num_parts = 1000
        fitters = [
            keeper.ParametricModel(100, keeper.models, name="X"),
            keeper.ParametricModel(100, keeper.models, name="Y")
        ]

        self.positions = list()

        self.pd = keeper.Predictor(*fitters)


    def test_predictor(self):
        classifier = keeper.DepthClassifier(
            self.min_depth, min_blob_size=self.min_blob_size
        )
        drawer = keeper.KinectDrawer()
        tracker = keeper.KinectTracker(classifier, drawer)
        for i in xrange(self.num_iter):
            print self.pd
            tr_points = tracker.track()
            if len(tr_points) == 1:
                tr_point = tr_points[0]
                self.positions.append(tr_point)
                self.pd.push(640 - tr_point.x, 480 - tr_point.y)

            if len(self.pd) > 10:
                XS = list()
                YS = list()
                for t in np.linspace(0, self.how_far, self.num_parts):
                    ret_list = self.pd(t)
                    XS.append(ret_list[0])
                    YS.append(ret_list[1])

                PXS = list()
                PYS = list()
                for position in self.positions:
                    PXS.append(640 - position.x)
                    PYS.append(480 - position.y)

                for i, x in enumerate(XS):
                    if x > 640:
                        XS[i] = 640

                    if x < 0:
                        XS[i] = 0

                for i, y in enumerate(YS):
                    if y > 480:
                        YS[i] = 480

                    if y < 0:
                        YS[i] = 0

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

                plt.draw()
                plt.pause(0.001)


if __name__ == "__main__":
    unittest.main()


