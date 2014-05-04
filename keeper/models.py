
import numpy as np


def sin_model(t, a, b, c):
    return a * np.sin(b * t) + c


def exp_model(t, a, b, c):
    return a * np.exp(b * t) + c


def even_poly_model(t, a, b, c, d, e):
    return (
        a * np.power(t, 4) +
        b * np.power(t, 3) +
        c * np.power(t, 2) +
        d * t + e
    )

def odd_poly_model(t, a, b, c, d, e, f):
    return (
        a * np.power(t, 5) +
        b * np.power(t, 4) +
        c * np.power(t, 3) +
        d * np.power(t, 2) +
        e * t + f
    )
