import pytest
from day1.solution import DaySolution


@pytest.fixture
def day1_testdata():
    return [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]


def test_part1(day1_testdata):
    sol = DaySolution()
    result = sol._solve_part1(day1_testdata)
    assert result == 7


def test_part2(day1_testdata):
    sol = DaySolution();
    result = sol._solve_part2(day1_testdata)
    assert result == 5

