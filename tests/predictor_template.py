
import time
import math
import pylab as plt
import numpy as np
import util


NUM_ITER = 150


class PredictorTest(object):

    def init_graph(self):
        t = np.linspace(
            self.start_time, self.start_time + self.how_far, 100
        )

        self.X = self.x(t)
        self.Y = self.y(t)
        plt.ion()
        self.graph = plt.plot(self.X, self.Y, "r")[0]

    def test_prediction(self):
        self.start_time = time.time()
        self.how_far = 100

        self.init_graph()

        for i in xrange(NUM_ITER):
            current_time = time.time()
            self.pd.push(self.x(current_time), self.y(current_time))

            if i > 10:
                XS = list()
                YS = list()
                for t in np.linspace(0, self.how_far, 100):
                    ret_list = self.pd(t)
                    XS.append(ret_list[0])
                    YS.append(ret_list[1])

                progression = int(
                    100 * (current_time - self.start_time) /
                    (self.how_far)
                )

                self.truth_graph = plt.plot(
                    self.X[:progression], self.Y[:progression], "g"
                )[0]
                self.graph.set_xdata(XS)
                self.graph.set_ydata(YS)
                plt.draw()
                plt.pause(0.01)

        plt.clf()
