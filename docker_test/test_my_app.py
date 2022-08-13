import pytest
from my_app import double_sum_app


@pytest.mark.parametrize("num1, num2", [(i, i+1) for i in range(10)])
def test_my_app(num1, num2):
    assert double_sum_app(num1, num2) == 2 * (num1 + num2)
