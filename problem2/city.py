class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, city):
        return abs(self.x - city.x) + abs(self.y - city.y)