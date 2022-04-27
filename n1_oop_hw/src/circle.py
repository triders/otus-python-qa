import math
from n1_oop_hw.src.figure import Figure


class Circle(Figure):

    def __init__(self, r):
        self.name = "circle"
        if r > 0:
            self.r = r
        else:
            raise ValueError("Circle must have a radius greater than 0")

    @property
    def get_perimeter(self):
        return 2 * math.pi * self.r

    @property
    def get_area(self):
        return math.pi * self.r ** 2
