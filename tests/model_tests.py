
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import unittest
import keeper
import predictor_template as pt


class ModelTest(pt.PredictorTest, unittest.TestCase):

    def setUp(self):
        fitters = [
            keeper.ParametricModel(100, keeper.models),
            keeper.ParametricModel(100, keeper.models)
        ]

        self.pd = keeper.Predictor(*fitters)


if __name__ == "__main__":
    unittest.main()

