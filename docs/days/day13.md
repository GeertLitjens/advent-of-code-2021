---
layout: default
title: Day 13
description: Transparent Origami

---

## Day 13

[Return to main page](../)


Interesting graphical puzzle in the end, the first one where I could not auto-submit Part 2 but had to type it in
manually. In the end I took the intellectually easy way output by not actually mirroring the coordinates, but simply
using a very large numpy array to holds all the positions and simply using np.flip and appropriate indexing to do the
folds, which worked well enough.


### Part 1
> You reach another volcanically active part of the cave. It would be nice if you could do some kind of thermal imaging so you could tell ahead of time which caves are too hot to safely enter.
> 
> Fortunately, the submarine seems to be equipped with a thermal camera! When you activate it, you are greeted with:
> ```
> Congratulations on your purchase! To activate this infrared thermal imaging
> camera system, please enter the code found on page 1 of the manual.
> ```
> Apparently, the Elves have never used this feature. To your surprise, you manage to find the manual; as you go to open it, page 1 falls out. It's a large sheet of transparent paper! The transparent paper is marked with random dots and includes instructions on how to fold it up (your puzzle input). For example:
> ```
> 6,10
> 0,14
> 9,10
> 0,3
> 10,4
> 4,11
> 6,0
> 6,12
> 4,1
> 0,13
> 10,12
> 3,4
> 3,0
> 8,4
> 1,10
> 2,14
> 8,10
> 9,0
> 
> fold along y=7
> fold along x=5
> ```
> The first section is a list of dots on the transparent paper. 0,0 represents the top-left coordinate. The first value, x, increases to the right. The second value, y, increases downward. So, the coordinate 3,0 is to the right of 0,0, and the coordinate 0,7 is below 0,0. The coordinates in this example form the following pattern, where # is a dot on the paper and . is an empty, unmarked position:
> ```
> ...#..#..#.
> ....#......
> ...........
> #..........
> ...#....#.#
> ...........
> ...........
> ...........
> ...........
> ...........
> .#....#.##.
> ....#......
> ......#...#
> #..........
> #.#........
> ```
> Then, there is a list of fold instructions. Each instruction indicates a line on the transparent paper and wants you to fold the paper up (for horizontal y=... lines) or left (for vertical x=... lines). In this example, the first fold instruction is fold along y=7, which designates the line formed by all of the positions where y is 7 (marked here with -):
> ```
> ...#..#..#.
> ....#......
> ...........
> #..........
> ...#....#.#
> ...........
> ...........
> -----------
> ...........
> ...........
> .#....#.##.
> ....#......
> ......#...#
> #..........
> #.#........
> ```
> Because this is a horizontal line, fold the bottom half up. Some of the dots might end up overlapping after the fold is complete, but dots will never appear exactly on a fold line. The result of doing this fold looks like this:
> ```
> #.##..#..#.
> #...#......
> ......#...#
> #...#......
> .#.#..#.###
> ...........
> ...........
> ```
> Now, only 17 dots are visible.
> 
> Notice, for example, the two dots in the bottom left corner before the transparent paper is folded; after the fold is complete, those dots appear in the top left corner (at 0,0 and 0,1). Because the paper is transparent, the dot just below them in the result (at 0,3) remains visible, as it can be seen through the transparent paper.
> 
> Also notice that some dots can end up overlapping; in this case, the dots merge together and become a single dot.
> 
> The second fold instruction is fold along x=5, which indicates this line:
> ```
> #.##.|#..#.
> #...#|.....
> .....|#...#
> #...#|.....
> .#.#.|#.###
> .....|.....
> .....|.....
> ```
> Because this is a vertical line, fold left:
> ```
> #####
> #...#
> #...#
> #...#
> #####
> .....
> .....
> ```
> The instructions made a square!
> 
> The transparent paper is pretty big, so for now, focus on just completing the first fold. After the first fold in the example above, 17 dots are visible - dots that end up overlapping after the fold is completed count as a single dot.
> 
> How many dots are visible after completing just the first fold instruction on your transparent paper?
> 


 More involved data parsing function this time around because I wanted to encode the coordinates in an array. So first split the coordinates and the folding instructions. Then generate an array as large as the span of the coordinates in both dimensions and set the coordinates to 1. Subsequently, split the fold instructions into an axis identifier and a position. 
```python
def _parse_data(self, input_data: str) -> Any:
    coord_string, fold_string = input_data.split("\n\n")
    coords = np.array([[int(coord.split(",")[1]), int(coord.split(",")[0])] for coord in coord_string.split("\n")])
    paper = np.zeros((np.max(coords[:, 0]) + 1, np.max(coords[:, 1]) + 1), dtype="ubyte")
    paper[coords[:, 0], coords[:, 1]] = 1
    folds = [(a_p.split("=")[0].split("fold along ")[1], int(a_p.split("=")[1])) for a_p in fold_string.split("\n") if a_p]
    return paper, folds
```

 Part 1 uses the basic folding mechanism: identify the axis and flip the subarray to the right or bottom and add that to the subarray to the left or top and removing the remainder. Here we just take the first fold. 
```python
def _solve_part1(self, parsed_data: Any) -> Any:
    paper, folds = parsed_data
    axis, pos = folds[0]
    if axis == "x":
        paper = paper[:, :pos] + np.flip(paper[:, pos + 1:], axis=1)
    else:
        flipped = np.flip(paper[pos + 1:] , axis=0)
        paper = paper[:pos] + flipped
    paper = (paper > 0).astype("ubyte")
    return np.sum(paper)
```

### Part 2

> Finish folding the transparent paper according to the instructions. The manual says the code is always eight capital letters.
> 
> What code do you use to activate the infrared thermal imaging camera system?


 Same as part 1, but now we do all folds. Because I don't want to implement an entire OCR step, I just read the result from the terminal window. To still have a meaningful test, I use the same return value as in part 1. 
```python
def _solve_part2(self, parsed_data: Any) -> Any:
    paper, folds = parsed_data
    for axis, pos in folds:
        if axis == "x":
            paper = paper[:, :pos] + np.flip(paper[:, pos + 1:], axis=1)
        else:
            flipped = np.flip(paper[pos + 1:] , axis=0)
            paper = paper[:pos] + flipped
        paper = (paper > 0).astype("ubyte")
    print("\n" + np.array2string(paper, separator='', formatter={'int': {0: ' ', 1: "\u2588"}.get}))
    return np.sum(paper)
```

[Return to main page](../)