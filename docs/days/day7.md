---
layout: default
title: Day 7
description: Day 7: The Treachery of Whales

---

## Day 7

[Return to main page](../)


Today was quite simple again, especially part 1. The key for part 1 was simply the realization that the median position
will always cause the sum of distance to be lowest. Part 2 was a bit more tricky. I did realize that the distance
for part 2 was simply the triangular number, defined as $rac{n * (n + 1)}rac{2}$. Then I first simply brute forced
the solution to find the smallest sum of distances, starting at the median. This gave me the correct answer, and then
I spent a bit of time to implement a binary search to optimize the search time.


### Part 1
> A giant whale has decided your submarine is its next meal, and it's much faster than you are. There's nowhere to run!
> 
> Suddenly, a swarm of crabs (each in its own tiny submarine - it's too deep for them otherwise) zooms in to rescue you! They seem to be preparing to blast a hole in the ocean floor; sensors indicate a massive underground cave system just beyond where they're aiming!
> 
> The crab submarines all need to be aligned before they'll have enough power to blast a large enough hole for your submarine to get through. However, it doesn't look like they'll be aligned before the whale catches you! Maybe you can help?
> 
> There's one major catch - crab submarines can only move horizontally.
> 
> You quickly make a list of the horizontal position of each crab (your puzzle input). Crab submarines have limited fuel, so you need to find a way to make all of their horizontal positions match while requiring them to spend as little fuel as possible.
> 
> For example, consider the following horizontal positions:
> 
> ```
> 16,1,2,0,4,2,7,1,2,14
> ```
> This means there's a crab with horizontal position 16, a crab with horizontal position 1, and so on.
> 
> Each change of 1 step in horizontal position of a single crab costs 1 fuel. You could choose any horizontal position to align them all on, but the one that costs the least fuel is horizontal position 2:
> 
> - Move from 16 to 2: 14 fuel
> - Move from 1 to 2: 1 fuel
> - Move from 2 to 2: 0 fuel
> - Move from 0 to 2: 2 fuel
> - Move from 4 to 2: 2 fuel
> - Move from 2 to 2: 0 fuel
> - Move from 7 to 2: 5 fuel
> - Move from 1 to 2: 1 fuel
> - Move from 2 to 2: 0 fuel
> - Move from 14 to 2: 12 fuel
> 
> This costs a total of 37 fuel. This is the cheapest possible outcome; more expensive outcomes include aligning at position 1 (41 fuel), position 3 (39 fuel), or position 10 (71 fuel).
> 
> Determine the horizontal position that the crabs can align to using the least fuel possible. How much fuel must they spend to align to that position?


 Data parsing was again very straightforward, just returning a numpy array of ints. 
```python
def _parse_data(self, input_data: str) -> Any:
    return np.array([int(x) for x in input_data.split(",")])
```

 Part 1 was straightforward, the median of a list points will always be the point with the lowest sum of distances to the other points in a list. 
```python
def _solve_part1(self, parsed_data: Any) -> Any:
    return np.sum(np.abs(parsed_data - np.median(parsed_data)))
```

### Part 2

> The crabs don't seem interested in your proposed solution. Perhaps you misunderstand crab engineering?
> 
> As it turns out, crab submarine engines don't burn fuel at a constant rate. Instead, each change of 1 step in horizontal position costs 1 more unit of fuel than the last: the first step costs 1, the second step costs 2, the third step costs 3, and so on.
> 
> As each crab moves, moving further becomes more expensive. This changes the best horizontal position to align them all on; in the example above, this becomes 5:
> 
> - Move from 16 to 5: 66 fuel
> - Move from 1 to 5: 10 fuel
> - Move from 2 to 5: 6 fuel
> - Move from 0 to 5: 15 fuel
> - Move from 4 to 5: 1 fuel
> - Move from 2 to 5: 6 fuel
> - Move from 7 to 5: 3 fuel
> - Move from 1 to 5: 10 fuel
> - Move from 2 to 5: 6 fuel
> - Move from 14 to 5: 45 fuel
> 
> This costs a total of 168 fuel. This is the new cheapest possible outcome; the old alignment position (2) now costs 206 fuel instead.
> 
> Determine the horizontal position that the crabs can align to using the least fuel possible so they can make you an escape route! How much fuel must they spend to align to that position?

 Part 2 was a bit more tricky. I did know that the given definition of the new distance was a triangular number, for example $T_2 = 1 + 2$ and $T_4 = 1 + 2 + 3 + 4$. I couldn't think of a way to solve this analytically, so I wrote a simple brute force search, starting from the median point and then going higher. Later I replaced it with a binary search to make it more efficient. There might be a better solution, but I'm pretty happy with the result. 
```python
def _solve_part2(self, parsed_data: Any) -> Any:
    low_x = np.median(parsed_data)
    high_x = np.max(parsed_data)
    def calc_min(cur_pos, all_pos): return np.sum([x * (x + 1) / 2 for x in np.abs(all_pos - cur_pos)])
    low_min = calc_min(low_x, parsed_data)
    high_min = calc_min(high_x, parsed_data)
    while low_x != high_x:
        if low_min > high_min:
            low_x = np.ceil((low_x + high_x) / 2)
            low_min = calc_min(low_x, parsed_data)
        else:
            high_x = np.floor((low_x + high_x) / 2)
            high_min = calc_min(high_x, parsed_data)
    return high_min
```

[Return to main page](../)