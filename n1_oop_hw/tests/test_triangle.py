import pytest
from n1_oop_hw.src.triangle import Triangle
from n1_oop_hw.src.rectangle import Rectangle
from n1_oop_hw.src.square import Square
from n1_oop_hw.src.circle import Circle


def test_triangle_name():
    assert Triangle(3, 4, 5).name == "triangle"


def test_triangle_area_calculated_correctly():
    assert Triangle(1, 1, 1).get_area == 0.4330127018922193
    assert Triangle(3, 4, 5).get_area == 6
    assert Triangle(4.5, 5.111111111, 6.9090901909101).get_area == 11.494957492100871


def test_triangle_perimeter_calculated_correctly():
    assert Triangle(1, 1, 1).get_perimeter == 3
    assert Triangle(3, 4, 5).get_perimeter == 12
    assert Triangle(4.5, 5.111111111, 6.9090901909101).get_perimeter == 16.5202013019101


def test_triangles_area_sum_calculated_correctly():
    assert Triangle(1, 1, 1).add_area(Triangle(3, 4, 5)) == 6.4330127018922193


def test_triangle_and_other_figures_sum_calculated_correctly():
    assert Triangle(3, 4, 5).add_area(Rectangle(2, 3)) == 12
    assert Triangle(3, 4, 5).add_area(Square(2)) == 10
    assert Triangle(3, 4, 5).add_area(Circle(3)) == 28.274333882308138 + 6


@pytest.mark.xfail
def test_cannot_add_area_of_not_figure_object():
    assert Triangle(3, 4, 5).add_area(1)


@pytest.mark.xfail
def test_cannot_create_triangle_with_sum_of_two_sides_equal_to_third_side():
    assert Triangle(5, 5, 10)


@pytest.mark.xfail
def test_cannot_create_triangle_with_sum_of_two_sides_less_than_third_side():
    assert Triangle(5, 5, 11)


@pytest.mark.xfail
def test_cannot_create_triangle_with_4_sides():
    assert Triangle(1, 2, 3, 4)


@pytest.mark.xfail
def test_cannot_create_triangle_with_negative_side():
    assert Triangle(1, 2, -2)


@pytest.mark.xfail
def test_cannot_create_triangle_with_zero_length_side():
    assert Triangle(0, 5, 5)
