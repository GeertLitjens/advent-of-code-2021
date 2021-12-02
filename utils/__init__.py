import requests
import os
from typing import Any, Tuple
import logging
from colorama import init, Fore, Back

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
        parsed_data = self._parse_data(self._get_input_data())
        self._solution_part1 = self._solve_part1(parsed_data)
        self._logger.info(f"\tSolution for part 1: {self._solution_part1}")
        if only_part1:
            self._solution_part2 = None
        else:
            self._solution_part2 = self._solve_part2(parsed_data)
            self._logger.info(f"\tSolution for part 2: {self._solution_part2}")
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