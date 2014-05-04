
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import unittest
import keeper
import predictor_template as pt
import regressions as reg


class NetTest(pt.PredictorTest):

    def setUp(self):
        fitters = [
            keeper.ParametricNet(100, 1, 30),
            keeper.ParametricNet(100, 1, 30)
        ]

        self.pd = keeper.Predictor(*fitters)


class NetGravityTest(NetTest, unittest.TestCase, reg.Gravity):
    pass


class NetLinearTest(NetTest, unittest.TestCase, reg.Linear):
    pass


class NetExpTest(NetTest, unittest.TestCase, reg.Exp):
    pass


class NetSinTest(NetTest, unittest.TestCase, reg.Sin):
    pass


if __name__ == "__main__":
    unittest.main()

