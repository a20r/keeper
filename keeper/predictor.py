
import time
import math
import scipy.stats


class Predictor(object):

    def __init__(self, *fitters):
        self.num_dim = len(fitters)
        self.fitters = fitters
        self.start_time = None

    def push(self, *ps):
        if not len(ps) == self.num_dim:
            raise TypeError(
                "Dimension of input does not match internal dimension"
            )

        if self.start_time is None:
            self.start_time = time.time()

        current_time = time.time()

        for out, fitter in zip(ps, self.fitters):
            fitter.push(current_time - self.start_time, out)

        return self

    def clear(self):
        for fitter in self.fitters:
            fitter.clear()

        self.start_time = None
        return self

    def __call__(self, t):
        """
        Returns the result from the parametric predictors as well as a
        distance based Gaussian distribution
        """
        out = [fitter(t) for fitter in self.fitters]
        std = 20 * abs(t - time.time() + self.start_time)
        normal_dist = scipy.stats.norm(0, std)

        def p_pdf(*coords):
            if len(coords) != len(out):
                raise RuntimeError("Coordinate input and dimension mismatch")

            distance_squared = 0
            for c, o in zip(coords, out):
                distance_squared += pow(c - o, 2)

            distance = math.sqrt(distance_squared)

            return normal_dist.pdf(distance)

        return out, p_pdf

    def __str__(self):
        return "\n".join(str(fitter) for fitter in self.fitters)

    def __len__(self):
        return len(self.fitters[0].inp)
