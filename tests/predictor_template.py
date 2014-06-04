
import time
import math
import pylab as plt
import numpy as np
import time


NUM_ITER = 40
NUM_PARTS = 50


class PredictorTest(object):

    def init_graph(self):
        t = np.linspace(
            self.start_time, self.start_time + self.how_far, NUM_PARTS
        )

        self.X = self.x(t)
        self.Y = self.y(t)
        plt.ion()
        self.truth_graph = plt.plot(self.X, self.Y, "b")[0]
        self.progression_graph = plt.plot(
            self.X[:0], self.Y[:0], "g", linewidth=5
        )[0]
        self.graph = plt.plot(self.X, self.Y, "r")[0]

    def test_prediction(self):
        self.start_time = time.time()
        self.how_far = 50

        self.init_graph()

        for i in xrange(NUM_ITER):
            current_time = time.time()
            self.pd.push(self.x(current_time), self.y(current_time))

            if i > 10:
                print self.pd
                XS = list()
                YS = list()
                for t in np.linspace(0, self.how_far, NUM_PARTS):
                    ret_list, _ = self.pd(t)
                    XS.append(ret_list[0])
                    YS.append(ret_list[1])

                progression = int(
                    NUM_PARTS * (current_time - self.start_time) /
                    (self.how_far)
                )

                self.graph.set_xdata(XS)
                self.graph.set_ydata(YS)
                self.progression_graph.set_xdata(self.X[:progression])
                self.progression_graph.set_ydata(self.Y[:progression])
                plt.draw()
                time.sleep(1)

        plt.clf()
