---
layout: default
title: Day 8
description: Seven Segment Search

---

## Day 8

[Return to main page](../)


Quite a challenging puzzle today, at least part 2. Part 1 was mostly complicated due to the large amount of story text,
which you really did not need to solve that part. Other than that, I over-engineered part 2 initially by figuring out
exactly which segment corresponded to which letter in the code, but that seemed to be completely unnecessary after I
finished the assignment because I realized you can identify any number by just using set intersection with the numbers
you know because of their length. For example, 2 is the only number with 5 segments and 2 overlapping segments with 4,
which you can identify uniquely because it has 4 segments. After this I simplified the code to what it is now. As such,
mostly a conceptual exercise, but the programming part was straightforward.


### Part 1
> You barely reach the safety of the cave when the whale smashes into the cave mouth, collapsing it. Sensors indicate another exit to this cave at a much greater depth, so you have no choice but to press on.
> 
> As your submarine slowly makes its way through the cave system, you notice that the four-digit seven-segment displays in your submarine are malfunctioning; they must have been damaged during the escape. You'll be in a lot of trouble without them, so you'd better figure out what's wrong.
> 
> Each digit of a seven-segment display is rendered by turning on or off any of seven segments named a through g:
> ```
>   0:      1:      2:      3:      4:
>  aaaa    ....    aaaa    aaaa    ....
> b    c  .    c  .    c  .    c  b    c
> b    c  .    c  .    c  .    c  b    c
>  ....    ....    dddd    dddd    dddd
> e    f  .    f  e    .  .    f  .    f
> e    f  .    f  e    .  .    f  .    f
>  gggg    ....    gggg    gggg    ....
> 
>   5:      6:      7:      8:      9:
>  aaaa    aaaa    aaaa    aaaa    aaaa
> b    .  b    .  .    c  b    c  b    c
> b    .  b    .  .    c  b    c  b    c
>  dddd    dddd    ....    dddd    dddd
> .    f  e    f  .    f  e    f  .    f
> .    f  e    f  .    f  e    f  .    f
>  gggg    gggg    ....    gggg    gggg
>  ```
> So, to render a 1, only segments c and f would be turned on; the rest would be off. To render a 7, only segments a, c, and f would be turned on.
> 
> The problem is that the signals which control the segments have been mixed up on each display. The submarine is still trying to display numbers by producing output on signal wires a through g, but those wires are connected to segments randomly. Worse, the wire/segment connections are mixed up separately for each four-digit display! (All of the digits within a display use the same connections, though.)
> 
> So, you might know that only signal wires b and g are turned on, but that doesn't mean segments b and g are turned on: the only digit that uses two segments is 1, so it must mean segments c and f are meant to be on. With just that information, you still can't tell which wire (b/g) goes to which segment (c/f). For that, you'll need to collect more information.
> 
> For each display, you watch the changing signals for a while, make a note of all ten unique signal patterns you see, and then write down a single four digit output value (your puzzle input). Using the signal patterns, you should be able to work out which pattern corresponds to which digit.
> 
> For example, here is what you might see in a single entry in your notes:
> ```
> acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab |
> cdfeb fcadb cdfeb cdbaf
> ```
> (The entry is wrapped here to two lines so it fits; in your notes, it will all be on a single line.)
> 
> Each entry consists of ten unique signal patterns, a \| delimiter, and finally the four digit output value. Within an entry, the same wire/segment connections are used (but you don't know what the connections actually are). The unique signal patterns correspond to the ten different ways the submarine tries to render a digit using the current wire/segment connections. Because 7 is the only digit that uses three segments, dab in the above example means that to render a 7, signal lines d, a, and b are on. Because 4 is the only digit that uses four segments, eafb means that to render a 4, signal lines e, a, f, and b are on.
> 
> Using this information, you should be able to work out which combination of signal wires corresponds to each of the ten digits. Then, you can decode the four digit output value. Unfortunately, in the above example, all of the digits in the output value (cdfeb fcadb cdfeb cdbaf) use five segments and are more difficult to deduce.
> 
> For now, focus on the easy digits. Consider this larger example:
> ```
> be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb |
> fdgacbe cefdb cefbgd gcbe
> edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec |
> fcgedb cgb dgebacf gc
> fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef |
> cg cg fdcagb cbg
> fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega |
> efabcd cedba gadfec cb
> aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga |
> gecf egdcabf bgf bfgea
> fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf |
> gebdcfa ecba ca fadegcb
> dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf |
> cefg dcbef fcge gbcadfe
> bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd |
> ed bcgafe cdgba cbgef
> egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg |
> gbdfcae bgc cg cgb
> gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc |
> fgae cfgab fg bagce
> ```
> Because the digits 1, 4, 7, and 8 each use a unique number of segments, you should be able to tell which combinations of signals correspond to those digits. Counting only digits in the output values (the part after | on each line), in the above example, there are 26 instances of digits that use a unique number of segments (highlighted above).
> 
> In the output values, how many times do digits 1, 4, 7, or 8 appear?


 Data parsing is pretty straightforward. First split the lines, then the patterns and output values on the | separator. Finally, we create sets for the individual patterns and output sections to allow set operations later on. 
```python
def _parse_data(self, input_data: str) -> Any:
    lines = [x for x in input_data.split("\n") if x]
    patterns = [line.split(" | ")[0] for line in lines]
    output_values = [line.split(" | ")[1] for line in lines]
    patterns = [[set(y) for y in x.split(" ")] for x in patterns]
    output_values = [[set(y) for y in x.split(" ")] for x in output_values]
    return patterns, output_values
```

 Part 1 has a very simple solution, you just calculate the length of the output values and if it is either 2, 3, 4 or 7 it is one of the simple numbers. Just count them and return, we can even do it in a 1-line list comprehension. 
```python
def _solve_part1(self, parsed_data: Any) -> Any:
    patterns, output_values = parsed_data
    return np.sum([1 for output_value in output_values for value in output_value if len(value) in [2, 3, 4, 7]])
```

### Part 2

> Through a little deduction, you should now be able to determine the remaining digits. Consider again the first example above:
> ```
> acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab |
> cdfeb fcadb cdfeb cdbaf
> ```
> After some careful analysis, the mapping between signal wires and segments only make sense in the following configuration:
> ```
>  dddd
> e    a
> e    a
>  ffff
> g    b
> g    b
>  cccc
>  ```
> So, the unique signal patterns would correspond to the following digits:
> 
> - acedgfb: 8
> - cdfbe: 5
> - gcdfa: 2
> - fbcad: 3
> - dab: 7
> - cefabd: 9
> - cdfgeb: 6
> - eafb: 4
> - cagedb: 0
> - ab: 1
> 
> Then, the four digits of the output value can be decoded:
> 
> - cdfeb: 5
> - fcadb: 3
> - cdfeb: 5
> - cdbaf: 3
> 
> Therefore, the output value for this entry is 5353.
> 
> Following this same process for each entry in the second, larger example above, the output value of each entry can be determined:
> 
> - fdgacbe cefdb cefbgd gcbe: 8394
> - fcgedb cgb dgebacf gc: 9781
> - cg cg fdcagb cbg: 1197
> - efabcd cedba gadfec cb: 9361
> - gecf egdcabf bgf bfgea: 4873
> - gebdcfa ecba ca fadegcb: 8418
> - cefg dcbef fcge gbcadfe: 4548
> - ed bcgafe cdgba cbgef: 1625
> - gbdfcae bgc cg cgb: 8717
> - fgae cfgab fg bagce: 4315
> 
> Adding all of the output values in this larger example produces 61229.
> 
> For each entry, determine all of the wire/segment connections and decode the four-digit output values. What do you get if you add up all of the output values?

 Part 2 was trickier and mostly required a bit of logical reasoning. The key here is that any number can be expressed by the number of segments and the overlapping segments with other numbers. For example, 1, 4, 7 and 8 are identifiable by their number of segments alone because they are unique. However, there are 3 numbers with 5 segments (2, 3, and 5) and 3 numbers with 6 segments (6, 9 and 0). These can be identified by looking at the overlap between them and 1, 4, 7, 8. For example, 3 is the only 5-segment number with 3 overlapping segments with 7. As such, if there are three letters in common between a 5-segment number and 7, it has to be 3. You can make a rule for each number and the simply check the output values against it. Then you finish the puzzle by simply adding up the resultant integers. 
```python
def _solve_part2(self, parsed_data: Any) -> Any:
    solution = 0
    patterns, output_values = parsed_data
    for pattern, output_value in zip(patterns, output_values):
        # First get 1, 4, 7 and 8
        len_to_pattern = {len(x): x for x in pattern}
        one = len_to_pattern[2]
        four = len_to_pattern[4]
        seven = len_to_pattern[3]
        out_string = ""
        for val in output_value:
            val_len = len(val)
            if val_len == 2:
                out_string += "1"
            elif val_len == 3:
                out_string += "7"
            elif val_len == 4:
                out_string += "4"
            elif val_len == 7:
                out_string += "8"
            elif val_len == 5 and len(val & four) == 2:
                out_string += "2"
            elif val_len == 5 and len(val & seven) == 3:
                out_string += "3"
            elif val_len == 5 and len(val & four) == 3 and len(val & one) == 1:
                out_string += "5"
            elif val_len == 6 and len(val & four) == 4:
                out_string += "9"
            elif val_len == 6 and len(val & four) == 3 and len(val & one) == 1:
                out_string += "6"
            elif val_len == 6 and len(val & four) == 3 and len(val & one) == 2:
                out_string += "0"
        solution += int(out_string)
    return solution
```

[Return to main page](../)