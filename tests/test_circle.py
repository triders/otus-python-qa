import pytest
from src.circle import Circle
from src.triangle import Triangle
from src.rectangle import Rectangle
from src.square import Square


def test_circle_name():
    assert Circle(1).name == "circle"


def test_circle_area_calculated_correctly():
    assert Circle(1).get_area == 3.141592653589793
    assert Circle(3).get_area == 28.274333882308138
    assert Circle(4.5).get_area == 63.61725123519331


def test_circle_perimeter_calculated_correctly():
    assert Circle(1).get_perimeter == 6.283185307179586
    assert Circle(3).get_perimeter == 18.84955592153876
    assert Circle(4.5).get_perimeter == 28.274333882308138


def test_circles_area_sum_calculated_correctly():
    assert Circle(1).add_area(Circle(3)) == 3.141592653589793 + 28.274333882308138


def test_circle_and_other_figures_sum_calculated_correctly():
    assert Circle(3).add_area(Rectangle(2, 3)) == 28.274333882308138 + 6
    assert Circle(3).add_area(Square(2)) == 28.274333882308138 + 4
    assert Circle(3).add_area(Triangle(3, 4, 5)) == 28.274333882308138 + 6


@pytest.mark.xfail
def test_cannot_add_area_of_not_figure_object():
    assert Circle(3).add_area(1)


@pytest.mark.xfail
def test_cannot_create_circle_with_2_radius():
    assert Circle(1, 2)


@pytest.mark.xfail
def test_cannot_create_circle_with_negative_radius():
    assert Circle(-2)


@pytest.mark.xfail
def test_cannot_create_circle_with_zero_radius():
    assert Circle(0)
