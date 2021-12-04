---
layout: default
title: Day 4
description: Python solution to day 4
---

## Day 4

[Return to main page](../)


The puzzles start to become a little more complex. I quickly decided I would again use numpy to solve this puzzle
because it allows efficient summing across different axes. Furthermore, it allows to quickly perform comparisons across
all elements. After solving the first part, the second part was pretty straightforward this time.


### Part 1
> You're already almost 1.5km (almost a mile) below the surface of the ocean, already so deep that you can't see any sunlight. What you can see, however, is a giant squid that has attached itself to the outside of your submarine.
> 
> Maybe it wants to play bingo?
> 
> Bingo is played on a set of boards each consisting of a 5x5 grid of numbers. Numbers are chosen at random, and the chosen number is marked on all boards on which it appears. (Numbers may not appear on all boards.) If all numbers in any row or any column of a board are marked, that board wins. (Diagonals don't count.)
> 
> The submarine has a bingo subsystem to help passengers (currently, you and the giant squid) pass the time. It automatically generates a random order in which to draw numbers and a random set of boards (your puzzle input). For example:
> ```
> 7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1
> 
> 22 13 17 11  0
>  8  2 23  4 24
> 21  9 14 16  7
>  6 10  3 18  5
>  1 12 20 15 19
> 
>  3 15  0  2 22
>  9 18 13 17  5
> 19  8  7 25 23
> 20 11 10 24  4
> 14 21 16 12  6
> 
> 14 21 17 24  4
> 10 16 15  9 19
> 18  8 23 26 20
> 22 11 13  6  5
>  2  0 12  3  7
> ```
> After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no winners, but the boards are marked as follows (shown here adjacent to each other to save space):
> ```
> 22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
>  8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
> 21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
>  6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
>  1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
>  ```
> After the next six numbers are drawn (17, 23, 2, 0, 14, and 21), there are still no winners:
> ```
> 22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
>  8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
> 21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
>  6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
>  1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
>  ```
> Finally, 24 is drawn:
> ```
> 22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
>  8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
> 21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
>  6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
>  1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
>  ```
> At this point, the third board wins because it has at least one complete row or column of marked numbers (in this case, the entire top row is marked: 14 21 17 24 4).
> 
> The score of the winning board can now be calculated. Start by finding the sum of all unmarked numbers on that board; in this case, the sum is 188. Then, multiply that sum by the number that was just called when the board won, 24, to get the final score, 188 * 24 = 4512.
> 
> To guarantee victory against the giant squid, figure out which board will win first. What will your final score be if you choose that board?


 The data parsing was again slightly more complex because of the different first line. So first split all objects by splitting on a double new line. Then conver the first line into a list of ints. For the boards we use numpy from string to convert every board into a 1D array and then reshape it to become 2D again. 
```python
def _parse_data(self, input_data: str) -> Any:
    object_list = input_data.split("\n\n")
    drawn_numbers = [int(x) for x in object_list[0].split(",")]
    board_list = []
    for board in object_list[1:]:
        board_list.append(np.fromstring(board.replace("\n", " "), dtype="int", sep=" ").reshape(5, 5))
    return drawn_numbers, board_list
```

 The overall solution is pretty straightforward and might not be the most computationally efficient, but it requires only a few lines of code. We create a mask containing ones for each board to keep track of the numbers that have been marked. By setting the drawn numbers to zero we can simply multiply the mask with the board at the end to get a sum of the unmarked numbers. We identify completed lines by summing along both axes: if a row or column only contains 0's, then the sum obviously will also only contain zeros. Once the first board completes , we return the solution. 
```python
def _solve_part1(self, parsed_data: tuple[list[int], list[np.ndarray]]) -> Any:
    drawn_numbers, board_list = parsed_data
    mask_list = [np.ones((5,5), dtype="byte") for x in range(len(board_list))]
    for number in drawn_numbers:
        for board_index in range(len(board_list)):
            mask_list[board_index][np.where(board_list[board_index] == number)] = 0
            if (mask_list[board_index].sum(axis=0) == 0).any() or (mask_list[board_index].sum(axis=1) == 0).any():
                return (mask_list[board_index] * board_list[board_index]).sum() * number
```

### Part 2

> On the other hand, it might be wise to try a different strategy: let the giant squid win.
> 
> You aren't sure how many bingo boards a giant squid could play at once, so rather than waste time counting its arms, the safe thing to do is to figure out which board will win last and choose that one. That way, no matter which boards it picks, it will win for sure.
> 
> In the above example, the second board is the last to win, which happens after 13 is eventually called and its middle column is completely marked. If you were to keep playing until this point, the second board would have a sum of unmarked numbers equal to 148 for a final score of 148 * 13 = 1924.
> 
> Figure out which board will win last. Once it wins, what would its final score be?

 Part 2 is very similar to part one. The only difference is that we need to remove (blacklist) all the boards that have been completed, otherwise they will pop-up more often (because other rows or columns) complete. We do not one to change the list we are iterating over in-place, so we blacklist the board index so we do not consider it again once we have completed it once. After all numbers have been draw we simply return the last board that was completed to solve part 2! 
```python
def _solve_part2(self, parsed_data: tuple[list[int], list[np.ndarray]]) -> Any:
    drawn_numbers, board_list = parsed_data
    mask_list = [np.ones((5,5), dtype="byte") for x in range(len(board_list))]
    last_board = None
    last_mask = None
    last_number = None
    blacklist = []
    for number in drawn_numbers:
        for board_index in range(len(board_list)):
            if board_index in blacklist:
                continue
            mask_list[board_index][np.where(board_list[board_index] == number)] = 0
            if (mask_list[board_index].sum(axis=0) == 0).any() or (mask_list[board_index].sum(axis=1) == 0).any():
                last_board = board_list[board_index]
                last_mask = mask_list[board_index]
                last_number = number
                blacklist.append(board_index)
    return (last_board * last_mask).sum() * last_number
```

[Return to main page](../)