
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import unittest
import keeper
import pylab as plt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import time


class LiveUncertaintyTests(unittest.TestCase):

    def setUp(self):
        self.fig = plt.figure("Uncertainty Map")
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel("X Location")
        self.ax.set_ylabel("Y Location")
        self.x_step = 20
        self.y_step = 20
        self.x_min = 0
        self.y_min = 0
        self.x_max = 640
        self.y_max = 480
        self.x = np.arange(self.x_min, self.x_max, self.x_step)
        self.y = np.arange(self.y_min, self.y_max, self.y_step)
        self.X, self.Y = np.meshgrid(self.x, self.y)
        plt.ion()
        self.ax.set_xlim(self.x_min, self.x_max)
        self.ax.set_ylim(self.y_min, self.y_max)

        self.num_iter = 1000
        self.min_depth = 600
        self.min_blob_size = 10000
        self.how_far = 8
        self.num_parts = 10
        self.len_data = 20

        classifier = keeper.DepthClassifier(
            self.min_depth, min_blob_size=self.min_blob_size
        )
        drawer = keeper.KinectDrawer()
        self.tracker = keeper.KinectTracker(classifier, drawer)

        fitters = [
            keeper.ParametricModel(self.len_data, keeper.models, name="X"),
            keeper.ParametricModel(self.len_data, keeper.models, name="Y")
        ]

        self.pd = keeper.Predictor(*fitters)
        self.norm_list = list()

    def get_zs(self):
        zs = np.array(
            [
                max(f(x_i, y_i) for f in self.norm_list)
                for x_i, y_i in zip(np.ravel(self.X), np.ravel(self.Y))
            ]
        )
        return zs

    def update(self):
        try:
            self.graph.remove()
        except:
            pass

        zs = self.get_zs()
        Z = zs.reshape(self.X.shape)
        self.graph = self.ax.pcolormesh(self.X, self.Y, Z, cmap=cm.jet)
        plt.draw()
        plt.pause(0.0000001)

    def test_normal(self):
        for i in xrange(self.num_iter):
            try:
                tr_points = self.tracker.track()
                print self.pd

                if len(tr_points) == 0:
                    self.pd.clear()
                    continue

                tr_point = tr_points[0]
                self.pd.push(640 - tr_point.x, 480 - tr_point.y)

                self.norm_list = list()
                current_time = time.time()
                for t in np.linspace(
                    current_time - self.pd.start_time,
                    current_time - self.pd.start_time + self.how_far,
                    self.num_parts
                ):
                    _, norm = self.pd(t)
                    self.norm_list.append(norm)

                self.update()

            except Exception as e:
                print e


if __name__ == "__main__":
    unittest.main()

