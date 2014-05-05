
class Predictor(object):

    def __init__(self, *fitters):
        self.num_dim = len(fitters)
        self.fitters = fitters

    def push(self, *ps):
        if not len(ps) == self.num_dim:
            raise TypeError(
                "Dimension of input does not match internal dimension"
            )

        for out, fitter in zip(ps, self.fitters):
            fitter.push(out)

        return self

    def __call__(self, t):
        return [fitter(t) for fitter in self.fitters]

    def __str__(self):
        return "\n".join(str(fitter) for fitter in self.fitters)
