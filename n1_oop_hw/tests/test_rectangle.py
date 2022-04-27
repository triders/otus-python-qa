import pytest
from n1_oop_hw.src.triangle import Triangle
from n1_oop_hw.src.rectangle import Rectangle
from n1_oop_hw.src.square import Square
from n1_oop_hw.src.circle import Circle


def test_rectangle_name():
    assert Rectangle(1, 2).name == "rectangle"


def test_rectangle_area_calculated_correctly():
    assert Rectangle(1, 1).get_area == 1
    assert Rectangle(3, 4).get_area == 12
    assert Rectangle(4.5, 6.9090901909101).get_area == 4.5 * 6.9090901909101


def test_rectangle_perimeter_calculated_correctly():
    assert Rectangle(1, 1).get_perimeter == 4
    assert Rectangle(3, 4).get_perimeter == 14
    assert Rectangle(4.5, 6.9090901909101).get_perimeter == 2 * (4.5 + 6.9090901909101)


def test_rectangles_area_sum_calculated_correctly():
    assert Rectangle(1, 1).add_area(Rectangle(3, 4)) == 13


def test_rectangle_and_other_figures_sum_calculated_correctly():
    assert Rectangle(3, 4).add_area(Square(2)) == 16
    assert Rectangle(3, 4).add_area(Circle(3)) == 12 + 28.274333882308138
    assert Rectangle(3, 4).add_area(Triangle(3, 4, 5)) == 18


@pytest.mark.xfail
def test_cannot_add_area_of_not_figure_object():
    assert Rectangle(3, 4).add_area(1)


@pytest.mark.xfail
def test_cannot_create_rectangle_with_3_sides():
    assert Rectangle(1, 2, 3)


@pytest.mark.xfail
def test_cannot_create_rectangle_with_negative_side():
    assert Rectangle(1, -2)


@pytest.mark.xfail
def test_cannot_create_rectangle_with_zero_length_side():
    assert Rectangle(0, 5)
