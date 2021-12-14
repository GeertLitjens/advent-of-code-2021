---
layout: default
title: Day 14
description: Extended Polymerization

---

## Day 14

[Return to main page](../)


The most challenging puzzle for me so far, obviously mostly part 2. I made a simple, straighforward list iterator for
part 1, but of course that could not handle 2^40 elements in part 2. So I had to rethink my strategy and it took me a
bit of time to realize that I could just keep track again of only the pairs and the number of pairs as their positions
do not matter. So I used the Python Counter class for that, which is essentially a fancy dictionary structure. I left my
old solution for part 1, just to show how you can do it in a very computationally inefficient wat as well :).


### Part 1
> The incredible pressures at this depth are starting to put a strain on your submarine. The submarine has polymerization equipment that would produce suitable materials to reinforce the submarine, and the nearby volcanically-active caves should even have the necessary input elements in sufficient quantities.
> 
> The submarine manual contains instructions for finding the optimal polymer formula; specifically, it offers a polymer template and a list of pair insertion rules (your puzzle input). You just need to work out what polymer would result after repeating the pair insertion process a few times.
> 
> For example:
> ```
> NNCB
> 
> CH -> B
> HH -> N
> CB -> H
> NH -> C
> HB -> C
> HC -> B
> HN -> C
> NN -> C
> BH -> H
> NC -> B
> NB -> B
> BN -> B
> BB -> N
> BC -> B
> CC -> N
> CN -> C
> ```
> The first line is the polymer template - this is the starting point of the process.
> 
> The following section defines the pair insertion rules. A rule like AB -> C means that when elements A and B are immediately adjacent, element C should be inserted between them. These insertions all happen simultaneously.
> 
> So, starting with the polymer template NNCB, the first step simultaneously considers all three pairs:
> 
> - The first pair (NN) matches the rule NN -> C, so element C is inserted between the first N and the second N.
> - The second pair (NC) matches the rule NC -> B, so element B is inserted between the N and the C.
> - The third pair (CB) matches the rule CB -> H, so element H is inserted between the C and the B.
> 
> Note that these pairs overlap: the second element of one pair is the first element of the next pair. Also, because all pairs are considered simultaneously, inserted elements are not considered to be part of a pair until the next step.
> 
> After the first step of this process, the polymer becomes NCNBCHB.
> 
> Here are the results of a few steps using the above rules:
> ```
> Template:     NNCB
> After step 1: NCNBCHB
> After step 2: NBCCNBBBCBHCB
> After step 3: NBBBCNCCNBBNBNBBCHBHHBCHB
> After step 4: NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB
> ```
> This polymer grows quickly. After step 5, it has length 97; After step 10, it has length 3073. After step 10, B occurs 1749 times, C occurs 298 times, H occurs 161 times, and N occurs 865 times; taking the quantity of the most common element (B, 1749) and subtracting the quantity of the least common element (H, 161) produces 1749 - 161 = 1588.
> 
> Apply 10 steps of pair insertion to the polymer template and find the most and least common elements in the result. What do you get if you take the quantity of the most common element and subtract the quantity of the least common element?


 Again data consists of two parts, so first split on a double new line and turn the template string into a list. Then parse the rules into a dictionary. 
```python
def _parse_data(self, input_data: str) -> Any:
    template, rules_string = input_data.split("\n\n")
    template = [x for x in template]
    rules = {}
    for line in rules_string.split("\n"):
        if line:
            k, v = line.split(" -> ")
            rules[k] = v
    return template, rules
```

 Part 1 just work directly on lists. Iterate over the old list, a the first element of a pair  and a new element to the new list based on the rules. This works well and fast, however it does not scale to a large number of turns as the length of the list grows exponentially. 
```python
def _solve_part1(self, parsed_data: Any) -> Any:
    old_poly, rules = parsed_data
    for step in range(10):
        new_poly = []
        for e_i in range(len(old_poly) - 1):
            new_poly.append(old_poly[e_i])
            new_poly.append(rules[old_poly[e_i] + old_poly[e_i + 1]])
        new_poly.append(old_poly[-1])
        old_poly = new_poly
    cntr = Counter(new_poly)
    counts = cntr.most_common()
    return counts[0][1] - counts[-1][1]
```

### Part 2

> The resulting polymer isn't nearly strong enough to reinforce the submarine. You'll need to run more steps of the pair insertion process; a total of 40 steps should do it.
> 
> In the above example, the most common element is B (occurring 2192039569602 times) and the least common element is H (occurring 3849876073 times); subtracting these produces 2188189693529.
> 
> Apply 40 steps of pair insertion to the polymer template and find the most and least common elements in the result. What do you get if you take the quantity of the most common element and subtract the quantity of the least common element?

 Smarter solution: we only keep track of the pairs and how often they occur. Then at each step, iterate over all the pairs, remove the originals and replace them with two new ones pased on the rules. Last trick is to keep a separate counter to actually count then number of individual elements so we don't have to figure that out from the pair counter at the end. 
```python
def _solve_part2(self, parsed_data: Any) -> Any:
    old_poly, rules = parsed_data
    poly_dict = Counter(map(str.__add__, old_poly, old_poly[1:]))
    elem_count = Counter(old_poly)
    for step in range(40):
        for (elem_1, elem_2), count in poly_dict.copy().items():
            new_elem = rules[elem_1 + elem_2]
            poly_dict[elem_1 + elem_2] -= count
            poly_dict[elem_1 + new_elem] += count
            poly_dict[new_elem + elem_2] += count
            elem_count[new_elem] += count
    return max(elem_count.values()) - min(elem_count.values())
```

[Return to main page](../)