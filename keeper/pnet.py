
import neurolab as nl
import collections
import time


class ParametricNet(object):

    def __init__(self, input_bounds, num_hidden_units, num_outputs, inp_size):
        self.input_bounds = input_bounds
        self.num_hidden_units = num_hidden_units
        self.num_outputs = num_outputs
        self.inp = collections.deque(list(), inp_size)
        self.out = collections.deque(list(), inp_size)
        self.net = None

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
        net = nl.net.newff(*self.get_nl_params())
        net.train(
            list(self.inp), list(self.out),
            epochs=500, show=100, goal=0.02
        )

        return net

    def push(self, out, t=None):
        if t is None:
            self.inp.append(time.time())
        else:
            self.inp.append(t)

        self.out.append(out)
        self.net = self.get_neural_network()

        return self

    def __call__(self, t):
        if self.net is None:
            raise NameError("Net is not yet defined")

        return self.net.sim([t])[0]

