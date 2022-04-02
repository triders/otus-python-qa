import math
from src.figure import Figure


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


if __name__ == "__main__":
    print(Triangle(1, 1, 1).get_perimeter)
    print(Triangle(3, 4, 5).get_perimeter)
    print(Triangle(4.5, 5.111111111, 6.9090901909101).get_perimeter)
    print(Triangle(1, 1000, 1000).get_perimeter)