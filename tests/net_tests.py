
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import unittest
import keeper
import util


class NetTest(util.PredictorTest, unittest.TestCase):

    def setUp(self):
        fitters = [
            keeper.ParametricNet(10, 1, 10),
            keeper.ParametricNet(10, 1, 10)
        ]

        self.pd = keeper.Predictor(*fitters)


if __name__ == "__main__":
    unittest.main()

