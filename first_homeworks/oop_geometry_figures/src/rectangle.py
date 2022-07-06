from first_homeworks.oop_geometry_figures.src.figure import Figure


class Rectangle(Figure):

    def __init__(self, a, b):
        self.name = "rectangle"
        if a > 0 and b > 0:
            self.a = a
            self.b = b
        else:
            raise ValueError("All rectangle sides must be greater than 0.")

    @property
    def get_perimeter(self):
        return 2 * (self.a + self.b)

    @property
    def get_area(self):
        return self.a * self.b
