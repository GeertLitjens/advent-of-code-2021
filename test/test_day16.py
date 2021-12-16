import pytest
from day16.solution import DaySolution


@pytest.fixture
def day_testdata():
    return "A0016C880162017C3686B18A3D4780"


def test_part1(day_testdata):
    sol = DaySolution()
    parsed_data = sol._parse_data(day_testdata)
    result = sol._solve_part1(parsed_data)
    assert result == 31


def test_part2(day_testdata):
    sol = DaySolution()
    parsed_data = sol._parse_data(day_testdata)
    result = sol._solve_part2(parsed_data)
    assert result == 1
