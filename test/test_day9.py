import pytest
from day9.solution import DaySolution


@pytest.fixture
def day_testdata():
    return """\
2199943210
3987894921
9856789892
8767896789
9899965678"""


def test_part1(day_testdata):
    sol = DaySolution()
    parsed_data = sol._parse_data(day_testdata)
    result = sol._solve_part1(parsed_data)
    assert result == 15


def test_part2(day_testdata):
    sol = DaySolution()
    parsed_data = sol._parse_data(day_testdata)
    result = sol._solve_part2(parsed_data)
    assert result == 1134
