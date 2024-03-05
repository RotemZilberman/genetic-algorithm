import numpy as np


class City:
    def __init__(self, x, y, distance_matrix="euclidean"):
        self.x = x
        self.y = y
        self.distance_matrix = distance_matrix

    def distance(self, city):
        if self.distance_matrix == "euclidean":
            return np.sqrt((self.x - city.x) ** 2 + (self.y - city.y) ** 2)
        else:
            return abs(self.x - city.x) + abs(self.y - city.y)
