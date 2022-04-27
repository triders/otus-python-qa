import math
from n1_oop_hw.src.figure import Figure


class Triangle(Figure):

    def __init__(self, a, b, c):
        self.name = "triangle"
        if (a + b > c) and (a + c > b) and (c + b > a) and a > 0 and b > 0 and c > 0:
            self.a = a
            self.b = b
            self.c = c
        else:
            raise ValueError("Some of triangle parameters are invalid")

    @property
    def get_perimeter(self):
        return self.a + self.b + self.c

    @property
    def get_area(self):
        s = self.get_perimeter / 2
        return math.sqrt((s * (s - self.a) * (s - self.b) * (s - self.c)))
