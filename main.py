# This script runs the solutions for all days of the Advent of Code 2020
import logging

from day1 import day1
from day2 import day2

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print("Solving Advent of Code 2021")
    day1 = day1.Day1Solution()
    day1.solve()
    day2 = day2.Day2Solution()
    day2.solve()
