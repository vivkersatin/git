import pytest
from add_numbers import add

@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0)
])
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected

