---
layout: default
title: Day 5
description: Hydrothermal Venture
---

## Day 5

[Return to main page](../)


I think the key challenge today was to really subdivide the problem into two parts. First, put most of the logic related
to the orientation and coordinates of the line in a separate class. Then in the problem itself we focus on keeping track
of the hit rate of the different coordinates. In that way the logical statements (i.e. is equal, greater than, etc.)
can be simpler.

### Part 1
> You come across a field of hydrothermal vents on the ocean floor! These vents constantly produce large, opaque clouds, so it would be best to avoid them if possible.
> 
> They tend to form in lines; the submarine helpfully produces a list of nearby lines of vents (your puzzle input) for you to review. For example:
> ```
> 0,9 -> 5,9
> 8,0 -> 0,8
> 9,4 -> 3,4
> 2,2 -> 2,1
> 7,0 -> 7,4
> 6,4 -> 2,0
> 0,9 -> 2,9
> 3,4 -> 1,4
> 0,0 -> 8,8
> 5,5 -> 8,2
> ```
> Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where x1,y1 are the coordinates of one end the line segment and x2,y2 are the coordinates of the other end. These line segments include the points at both ends. In other words:
> 
> - An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
> - An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.
> 
> For now, only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.
> 
> So, the horizontal and vertical lines from the above list would produce the following diagram:
> ```
> .......1..
> ..1....1..
> ..1....1..
> .......1..
> .112111211
> ..........
> ..........
> ..........
> ..........
> 222111....
> ```
> In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9. Each position is shown as the number of lines which cover that point or . if no line covers that point. The top-left pair of 1s, for example, comes from 2,2 -> 2,1; the very bottom row is formed by the overlapping lines 0,9 -> 5,9 and 0,9 -> 2,9.
> 
> To avoid the most dangerous areas, you need to determine the number of points where at least two lines overlap. In the above example, this is anywhere in the diagram with a 2 or larger - a total of 5 points.
> 
> Consider only horizontal and vertical lines. At how many points do at least two lines overlap?

The Line class contains all the logic for getting line coordinates. Note that it only works under the assumption that
lines are either horizontal, vertical or have a 45-degree angle. In the init function we determine the
directionality in the x and y directions using the sign function. In traverse we simply iterate from the start to
the end of the line using a generator function.

```python
class Line:
    def __init__(self, point_1: tuple[int, int], point_2: tuple[int, int]) -> None:
        self._x0, self._y0 = point_1
        self._x1, self._y1 = point_2
        self._dir_x = np.sign(self._x1 - self._x0)
        self._dir_y = np.sign(self._y1 - self._y0)

    def is_horizontal(self) -> bool:
        return self._y0 == self._y1

    def is_vertical(self) -> bool:
        return self._x0 == self._x1

    def traverse(self) -> tuple[int, int]:
        cur_x = self._x0
        cur_y = self._y0
        while cur_x != self._x1 + self._dir_x or cur_y != self._y1 + self._dir_y:
            yield cur_x, cur_y
            cur_x += self._dir_x
            cur_y += self._dir_y
```
We parse the data into Line class instances, which was pretty straightforward parsing: simply split the lines to obtain the different line definitions. Then split on the arrow character to get the begin and end points. These points are then converted to int's and fed to the initialization function of the line class.
```python
def _parse_data(self, input_data: str) -> Any:
    lines_string = [x for x in input_data.split("\n") if x]
    lines = []
    for line in lines_string:
        coord1, coord2 = line.split(" -> ")
        x0, y0 = [int(x) for x in coord1.split(",")]
        x1, y1 = [int(x) for x in coord2.split(",")]
        lines.append(Line((x0, y0), (x1, y1)))
    return lines
```

The _discover_danger_points function checks the count a coordinate is hit using a dictionary object. This is more memory efficient than a list
or array because we have sparse points along broad dimensions. We check here whether we should only should
consider straight lines and whether the line is actually horizontal and vertical.

```python
def _discover_danger_points(self, parsed_data: list[Line], check_straight: bool = True):
    coord_checker = defaultdict(int)
    for line in parsed_data:
        if not check_straight or (line.is_horizontal() or line.is_vertical()):
            for coord in line.traverse():
                coord_checker[coord] += 1
    danger_points = np.array(list(coord_checker.values()))
    return (danger_points > 1).sum()
```
This was the first time this year that I created a separate class to handle most of the logic of the problem. That simplifies this function significantly. As the only difference between part 1 and 2 is whether diagonal lines should be considered I implemented a separate parameterized function to handle this. 
```python
def _solve_part1(self, parsed_data: list[Line]) -> Any:
    return self._discover_danger_points(parsed_data)
```

### Part 2

> Unfortunately, considering only horizontal and vertical lines doesn't give you the full picture; you need to also consider diagonal lines.
> 
> Because of the limits of the hydrothermal vent mapping system, the lines in your list will only ever be horizontal, vertical, or a diagonal line at exactly 45 degrees. In other words:
> 
> - An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
> - An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.
> 
> Considering all lines from the above example would now produce the following diagram:
> ```
> 1.1....11.
> .111...2..
> ..2.1.111.
> ...1.2.2..
> .112313211
> ...1.2....
> ..1...1...
> .1.....1..
> 1.......1.
> 222111....
> ```
> You still need to determine the number of points where at least two lines overlap. In the above example, this is still anywhere in the diagram with a 2 or larger - now a total of 12 points.
> 
> Consider all of the lines. At how many points do at least two lines overlap?

 Exactly the same implementation as part 1, just one different parameter to make sure we consider diagonal lines. 
```python
def _solve_part2(self, parsed_data: list[Line]) -> Any:
    return self._discover_danger_points(parsed_data, False)
```

[Return to main page](../)