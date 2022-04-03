class Figure:

    @property
    def get_perimeter(self):
        return None

    @property
    def get_area(self):
        return None

    def add_area(self, figure):
        if isinstance(figure, Figure):
            return self.get_area + figure.get_area
        else:
            raise ValueError("The given object is not an instance of 'Figure' class.")

