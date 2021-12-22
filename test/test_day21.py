import pytest
from day21.solution import DaySolution


@pytest.fixture
def day_testdata():
    return """\
Player 1 starting position: 4
Player 2 starting position: 8\
"""


def test_part1(day_testdata):
    sol = DaySolution()
    parsed_data = sol._parse_data(day_testdata)
    result = sol._solve_part1(parsed_data)
    assert result == 739785


def test_part2(day_testdata):
    sol = DaySolution()
    parsed_data = sol._parse_data(day_testdata)
    result = sol._solve_part2(parsed_data)
    assert result == 444356092776315
