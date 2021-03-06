import pytest
from day7.solution import DaySolution


@pytest.fixture
def day_testdata():
    return "16,1,2,0,4,2,7,1,2,14"


def test_part1(day_testdata):
    sol = DaySolution()
    parsed_data = sol._parse_data(day_testdata)
    result = sol._solve_part1(parsed_data)
    assert result == 37


def test_part2(day_testdata):
    sol = DaySolution()
    parsed_data = sol._parse_data(day_testdata)
    result = sol._solve_part2(parsed_data)
    assert result == 168
