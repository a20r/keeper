
import neurolab as nl
import collections
import time
import numpy as np


class ParametricNet(object):

    def __init__(self, num_hidden_units, num_outputs, inp_size, **kwargs):
        self.start_time = kwargs.get("start_time", time.time())
        self.max_time = kwargs.get("max_time", 100)
        self.input_bounds = [[0, self.max_time]]
        self.num_hidden_units = num_hidden_units
        self.num_outputs = num_outputs
        self.inp = collections.deque(list(), inp_size)
        self.out = collections.deque(list(), inp_size)
        self.net = nl.net.newff(
            *self.get_nl_params(), transf=[
                nl.trans.TanSig(), nl.trans.PureLin()
            ]
        )

        self.last_time_collected = 0
        self.collection_delay = 0.4

    def set_input_bounds(self, input_bounds):
        self.input_bounds = input_bounds
        return self

    def set_num_hidden_units(self, num_hidden_units):
        self.num_hidden_units = num_hidden_units
        return self

    def set_num_outputs(self, num_outputs):
        self.num_outputs = num_outputs

    def get_nl_params(self):
        return [self.input_bounds, [self.num_hidden_units, self.num_outputs]]

    def get_neural_network(self):
        inp = [[i] for i in list(self.inp)]
        out = [[o] for o in list(self.out)]

        self.net.train(
            inp, out,
            epochs=500, show=0, goal=0.02
        )

        return self.net

    def push(self, out, t=None):
        if time.time() - self.last_time_collected > self.collection_delay:

            if t is None:
                self.inp.append(time.time() - self.start_time)
            else:
                self.inp.append(t)

            self.out.append(out)
            self.get_neural_network()
            self.last_time_collected = time.time()

        return self

    def __call__(self, t):
        if self.net is None:
            raise NameError("Net is not yet defined")

        return self.net.sim([[t]])[0][0]

