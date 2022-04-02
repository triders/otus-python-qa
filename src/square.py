from src.rectangle import Rectangle


class Square(Rectangle):

    def __init__(self, a, b=None):
        self.name = "square"
        if a > 0:
            self.a = self.b = a
        else:
            raise ValueError("Some of triangle parameters are invalid")
