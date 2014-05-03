
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import unittest
import numpy as np
import math
import keeper
import time
import util


class PredictorTest(unittest.TestCase):

    def setUp(self):
        pnets = [
            keeper.ParametricNet(10, 1, 100),
            keeper.ParametricNet(10, 1, 100)
        ]

        self.pd = keeper.Predictor(*pnets)

    @util.log
    def test_sin_prediction(self):
        start_time = time.time()
        x = lambda t: 5 * (t - start_time)
        y = lambda t: -9.81 * 0.5 * math.pow(t - start_time, 2) + 100
        for i in xrange(1000):
            current_time = time.time()
            self.pd.push(x(current_time), y(current_time))
            print self.pd(1)


if __name__ == "__main__":
    unittest.main()

