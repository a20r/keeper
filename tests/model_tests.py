#!/usr/bin/env python2
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import unittest
import keeper
import predictor_template as pt
import regressions as reg


class ModelTest(pt.PredictorTest):

    def setUp(self):
        fitters = [
            keeper.ParametricModel(100, keeper.models, name="X"),
            keeper.ParametricModel(100, keeper.models, name="Y")
        ]

        self.pd = keeper.Predictor(*fitters)


class ModelGravityTest(ModelTest, unittest.TestCase, reg.Gravity):
    pass


class ModelLinearTest(ModelTest, unittest.TestCase, reg.Linear):
    pass


class ModelExpTest(ModelTest, unittest.TestCase, reg.Exp):
    pass


class ModelSinTest(ModelTest, unittest.TestCase, reg.Sin):
    pass


class ModelLogTest(ModelTest, unittest.TestCase, reg.Log):
    pass


class ModelCircleTest(ModelTest, unittest.TestCase, reg.Circle):
    pass


if __name__ == "__main__":
    unittest.main()

