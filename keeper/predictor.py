

class Predictor(object):

    def __init__(self, *pnets):
        self.num_dim = len(pnets)
        self.pnets = pnets

    def push(self, *ps):
        if not len(ps) == self.num_dim:
            raise TypeError(
                "Dimension of input does not match internal dimension"
            )

        for out, net in zip(ps, self.pnets):
            net.push(out)

        return self

    def __call__(self, t):
        return [net(t) for net in self.pnets]
