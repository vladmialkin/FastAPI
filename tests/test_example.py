from app.example_for_test import Calculator
import pytest


@pytest.mark.parametrize(
    ("x", "y", "res"),
    [
        (5, -1, -5),
        (10, 2, 5),
        (1, 2, 0.5),
    ]
)
def test_division(x, y, res):
    assert Calculator().divine(x, y) == res


@pytest.mark.parametrize(
    ("x", "y", "res"),
    [
        (5, -1, 4),
        (10, 2, 12),
        (1, 2, 3),
    ]
)
def test_add(x, y, res):
    assert Calculator().add(x, y) == res


