from src.rectangle import Rectangle


class Square(Rectangle):

    def __init__(self, a):
        self.name = "square"
        if a > 0:
            self.a = self.b = a
        else:
            raise ValueError("Square sides must be greater than 0.")
