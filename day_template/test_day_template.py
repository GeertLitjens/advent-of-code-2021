import pytest
from day<DAY_NUMBER>.solution import DaySolution


@pytest.fixture
def day_testdata():
    return ""


def test_part1(day_testdata):
    sol = DaySolution()
    parsed_data = sol._parse_data(day_testdata)
    result = sol._solve_part1(parsed_data)
    assert result == <TEST_ANSWER_1>


def test_part2(day_testdata):
    sol = DaySolution()
    parsed_data = sol._parse_data(day_testdata)
    result = sol._solve_part2(parsed_data)
    assert result == <TEST_ANSWER_2>
