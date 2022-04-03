import pytest
from src.triangle import Triangle
from src.rectangle import Rectangle
from src.square import Square
from src.circle import Circle


def test_square_name():
    assert Square(1).name == "square"


def test_square_area_calculated_correctly():
    assert Square(1).get_area == 1
    assert Square(3).get_area == 9
    assert Square(4.5).get_area == 4.5 ** 2


def test_square_perimeter_calculated_correctly():
    assert Square(1).get_perimeter == 4
    assert Square(3).get_perimeter == 12
    assert Square(4.5).get_perimeter == 4 * 4.5


def test_squares_area_sum_calculated_correctly():
    assert Square(1).add_area(Square(3)) == 10


def test_square_and_other_figures_sum_calculated_correctly():
    assert Square(3).add_area(Rectangle(2, 3)) == 15
    assert Square(3).add_area(Circle(3)) == 9 + 28.274333882308138
    assert Square(3).add_area(Triangle(3, 4, 5)) == 15


@pytest.mark.xfail
def test_cannot_add_area_of_not_figure_object():
    assert Square(3).add_area(1)


@pytest.mark.xfail
def test_cannot_create_square_with_2_sides():
    assert Square(1, 2)


@pytest.mark.xfail
def test_cannot_create_square_with_negative_side():
    assert Square(-2)


@pytest.mark.xfail
def test_cannot_create_square_with_zero_length_side():
    assert Square(0)
