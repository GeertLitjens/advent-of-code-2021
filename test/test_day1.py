import unittest
from day1.day1 import part1, part2


class TestDay1(unittest.TestCase):

    test_data = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]

    def test_part1(self):
        result = part1(self.test_data)
        self.assertEqual(result, 7, msg="There should be 7 differences larger than the previous")

    def test_part2(self):
        result = part2(self.test_data)
        self.assertEqual(result, 5, msg="There should be 5 differences larger than the previous")

