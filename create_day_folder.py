import argparse
import logging
import shutil
from pathlib import Path
from utils import ColorLogger

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run (a subset of) the solutions for the Advent of Code 2021')
    parser.add_argument('day', type=int, help="Create the folder and test for the provided day number")

    args = parser.parse_args()

    logging.setLoggerClass(ColorLogger)
    logger = logging.getLogger("aoclogger")
    logger.setLevel(logging.INFO)

    logger.info(f"Creating structure for day {args.day}")
    in_path = Path(__file__).parent / f"day_template"
    out_path = Path(__file__).parent / f"day{args.day}"
    out_test_path = Path(__file__).parent / f"day{args.day}/test_day_template.py"
    test_path = Path(__file__).parent / f"test/test_day{args.day}.py"

    shutil.copytree(in_path, out_path)
    shutil.move(out_test_path, test_path)
    logger.log(25, "Successfully created folder and tests")