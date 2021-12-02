import requests
import os
from typing import Any, Tuple
import logging

from abc import ABC, abstractmethod


class Solution(ABC):

    _user_agent = {"User-Agent": "advent-of-code-data v1.1.0"}
    _session_token = {"session": os.environ["AOC_TOKEN"]}

    def __init__(self, day: int = 1, year: int = 2021) -> None:
        self._day = day
        self._year = year
        self._solution_part1 = None
        self._solution_part2 = None

    def _get_input_data(self) -> str:
        input_url = f"https://adventofcode.com/{self._year}/day/{self._day}/input"
        response = requests.get(url=input_url, cookies=Solution._session_token, headers=Solution._user_agent)
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

    def solve(self) -> Tuple[Any, Any]:
        logging.info(f"Solving for Day {self._day}")
        parsed_data = self._parse_data(self._get_input_data())
        self._solution_part1 = self._solve_part1(parsed_data)
        self._solution_part2 = self._solve_part2(parsed_data)
        logging.info(f"Solution for Part 1: {self._solution_part1}")
        logging.info(f"Solution for Part 2: {self._solution_part2}")
        return self._solution_part1, self._solution_part2

    def submit(self) -> None:
        answer_url = f"https://adventofcode.com/{self._year}/day/{self._day}/answer"
        if self._solution_part1:
            response = requests.post(
                url=answer_url,
                cookies=Solution._session_token,
                headers=Solution._user_agent,
                data={"level": 1, "answer": str(self._solution_part1)},
            )
            if response.ok:
                logging.info("Response OK!")
                logging.info(response.text)
            else:
                logging.info("Failed ")
        if self._solution_part2:
            response = requests.post(
                url=answer_url,
                cookies=Solution._session_token,
                headers=Solution._user_agent,
                data={"level": 2, "answer": str(self._solution_part1)},
            )
            if response.ok:
                logging.info("Response OK!")
                logging.info(response.text)
            else:
                logging.info("Failed ")
