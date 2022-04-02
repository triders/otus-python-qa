import math
from src.figure import Figure


class Circle(Figure):

    def __init__(self, r):
        self.name = "circle"
        if r > 0:
            self.r = r
        else:
            raise ValueError("Some of triangle parameters are invalid")

    @property
    def get_perimeter(self):
        return 2 * math.pi * self.r

    @property
    def get_area(self):
        return math.pi * self.r ** 2
