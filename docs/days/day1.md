---
layout: default
title: Day 1
description: Python solution to day 1
---

## Day 1

[Return to main page](././)


My solution for the first day of the new advent of code for 2021. As always, pretty easy and straightforward for this
first day. That has allowed me to spend some more time on creating some nice things around it, such as the webpages
explaining my solutions. Below you can read the story of the first part of the first day.


### Part 1
> 
> As the submarine drops below the surface of the ocean, it automatically performs a sonar sweep of the nearby sea floor. On a small screen, the sonar sweep report (your puzzle input) appears: each line is a measurement of the sea floor depth as the sweep looks further and further away from the submarine.
> 
> For example, suppose you had the following report:
> 
> ```
> 200
> 208
> 199
> 210
> 200
> 207
> 240
> 269
> 260
> 263
> ```
> 
> This report indicates that, scanning outward from the submarine, the sonar sweep found depths of 199, 200, 208, 210, and so on.
> 
> The first order of business is to figure out how quickly the depth increases, just so you know what you're dealing with - you never know if the keys will get carried into deeper water by an ocean current or a fish or something.
> 
> To do this, count the number of times a depth measurement increases from the previous measurement. (There is no measurement before the first measurement.) In the example above, the changes are as follows:
> ```
> 199 (N/A - no previous measurement)
> 200 (increased)
> 208 (increased)
> 210 (increased)
> 200 (decreased)
> 207 (increased)
> 240 (increased)
> 269 (increased)
> 260 (decreased)
> 263 (increased)
> ```
> In this example, there are 7 measurements that are larger than the previous measurement.
> 


 The input data consists of a string of ints, so we split the string on the newline character and then convert the individual elements to int. 
```python
def _parse_data(self, input_data: str) -> Any:
    return [int(x) for x in input_data.split("\n") if x]
```

 This first task was really straightforward, it was just a matter of iterating over the list of items, starting from 1 and checking whether the previous value was lower. 
```python
def _solve_part1(self, parsed_data: Any) -> Any:
    count_diff = 0
    prev_val = parsed_data[0]
    for i in range(1, len(parsed_data)):
        cur_val = parsed_data[i]
        if cur_val > prev_val:
            count_diff += 1
        prev_val = cur_val
    return count_diff
```

### Part 2

> 
> Considering every single measurement isn't as useful as you expected: there's just too much noise in the data.
> 
> Instead, consider sums of a three-measurement sliding window. Again considering the above example:
> ```
> 199  A      
> 200  A B    
> 208  A B C  
> 210    B C D
> 200  E   C D
> 207  E F   D
> 240  E F G  
> 269    F G H
> 260      G H
> 263        H
> ```
> Start by comparing the first and second three-measurement windows. The measurements in the first window are marked A (199, 200, 208); their sum is 199 + 200 + 208 = 607. The second window is marked B (200, 208, 210); its sum is 618. The sum of measurements in the second window is larger than the sum of the first, so this first comparison increased.
> 
> Your goal now is to count the number of times the sum of measurements in this sliding window increases from the previous sum. So, compare A with B, then compare B with C, then C with D, and so on. Stop when there aren't enough measurements left to create a new three-measurement sum.
> 
> In the above example, the sum of each three-measurement window is as follows:
> ```
> A: 607 (N/A - no previous sum)
> B: 618 (increased)
> C: 618 (no change)
> D: 617 (decreased)
> E: 647 (increased)
> F: 716 (increased)
> G: 769 (increased)
> H: 792 (increased)
> ```
> In this example, there are 5 sums that are larger than the previous sum.
> 
> Consider sums of a three-measurement sliding window. How many sums are larger than the previous sum?

 Part 2 was not much more difficult, instead of taking the value itself we now take the sum of the next three values while iterating from 1 until length - 2. 
```python
def _solve_part2(self, parsed_data: Any) -> Any:
    count_diff = 0
    prev_val = sum(parsed_data[0:3])
    for i in range(1, len(parsed_data) - 2):
        cur_val = sum(parsed_data[i:i+3])
        if cur_val > prev_val:
            count_diff += 1
        prev_val = cur_val
    return count_diff
```

[Return to main page](././)