import pytest
from day3.day3 import DaySolution


@pytest.fixture
def day3_testdata():
    return '00100\n11110\n10110\n10111\n10101\n01111\n00111\n11100\n10000\n11001\n00010\n01010'


def test_part1(day3_testdata):
    sol = DaySolution()
    parsed_data = sol._parse_data(day3_testdata)
    result = sol._solve_part1(parsed_data)
    assert result == 198


def test_part2(day3_testdata):
    sol = DaySolution()
    parsed_data = sol._parse_data(day3_testdata)
    result = sol._solve_part2(parsed_data)
    assert result == 230
