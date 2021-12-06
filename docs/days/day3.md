---
layout: default
title: Day 3
description: Binary Diagnostic
---

## Day 3

[Return to main page](../)


This day was slightly more challenging. Initially, I thought I might need to apply some binary arithmetic to solve
this problem, however, in the end this was not needed. I did decide to use numpy for fast and easy handling of arrays.
Potentially there is a smarter/faster/code-efficient solution that I didn't think of, but what I came up with works, so
that is the most important part.


### Part 1
> The submarine has been making some odd creaking noises, so you ask it to produce a diagnostic report just in case.
> 
> The diagnostic report (your puzzle input) consists of a list of binary numbers which, when decoded properly, can tell you many useful things about the conditions of the submarine. The first parameter to check is the power consumption.
> 
> You need to use the binary numbers in the diagnostic report to generate two new binary numbers (called the gamma rate and the epsilon rate). The power consumption can then be found by multiplying the gamma rate by the epsilon rate.
> 
> Each bit in the gamma rate can be determined by finding the most common bit in the corresponding position of all numbers in the diagnostic report. For example, given the following diagnostic report:
> ```
> 00100
> 11110
> 10110
> 10111
> 10101
> 01111
> 00111
> 11100
> 10000
> 11001
> 00010
> 01010
> ```
> Considering only the first bit of each number, there are five 0 bits and seven 1 bits. Since the most common bit is 1, the first bit of the gamma rate is 1.
> 
> The most common second bit of the numbers in the diagnostic report is 0, so the second bit of the gamma rate is 0.
> 
> The most common value of the third, fourth, and fifth bits are 1, 1, and 0, respectively, and so the final three bits of the gamma rate are 110.
> 
> So, the gamma rate is the binary number 10110, or 22 in decimal.
> 
> The epsilon rate is calculated in a similar way; rather than use the most common bit, the least common bit from each position is used. So, the epsilon rate is 01001, or 9 in decimal. Multiplying the gamma rate (22) by the epsilon rate (9) produces the power consumption, 198.
> 
> Use the binary numbers in your diagnostic report to calculate the gamma rate and epsilon rate, then multiply them together. What is the power consumption of the submarine? (Be sure to represent your answer in decimal, not binary.)
> 


 The parsing of the data was slightly different than previous days. First, I convert the dataset to a list of lists containing string which I convert to a numpy array. 
```python
def _parse_data(self, input_data: str) -> Any:
    string_list = [list(x) for x in input_data.split("\n") if x]
    string_array = np.array(string_list)
    return string_array
```

 Because I converted the data to a numpy array, I can easily perform operations along any dimension. Specifically, to identify the most common element for each bit, I take the ceil of the median across the rows. The median itself in a binary setting will simply select the most common element, and the np.ceil resolves ties by assigning them to 1. Then I use a list comprehension to invert the resultant string to get the least common bits. Last, I convert the bit string to an integer by calling int with a base of 2. 
```python
def _solve_part1(self, parsed_data: np.ndarray) -> Any:
    median = np.ceil(np.median(parsed_data.astype("int"), axis=0)).astype("int")
    most_common = "".join(list(median.astype('str')))
    least_common = "".join(['1' if i == '0' else '0' for i in most_common])
    gamma = int(most_common, 2)
    epsilon = int(least_common, 2)
    return gamma * epsilon
```

### Part 2

> Next, you should verify the life support rating, which can be determined by multiplying the oxygen generator rating by the CO2 scrubber rating.
> 
> Both the oxygen generator rating and the CO2 scrubber rating are values that can be found in your diagnostic report - finding them is the tricky part. Both values are located using a similar process that involves filtering out values until only one remains. Before searching for either rating value, start with the full list of binary numbers from your diagnostic report and consider just the first bit of those numbers. Then:
> 
> - Keep only numbers selected by the bit criteria for the type of rating value for which you are searching. Discard numbers which do not match the bit criteria.
> - If you only have one number left, stop; this is the rating value for which you are searching.
> - Otherwise, repeat the process, considering the next bit to the right.
> 
> The bit criteria depends on which type of rating value you want to find:
> 
> - To find oxygen generator rating, determine the most common value (0 or 1) in the current bit position, and keep only numbers with that bit in that position. If 0 and 1 are equally common, keep values with a 1 in the position being considered.
> - To find CO2 scrubber rating, determine the least common value (0 or 1) in the current bit position, and keep only numbers with that bit in that position. If 0 and 1 are equally common, keep values with a 0 in the position being considered.
> 
> For example, to determine the oxygen generator rating value using the same example diagnostic report from above:
> 
> - Start with all 12 numbers and consider only the first bit of each number. There are more 1 bits (7) than 0 bits (5), so keep only the 7 numbers with a 1 in the first position: 11110, 10110, 10111, 10101, 11100, 10000, and 11001.
> - Then, consider the second bit of the 7 remaining numbers: there are more 0 bits (4) than 1 bits (3), so keep only the 4 numbers with a 0 in the second position: 10110, 10111, 10101, and 10000.
> - In the third position, three of the four numbers have a 1, so keep those three: 10110, 10111, and 10101.
> - In the fourth position, two of the three numbers have a 1, so keep those two: 10110 and 10111.
> - In the fifth position, there are an equal number of 0 bits and 1 bits (one each). So, to find the oxygen generator rating, keep the number with a 1 in that position: 10111.
> - As there is only one number left, stop; the oxygen generator rating is 10111, or 23 in decimal.
> 
> Then, to determine the CO2 scrubber rating value from the same example above:
> 
> - Start again with all 12 numbers and consider only the first bit of each number. There are fewer 0 bits (5) than 1 bits (7), so keep only the 5 numbers with a 0 in the first position: 00100, 01111, 00111, 00010, and 01010.
> - Then, consider the second bit of the 5 remaining numbers: there are fewer 1 bits (2) than 0 bits (3), so keep only the 2 numbers with a 1 in the second position: 01111 and 01010.
> - In the third position, there are an equal number of 0 bits and 1 bits (one each). So, to find the CO2 scrubber rating, keep the number with a 0 in that position: 01010.
> - As there is only one number left, stop; the CO2 scrubber rating is 01010, or 10 in decimal.
> 
> Finally, to find the life support rating, multiply the oxygen generator rating (23) by the CO2 scrubber rating (10) to get 230.
> 
> Use the binary numbers in your diagnostic report to calculate the oxygen generator rating and CO2 scrubber rating, then multiply them together. What is the life support rating of the submarine? (Be sure to represent your answer in decimal, not binary.)

 Again, reading the actual task was the most challenging part here for me. Initially I assumed I could simply use the most and least common bit strings from the previous example, however, then I realized that I had to do it per bit because the bit strings needed to be calculated with respect to the remaining rows. The filtering on the bit criteria is very easy to do in numpy using logical expression. I could very well imagine that this problem can be solved more efficiently with a recurrent function or so, but my approach is still reasonably fast (6 - 7 ms), so I think it is ok. 
```python
def _solve_part2(self, parsed_data: np.ndarray) -> Any:
    filtered_data = parsed_data.copy().astype("int")
    i = 0
    while filtered_data.shape[0] > 1:
        el = int(np.ceil(np.median(filtered_data[:, i])))
        filtered_data = filtered_data[filtered_data[:, i] == el]
        i += 1
    og_rating = int("".join(filtered_data[0].astype("str")), 2)
    filtered_data = parsed_data.copy().astype("int")
    i = 0
    while filtered_data.shape[0] > 1:
        el = int(np.abs(np.median(filtered_data[:, i]) - 1))
        filtered_data = filtered_data[filtered_data[:, i] == el]
        i += 1
    co_rating = int("".join(filtered_data[0].astype("str")), 2)
    return og_rating * co_rating
```

[Return to main page](../)