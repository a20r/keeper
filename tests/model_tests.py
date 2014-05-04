
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import unittest
import keeper
import util


class ModelTest(util.PredictorTest, unittest.TestCase):

    def setUp(self):
        fitters = [
            keeper.ParametricModel(100, keeper.models),
            keeper.ParametricModel(100, keeper.models)
        ]

        self.pd = keeper.Predictor(*fitters)


if __name__ == "__main__":
    unittest.main()

