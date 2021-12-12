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
> You ask the submarine to determine the best route out of the deep-sea cave, but it only replies:
> 
> Syntax error in navigation subsystem on line: all of them
> All of them?! The damage is worse than you thought. You bring up a copy of the navigation subsystem (your puzzle input).
> 
> The navigation subsystem syntax is made of several lines containing chunks. There are one or more chunks on each line, and chunks contain zero or more other chunks. Adjacent chunks are not separated by any delimiter; if one chunk stops, the next chunk (if any) can immediately start. Every chunk must open and close with one of four legal pairs of matching characters:
> 
> - If a chunk opens with ```(```, it must close with ```)```.
> - If a chunk opens with ```[```, it must close with ```]```.
> - If a chunk opens with ```{```, it must close with ```}```.
> - If a chunk opens with ```<```, it must close with ```>```.
> 
> So, ```()``` is a legal chunk that contains no other chunks, as is []. More complex but valid chunks include ```([])```, ```{()()()}```, ```<([{}])>```, ```[<>({}){}[([])<>]]```, and even ```(((((((((())))))))))```.
> 
> Some lines are incomplete, but others are corrupted. Find and discard the corrupted lines first.
> 
> A corrupted line is one where a chunk closes with the wrong character - that is, where the characters it opens and closes with do not form one of the four legal pairs listed above.
> 
> Examples of corrupted chunks include (], {()()()>, (((()))}, and <([]){()}[{}]). Such a chunk can appear anywhere within a line, and its presence causes the whole line to be considered corrupted.
> 
> For example, consider the following navigation subsystem:
> ```
> [({(<(())[]>[[{[]{<()<>>
> [(()[<>])]({[<{<<[]>>(
> {([(<{}[<>[]}>{[]{[(<()>
> (((({<>}<{<{<>}{[]{[]{}
> [[<[([]))<([[{}[[()]]]
> [{[{({}]{}}([{[{{{}}([]
> {<[[]]>}<{[{[{[]{()[[[]
> [<(<(<(<{}))><([]([]()
> <{([([[(<>()){}]>(<<{{
> <{([{{}}[<[[[<>{}]]]>[]]
> ```
> Some of the lines aren't corrupted, just incomplete; you can ignore these lines for now. The remaining five lines are corrupted:
> 
> - ```{([(<{}[<>[]}>{[]{[(<()>``` - Expected ```]```, but found ```}``` instead.
> - ```[[<[([]))<([[{}[[()]]]``` - Expected ```]```, but found ```)``` instead.
> - ```[{[{({}]{}}([{[{{{}}([]``` - Expected ```)```, but found ```]``` instead.
> - ```[<(<(<(<{}))><([]([]()``` - Expected ```>```, but found ```)``` instead.
> - ```<{([([[(<>()){}]>(<<{{``` - Expected ```]```, but found ```>``` instead.
> 
> Stop at the first incorrect closing character on each corrupted line.
> 
> Did you know that syntax checkers actually have contests to see who can get the high score for syntax errors in a file? It's true! To calculate the syntax error score for a line, take the first illegal character on the line and look it up in the following table:
> 
> - ```)```: 3 points.
> - ```]```: 57 points.
> - ```}```: 1197 points.
> - ```>```: 25137 points. 
> 
> In the above example, an illegal ) was found twice (2*3 = 6 points), an illegal ] was found once (57 points), an illegal } was found once (1197 points), and an illegal > was found once (25137 points). So, the total syntax error score for this file is 6+57+1197+25137 = 26397 points!
> 
> Find the first illegal character in each corrupted line of the navigation subsystem. What is the total syntax error score for those errors?
> 


 
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

> <PART_2_TEXT>


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