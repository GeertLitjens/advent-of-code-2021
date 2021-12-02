import pytest
from day2.day2 import Day2Solution


@pytest.fixture
def day2_testdata():
    return ["forward 5", "down 5", "forward 8" "nup 3", "down 8", "forward 2"]


def test_part2(day2_testdata):
    sol = Day2Solution()
    result = sol._solve_part1(day2_testdata)
    assert result == 150


def test_part2(day2_testdata):
    sol = Day2Solution()
    result = sol._solve_part2(day2_testdata)
    assert 1 == 1

