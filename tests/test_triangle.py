import pytest
from src.triangle import Triangle


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


@pytest.mark.xfail
def test_cannot_create_triangle_with_sum_of_two_sides_equal_to_third_side():
    assert Triangle(5, 5, 10)


@pytest.mark.xfail
def test_cannot_create_triangle_with_4_sides():
    assert Triangle(1, 2, 3, 4)


@pytest.mark.xfail
def test_cannot_create_triangle_with_negative_side():
    assert Triangle(1, 2, -2)


@pytest.mark.xfail
def test_cannot_create_triangle_with_zero_length_side():
    assert Triangle(0, 5, 5)
