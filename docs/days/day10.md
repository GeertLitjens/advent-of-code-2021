---
layout: default
title: Day 10
description: Syntax Scoring

---

## Day 10

[Return to main page](../)


Very familiar problem, I think I saw something similar before in previous years. Initially I thought I would solve it
with a recursive function, but soon realized that was overcomplicating the matter as every matching closing brace was
only determined by the exact opening brace before. As such a simple stack with pop and append was enough to keep track
of the braces as that had were part of the equation. Other than that, it is pretty straightforward, count the correct
number of points in the end.


### Part 1
The text of this Advent of Code Day was causing me a lot of GitHub parsing issues, so I removed it.
```python
def _parse_data(self, input_data: str) -> Any:
    return [x for x in input_data.split("\n") if x]
```

 I used a separate function because we need to use the exact same parsing behavior for parts 1 and 2. This function simply puts closing braces on the stack and pops one when we encounter a closing brace. If it does not match, the line is invalid and that brace is the wrong character. Then simply add up the costs. 
```python
def _check_line(self, line):
    stack = []
    for char in line:
        if char in self._open_to_close.keys():
            stack.append(self._open_to_close[char])
        elif char in self._open_to_close.values():
            close_char = stack.pop()
            if close_char != char:
                return True, char, stack
    return False, "", stack

def _solve_part1(self, parsed_data: Any) -> Any:
    cost = 0
    for line in parsed_data:
        invalid, wrong_char, stack = self._check_line(line)
        if invalid:
            cost += self._char_to_cost[wrong_char]
    return cost
```

### Part 2

 Part 2 uses the same parsing function, but now we consider lines that are not invalid. Because we use a stack, it is pretty straightforward to assess the missing closing braces, namely the remainder on the stack. The only mistake I initially made is that I forgot to reverse the stack to get the correct score. 
```python
def _solve_part2(self, parsed_data: Any) -> Any:
    points = []
    for line in parsed_data:
        invalid, wrong_char, stack = self._check_line(line)
        if not invalid:
            points_for_line = 0
            for close_char in reversed(stack):
                points_for_line = points_for_line * 5 + self._char_to_points[close_char]
            points.append(int(points_for_line))
    return np.median(points)
```

[Return to main page](../)