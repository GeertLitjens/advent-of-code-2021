# This script runs the solutions for all days of the Advent of Code 2021
import argparse
import logging
import os
import importlib
from utils import ColorLogger


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run (a subset of) the solutions for the Advent of Code 2021')
    parser.add_argument('token', type=str, help="Advent of Code session token to access your user's progress")
    parser.add_argument('-d', '--days', type=int, metavar='N',  nargs='*', default=[],
                        help="Run a specific set of days, default is all days")
    parser.add_argument('-p', '--part1', action="store_true", help="Only execute part 1 of the solutions")
    parser.add_argument('-s', '--submit', action="store_true", help="Submit answers to Advent of Code website")
    parser.add_argument('-w', '--write', action="store_true", help="Generate MD files for GitHub pages from code")
    parser.add_argument('-v', '--verbose', action="store_true", help="Increase verbosity for debug purposes")

    args = parser.parse_args()

    logging.setLoggerClass(ColorLogger)
    logger = logging.getLogger("aoclogger")
    if args.verbose:
        logger.setLevel(level=logging.DEBUG)
    else:
        logger.setLevel(level=logging.INFO)

    os.environ['AOC_TOKEN'] = args.token

    day_folders = [x for x in os.listdir(os.getcwd()) if "day" in x]
    if args.days:
        days = args.days
    else:
        days = sorted([int(x.replace('day', '')) for x in day_folders])

    logger.info("Started calculating solutions for days: " + str(days))
    for day_nr in days:
        day_module = importlib.import_module("day" + str(day_nr) + ".day" + str(day_nr))
        solution = day_module.DaySolution()
        solution.solve(args.part1)
        if args.submit:
            solution.submit()
        if args.write:
            solution.generate_day_md()
