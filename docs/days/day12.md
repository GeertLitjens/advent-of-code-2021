---
layout: default
title: Day 12
description: Passage Pathing

---

## Day 12

[Return to main page](../)


Interesting problem today, sort of a population growth model almost, with exponential growth of paths at the beginning
and subsequently they go down after hitting end. Adding new paths happens through iterating all the option in a loop
until you hit the blocking conditions (end or double access to lowercase cave). Part 2 added an interesting wrinkle, but
in the end only a small addition is needed.


### Part 1
> With your submarine's subterranean subsystems subsisting suboptimally, the only way you're getting out of this cave anytime soon is by finding a path yourself. Not just a path - the only way to know if you've found the best path is to find all of them.
> 
> Fortunately, the sensors are still mostly working, and so you build a rough map of the remaining caves (your puzzle input). For example:
> ```
> start-A
> start-b
> A-c
> A-b
> b-d
> A-end
> b-end
> ```
> This is a list of how all of the caves are connected. You start in the cave named start, and your destination is the cave named end. An entry like b-d means that cave b is connected to cave d - that is, you can move between them.
> 
> So, the above cave system looks roughly like this:
> ```
>     start
>     /   \
> c--A-----b--d
>     \   /
>      end
> ```
> Your goal is to find the number of distinct paths that start at start, end at end, and don't visit small caves more than once. There are two types of caves: big caves (written in uppercase, like A) and small caves (written in lowercase, like b). It would be a waste of time to visit any small cave more than once, but big caves are large enough that it might be worth visiting them multiple times. So, all paths you find should visit small caves at most once, and can visit big caves any number of times.
> 
> Given these rules, there are 10 paths through this example cave system:
> ```
> start,A,b,A,c,A,end
> start,A,b,A,end
> start,A,b,end
> start,A,c,A,b,A,end
> start,A,c,A,b,end
> start,A,c,A,end
> start,A,end
> start,b,A,c,A,end
> start,b,A,end
> start,b,end
> ```
> (Each line in the above list corresponds to a single path; the caves visited by that path are listed in the order they are visited and separated by commas.)
> 
> Note that in this cave system, cave d is never visited by any path: to do so, cave b would need to be visited twice (once on the way to cave d and a second time when returning from cave d), and since cave b is small, this is not allowed.
> 
> Here is a slightly larger example:
> ```
> dc-end
> HN-start
> start-kj
> dc-start
> dc-HN
> LN-dc
> HN-end
> kj-sa
> kj-HN
> kj-dc
> ```
> The 19 paths through it are as follows:
> ```
> start,HN,dc,HN,end
> start,HN,dc,HN,kj,HN,end
> start,HN,dc,end
> start,HN,dc,kj,HN,end
> start,HN,end
> start,HN,kj,HN,dc,HN,end
> start,HN,kj,HN,dc,end
> start,HN,kj,HN,end
> start,HN,kj,dc,HN,end
> start,HN,kj,dc,end
> start,dc,HN,end
> start,dc,HN,kj,HN,end
> start,dc,end
> start,dc,kj,HN,end
> start,kj,HN,dc,HN,end
> start,kj,HN,dc,end
> start,kj,HN,end
> start,kj,dc,HN,end
> start,kj,dc,end
> ```
> Finally, this even larger example has 226 paths through it:
> ```
> fs-end
> he-DX
> fs-he
> start-DX
> pj-DX
> end-zg
> zg-sl
> zg-pj
> pj-he
> RW-he
> fs-DX
> pj-RW
> zg-RW
> start-pj
> he-WI
> zg-he
> pj-fs
> start-RW
> ```
> How many paths through this cave system are there that visit small caves at most once?
> 


 Slightly more interesting parser than most days. Here I use a defaultdict to create a mapping betwene the nodes, for each entry I store the connected chambers. Note that all of them are bidirectional, so a-b is also b-a. 
```python
def _parse_data(self, input_data: str) -> Any:
    cave_mapper = defaultdict(list)
    for line in input_data.split("\n"):
        if line:
            start_node, end_node = line.split("-")
            cave_mapper[start_node].append(end_node)
            cave_mapper[end_node].append(start_node)
    return cave_mapper
```

 Part 1 required some thought, but in the end it was just adding each option to a running list of open paths. As soon as you hit the end point, add it to final paths. The only thing that is a bit special is that we only add an option if it is not already in the path or if it is uppercase (e.g. large cave). 
```python
def _solve_part1(self, parsed_data: dict[str, list[str]]) -> Any:
    path_tracker = []
    final_paths = []
    # Add first parts
    for option in parsed_data["start"]:
        current_path = ["start", option]
        path_tracker.append(current_path)
    while path_tracker:
        current_path = path_tracker.pop()
        options = parsed_data[current_path[-1]]
        for option in options:
            if option == "end":
                final_paths.append(current_path + [option])
            elif option.isupper() or option not in current_path:
                path_tracker.append(current_path + [option])
    return len(final_paths)
```

### Part 2

> After reviewing the available paths, you realize you might have time to visit a single small cave twice. Specifically, big caves can be visited any number of times, a single small cave can be visited at most twice, and the remaining small caves can be visited at most once. However, the caves named start and end can only be visited exactly once each: once you leave the start cave, you may not return to it, and once you reach the end cave, the path must end immediately.
> 
> Now, the 36 possible paths through the first example above are:
> ```
> start,A,b,A,b,A,c,A,end
> start,A,b,A,b,A,end
> start,A,b,A,b,end
> start,A,b,A,c,A,b,A,end
> start,A,b,A,c,A,b,end
> start,A,b,A,c,A,c,A,end
> start,A,b,A,c,A,end
> start,A,b,A,end
> start,A,b,d,b,A,c,A,end
> start,A,b,d,b,A,end
> start,A,b,d,b,end
> start,A,b,end
> start,A,c,A,b,A,b,A,end
> start,A,c,A,b,A,b,end
> start,A,c,A,b,A,c,A,end
> start,A,c,A,b,A,end
> start,A,c,A,b,d,b,A,end
> start,A,c,A,b,d,b,end
> start,A,c,A,b,end
> start,A,c,A,c,A,b,A,end
> start,A,c,A,c,A,b,end
> start,A,c,A,c,A,end
> start,A,c,A,end
> start,A,end
> start,b,A,b,A,c,A,end
> start,b,A,b,A,end
> start,b,A,b,end
> start,b,A,c,A,b,A,end
> start,b,A,c,A,b,end
> start,b,A,c,A,c,A,end
> start,b,A,c,A,end
> start,b,A,end
> start,b,d,b,A,c,A,end
> start,b,d,b,A,end
> start,b,d,b,end
> start,b,end
> ```
> The slightly larger example above now has 103 paths through it, and the even larger example now has 3509 paths through it.
> 
> Given these new rules, how many paths through this cave system are there?


 Small extension to part 1, we now also keep track whether a path has visited a small cave twice. If not, then we can add lowercase options. Other than that, exactly the same as part 1. 
```python
def _solve_part2(self, parsed_data: dict[str, list[str]]) -> Any:
    path_tracker = []
    final_paths = []
    for option in parsed_data["start"]:
        path_tracker.append({"path": ["start", option], "twice": False})
    while path_tracker:
        current_path = path_tracker.pop()
        options = parsed_data[current_path["path"][-1]]
        for option in options:
            if option == "end":
                final_paths.append({"path": current_path["path"] + [option], "twice": current_path["twice"]})
            elif option.isupper() or option not in current_path["path"]:
                path_tracker.append({"path": current_path["path"] + [option], "twice": current_path["twice"]})
            elif not current_path["twice"] and option != "start":
                path_tracker.append({"path": current_path["path"] + [option], "twice": True})
    return len(final_paths)
```

[Return to main page](../)