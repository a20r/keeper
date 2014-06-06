
class Chain(object):

    def __init__(self, nodes):
        self.nodes = nodes
        self.graph = self.init_graph(nodes)

    def init_graph(self, nodes):
        graph_dict = dict()
        for node in nodes:
            graph_dict[node] = dict((node, 1) for node in nodes)

        return graph_dict

    def add_transition(self, n_1, n_2):
        self.graph[n_1][n_2] += 1
        return self

    def get_total_weight(self, node):
        w_sum = 0
        neighbours = self.graph[node]
        for _, n_w in neighbours.iteritems():
            w_sum += n_w

        return w_sum

    def get_probability(self, n_1, n_2):
        if n_1 == n_2:
            return 1

        total_weight = self.get_total_weight(n_1)
        weight = self.get_weight(n_1, n_2)
        return float(weight) / float(total_weight)

    def get_weight(self, n_1, n_2):
        return self.graph[n_1][n_2]

    def set_weight(self, n_1, n_2, w):
        self.graph[n_1][n_2] = w
        return self

    def __setitem__(self, index, value):
        self.set_weight(index[0], index[1], value)

    def __getitem__(self, index):
        return self.get_weight(index[0], index[1])
