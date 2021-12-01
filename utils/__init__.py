import requests
import os


def get_input_data(day: int, year: int = 2021) -> str:
    input_url = f"https://adventofcode.com/{year}/day/{day}/input"
    user_agent = {"User-Agent": "advent-of-code-data v1.1.0"}
    session_token = {"session" : os.environ["AOC_TOKEN"]}
    response = requests.get(url=input_url, cookies=session_token, headers=user_agent)
    if response.ok:
        return response.text
    else:
        return ""


def submit_answer(answer: str, day: int, year: int) -> bool:
    pass
