#!/usr/bin/env python2
import numpy as np


class Gravity(object):
    def x(self, t):
        return 5 * (t - self.start_time)

    def y(self, t):
        return -9.81 * 0.5 * np.power(t - self.start_time, 2) + 100 * t + 100


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


class LogSin(object):
    def x(self, t):
        return 100 * np.log(5 * (t - self.start_time)) + 1

    def y(self, t):
        return np.sin(t - self.start_time)


class SquaredSin(object):
    def x(self, t):
        return (t - self.start_time)

    def y(self, t):
        return np.sin(t - self.start_time) ** 2


class Log(object):
    def x(self, t):
        return 18 * (t - self.start_time) + 2

    def y(self, t):
        return 43 * np.log(t - self.start_time + 0.0001) + 9
