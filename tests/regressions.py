
import numpy as np
import random


class Gravity(object):
    def x(self, t):
        return 5 * (t - self.start_time)

    def y(self, t):
        return -9.81 * 0.5 * np.power(t - self.start_time, 2) + 100


class Linear(object):
    def x(self, t):
        return (t - self.start_time)

    def y(self, t):
        return 3 * (t - self.start_time)


class Exp(object):
    def x(self, t):
        return (t - self.start_time)

    def y(self, t):
        return np.exp(t - self.start_time) + 10


class Sin(object):
    def x(self, t):
        return (t - self.start_time)

    def y(self, t):
        return 10 * np.sin(t - self.start_time)


class Circle(object):
    def x(self, t):
        return np.cos(t - self.start_time)

    def y(self, t):
        return np.sin(t - self.start_time)


class Log(object):
    def x(self, t):
        return 18 * (t - self.start_time) + 2

    def y(self, t):
        return 43 * np.log(t - self.start_time + 0.0001) + 9
