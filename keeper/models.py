
import numpy as np


class SinModel(object):

    def __call__(self, t, a, b, c, d):
        return a * np.sin(b * t + c) + d

    def func(self):
        return self.__call__

    def get_str(self, *popt):
        return "{} * Sin({} * t + {}) + {}".format(*popt)


class EvenPolyModel(object):

    def __call__(self, t, a, b, c, d, e):
        return (
            a * np.power(t, 4) +
            b * np.power(t, 3) +
            c * np.power(t, 2) +
            d * t + e
        )

    def func(self):
        return self.__call__

    def get_str(self, *popt):
        return ("{0} * t ^ 4 + {1} * t ^ 3 + {2} *"
                "t ^ 2 + {3} * t + {4}").format(*popt)


class ExpModel(object):

    def __call__(self, t, a, b, c):
        return a * np.exp(t) + b

    def func(self):
        return self.__call__

    def get_str(self, *popt):
        return "{} * Exp(t) + {}".format(*popt)


class LogModel(object):

    def __call__(self, t, a, b, c):
        return a * np.log(t + b) + c

    def func(self):
        return self.__call__

    def get_str(self, *popt):
        return "{} * Log(t + {}) + {}".format(*popt)


class SquaredSinModel(object):

    def __call__(self, t, a, b, c, d):
        return a * np.sin(b * t + c) ** 2 + d

    def func(self):
        return self.__call__

    def get_str(self, *popt):
        return "{} * Sin({} * t + {}) ^ 2 + {}".format(*popt)


class PowerModel(object):

    def __call__(self, t, a, b, c, d):
        return a * np.power(t + b, c) + d

    def func(self):
        return self.__call__

    def get_str(self, *popt):
        return "{} * (t + {}) ^ {} + {}".format(*popt)
