import pytest
from day2.day2 import Day2Solution


@pytest.fixture
def day2_testdata():
    return "forward 5\ndown 5\nforward 8\nup 3\ndown 8\nforward 2"


def test_part1(day2_testdata):
    sol = Day2Solution()
    parsed_data = sol._parse_data(day2_testdata)
    result = sol._solve_part1(parsed_data)
    assert result == 150


def test_part2(day2_testdata):
    sol = Day2Solution()
    parsed_data = sol._parse_data(day2_testdata)
    result = sol._solve_part2(parsed_data)
    assert result == 900

