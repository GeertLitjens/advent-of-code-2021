import requests
import os
from typing import Any, Tuple
import logging
import time
from colorama import init, Fore, Back
import inspect
from pathlib import Path
import sys

from abc import ABC, abstractmethod

init(autoreset=True)
logging.addLevelName(25, "SUCCESS")


class ColorFormatter(logging.Formatter):
    # Change this dictionary to suit your coloring needs!
    COLORS = {
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED + Back.WHITE,
        "DEBUG": Fore.BLUE,
        "INFO": Fore.WHITE,
        "SUCCESS": Fore.GREEN,
        "CRITICAL": Fore.RED + Back.WHITE
    }

    def format(self, record):
        color = self.COLORS.get(record.levelname, "")
        if color:
            record.name = color + record.name
            record.levelname = color + record.levelname
            record.msg = color + record.msg
        return logging.Formatter.format(self, record)


class ColorLogger(logging.Logger):

    def __init__(self, name):
        logging.Logger.__init__(self, name)
        color_formatter = ColorFormatter("%(message)s")
        console = logging.StreamHandler()
        console.setFormatter(color_formatter)
        self.addHandler(console)


class Solution(ABC):

    def __init__(self, day: int = 1, year: int = 2021) -> None:
        init()
        self._day = day
        self._year = year
        self._solution_part1 = None
        self._solution_part2 = None
        self._user_agent = {"User-Agent": "advent-of-code-data v1.1.0"}
        self._session_token = {"session": os.environ["AOC_TOKEN"]}
        self._logger = logging.getLogger("aoclogger")

    def _get_input_data(self) -> str:
        input_url = f"https://adventofcode.com/{self._year}/day/{self._day}/input"
        response = requests.get(url=input_url, cookies=self._session_token, headers=self._user_agent)
        if response.ok:
            return response.text
        else:
            return ""

    @abstractmethod
    def _parse_data(self, input_data: str) -> Any:
        return input_data

    @abstractmethod
    def _solve_part1(self, parsed_data: Any) -> Any:
        return parsed_data

    @abstractmethod
    def _solve_part2(self, parsed_data: Any) -> Any:
        return parsed_data

    def solve(self, only_part1: bool = False) -> Tuple[Any, Any]:
        self._logger.info(f"Solving for day {self._day}")
        parse_start = time.time()
        parsed_data = self._parse_data(self._get_input_data())
        parse_end = time.time()
        self._logger.info(f"\tTime needed for parsing data: {parse_end - parse_start}s")
        part1_start = time.time()
        self._solution_part1 = self._solve_part1(parsed_data)
        part1_end = time.time()
        self._logger.info(f"\tSolution for part 1: {self._solution_part1}")
        self._logger.info(f"\tTime needed for part 1: {part1_end - part1_start}s")
        if only_part1:
            self._solution_part2 = None
        else:
            part2_start = time.time()
            self._solution_part2 = self._solve_part2(parsed_data)
            part2_end = time.time()
            self._logger.info(f"\tSolution for part 2: {self._solution_part2}")
            self._logger.info(f"\tTime needed for part 2: {part2_end - part2_start}s")
        return self._solution_part1, self._solution_part2

    def submit(self) -> None:
        answer_url = f"https://adventofcode.com/{self._year}/day/{self._day}/answer"
        if self._solution_part1:
            response = requests.post(
                url=answer_url,
                cookies=self._session_token,
                headers=self._user_agent,
                data={"level": 1, "answer": str(self._solution_part1)},
            )
            if response.ok:
                self._logger.debug("Response OK!")
                self._check_answer(response.text)
            else:
                self._logger.error("Failed ")
        if self._solution_part2:
            response = requests.post(
                url=answer_url,
                cookies=self._session_token,
                headers=self._user_agent,
                data={"level": 2, "answer": str(self._solution_part1)},
            )
            if response.ok:
                self._logger.debug("Response OK!")
                self._check_answer(response.text)
            else:
                self._logger.error("Failed ")

    def _check_answer(self, response_text: str) -> None:
        if "That's the right answer" in response_text:
            self._logger.log(25, "\tYou answered correctly!")
        elif "Did you already complete it" in response_text:
            self._logger.warning("\tYou completed this part already!")
        else:
            self._logger.warning("\tYou gave the wrong answer!")

    def generate_day_md(self) -> None:
        template_path = Path(__file__).parent / "../utils/template.md"
        with open(template_path, 'r') as file:
            template = file.read()
        day_readme_path = Path(__file__).parent / f"../day{self._day}/README.md"
        with open(day_readme_path, 'r') as file:
            day_text = file.readlines()
        day_text = "".join(["> " + line for line in day_text[1:]])
        page_title = f"Day {self._day}"
        page_description = f"Python solution to day {self._day}"
        aoc_parse_solution = " ".join([x.lstrip() for x in self._parse_data.__doc__.split("\n")])
        aoc_part1_solution = " ".join([x.lstrip() for x in self._solve_part1.__doc__.split("\n")])
        aoc_part2_solution = " ".join([x.lstrip() for x in self._solve_part2.__doc__.split("\n")])
        day_experience = sys.modules[self.__module__].__doc__
        aoc_part1_text, aoc_part2_text = day_text.split("> ### Part 2")
        aoc_parse_code = inspect.getsourcelines(self._parse_data)[0]
        aoc_parse_code = self._clean_code_for_md(aoc_parse_code)
        aoc_part1_code = inspect.getsourcelines(self._solve_part1)[0]
        aoc_part1_code = self._clean_code_for_md(aoc_part1_code)
        aoc_part2_code = inspect.getsourcelines(self._solve_part2)[0]
        aoc_part2_code = self._clean_code_for_md(aoc_part2_code)
        replace_dict = {"<page_title>": page_title, "<page_description>": page_description,
                        "<aoc_part1_solution>": aoc_part1_solution, "<aoc_parse_solution>": aoc_parse_solution,
                        "<aoc_part2_solution>": aoc_part2_solution, "<day_experience>": day_experience,
                        "<aoc_part1_text>": aoc_part1_text, "<aoc_part2_text>": aoc_part2_text,
                        "<aoc_parse_code>": aoc_parse_code, "<aoc_part1_code>": aoc_part1_code,
                        "<aoc_part2_code>": aoc_part2_code}
        for key, value in replace_dict.items():
            template = template.replace(key, value)
        out_path = Path(__file__).parent / f"../docs/days/day{self._day}.md"
        with open(out_path, 'w') as file:
            file.write(template)

    @staticmethod
    def _clean_code_for_md(snippet: list[str]) -> str:
        leading_whitespace = len(snippet[0]) - len(snippet[0].lstrip(" "))
        snippet = [line[leading_whitespace:] for line in snippet]
        first_line_comment = 0
        last_line_comment = 0
        for i, line in enumerate(snippet):
            if line.lstrip().startswith('"""') and first_line_comment == 0:
                first_line_comment = i
            elif line.lstrip().startswith('"""') and first_line_comment > 0:
                last_line_comment = i
                break
        del snippet[first_line_comment:last_line_comment + 1]
        return "".join(snippet).rstrip()
