
import math
import random


class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_x(self, x):
        self.x = x
        return self

    def set_y(self, y):
        self.y = y
        return self

    def dist_to(self, other_point):
        return math.sqrt(
            pow(self.x - other_point.x, 2) +
            pow(self.y - other_point.y, 2)
        )

    def to_unit_vector(self):
        mag = self.dist_to(Point(0, 0))

        if mag == 0:
            return Point(0, 0)
        else:
            return Point(self.x / mag, self.y / mag)

    def to_list(self):
        return [self.x, self.y]

    def __str__(self):
        return "X: {0}, Y: {1}".format(self.x, self.y)

    def __repr__(self):
        return "Point({0}, {1})".format(self.x, self.y)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, val):
        try:
            return val.x == self.x and val.y == self.y
        except:
            return False


def get_random_point(width, height):
    x = random.randint(0, width)
    y = random.randint(0, height)

    return Point(x, y)
