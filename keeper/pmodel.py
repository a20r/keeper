
import collections
import time
import scipy.optimize as opt
import numpy as np
import inspect


class ParametricModel(object):

    def __init__(self, inp_size, models, **kwargs):
        self.inp = collections.deque(list(), inp_size)
        self.out = collections.deque(list(), inp_size)
        self.models = self.init_models(models)
        self.current_model = None
        self.new_data = False
        self.start_time = kwargs.get("start_time", time.time())

    def init_models(self, models):
        func_tuples = inspect.getmembers(models, inspect.isfunction)
        return [f for _, f in func_tuples]

    def get_in_out_arrays(self):
        return np.array(list(self.inp)), np.array(list(self.out))

    def get_ssr(self, popt, func):
        inp_array, out_array = self.get_in_out_arrays()
        residuals = out_array - func(inp_array, *popt)
        return sum(residuals ** 2)

    def select_model(self):
        inp_array, out_array = self.get_in_out_arrays()
        min_ssr = None
        min_model = None
        min_popt = None
        for model in self.models:
            try:
                popt, pcov = opt.curve_fit(model, inp_array, out_array)
            except RuntimeError:
                continue

            ssr = self.get_ssr(popt, model)
            if min_ssr is None or ssr < min_ssr:
                min_ssr = ssr
                min_popt = popt
                min_model = model

        print min_model.func_name

        return lambda t: min_model(t, *min_popt)

    def push(self, out, t=None):
        if t is None:
            self.inp.append(time.time() - self.start_time)
        else:
            self.inp.append(t)

        self.out.append(out)
        self.new_data = True

    def __call__(self, t):
        if self.new_data:
            self.current_model = self.select_model()
            self.new_data = False

        if self.current_model is None:
            raise NameError("Model not yet selected")

        return self.current_model(t)
