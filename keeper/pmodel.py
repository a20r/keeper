
import collections
import scipy.optimize as opt
import numpy as np
import inspect
import models
import random
import math


class ParametricModel(object):

    def __init__(self, inp_size, models, **kwargs):
        self.inp_size = inp_size
        self.inp = collections.deque(list(), inp_size)
        self.out = collections.deque(list(), inp_size)
        self.models = self.init_models(models)
        self.current_model = None
        self.new_data = False
        self.name = kwargs.get("name", "N/A")
        self.current_model_name = "N/A"
        self.test_size_const = 0.6
        self.num_test_lists = 6

    def init_models(self, models):
        class_tuples = inspect.getmembers(models, inspect.isclass)
        return [cls() for _, cls in class_tuples]

    def clear(self):
        self.inp = collections.deque(list(), self.inp_size)
        self.out = collections.deque(list(), self.inp_size)
        return self

    def get_in_out_arrays(self):
        return np.array(list(self.inp)), np.array(list(self.out))

    def get_ssr(self, popt, func):
        """
        Gets the squared sum of the residuals
        """

        inp_array, out_array = self.get_in_out_arrays()
        residuals = out_array - func(inp_array, *popt)
        return sum(residuals ** 2)

    def get_test_lists(self):
        inp_array, out_array = self.get_in_out_arrays()
        zipped_array = zip(inp_array, out_array)
        sample_size = int(math.ceil(len(self.inp) * self.test_size_const))
        test_lists = list()

        for _ in xrange(self.num_test_lists):
            t_list = random.sample(zipped_array, sample_size)
            test_lists.append(zip(*t_list))

        return test_lists

    def select_model(self):
        test_lists = self.get_test_lists()
        min_ssr = None
        min_model = None
        min_popt = None

        for t_inp_array, t_out_array in test_lists:
            for model in self.models:
                try:
                    popt, pcov = opt.curve_fit(
                        model.func(), t_inp_array, t_out_array
                    )
                except (RuntimeError, RuntimeWarning):
                    continue
                except TypeError:
                    raise Exception("Not enough data")

                ssr = self.get_ssr(popt, model)
                if min_ssr is None or ssr < min_ssr:
                    min_ssr = ssr
                    min_popt = popt
                    min_model = model

        self.current_model_name = min_model.get_str(*min_popt)
        return lambda t: min_model(t, *min_popt)

    def push(self, t, out):
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

    def __str__(self):
        return "{}(t) = {}".format(self.name, self.current_model_name)
