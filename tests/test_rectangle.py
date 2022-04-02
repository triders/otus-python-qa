import pytest
from src.rectangle import Rectangle


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


@pytest.mark.xfail
def test_cannot_create_rectangle_with_3_sides():
    assert Rectangle(1, 2, 3)


@pytest.mark.xfail
def test_cannot_create_rectangle_with_negative_side():
    assert Rectangle(1, -2)


@pytest.mark.xfail
def test_cannot_create_rectangle_with_zero_length_side():
    assert Rectangle(0, 5)
