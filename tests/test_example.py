from app.example_for_test import Calculator
import pytest
from contextlib import nullcontext as does_not_raise


class TestCalculator:
    @pytest.mark.parametrize(
        ("x", "y", "res", 'expectation'),
        [
            (5, -1, -5, does_not_raise()),
            (10, 2, 5, does_not_raise()),
            (1, 2, 0.5, does_not_raise()),
            (1, 0, None, pytest.raises(ZeroDivisionError)),
        ]
    )
    def test_division(self, x, y, res, expectation):
        with expectation:
            assert Calculator().divine(x, y) == res

    @pytest.mark.parametrize(
        ("x", "y", "res", 'expectation'),
        [
            (5, -1, 4, does_not_raise()),
            (10, 2, 12, does_not_raise()),
            (1, 2, 3, does_not_raise()),
            (1, "2", 3, pytest.raises(TypeError)),
            (1, 0, 1, does_not_raise()),
        ]
    )
    def test_add(self, x, y, res, expectation):
        with expectation:
            assert Calculator().add(x, y) == res
