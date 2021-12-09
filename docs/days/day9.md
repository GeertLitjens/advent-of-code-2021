---
layout: default
title: Day 9
description: Smoke Basin

---

## Day 9

[Return to main page](../)


Today was a nice image analysis challenge that I was very familiar with. The only caveat is that using scikit-image does
feel a bit like cheating, but it didn't make sense to me to reimplement a local minima filter and a watershed transform
while perfectly fine and fast version exist within the Python ecosystem. So very simple a short solutions today.


### Part 1
> These caves seem to be lava tubes. Parts are even still volcanically active; small hydrothermal vents release smoke into the caves that slowly settles like rain.
> 
> If you can model how the smoke flows through the caves, you might be able to avoid it and be that much safer. The submarine generates a heightmap of the floor of the nearby caves for you (your puzzle input).
> 
> Smoke flows to the lowest point of the area it's in. For example, consider the following heightmap:
> ```
> 2199943210
> 3987894921
> 9856789892
> 8767896789
> 9899965678
> ```
> Each number corresponds to the height of a particular location, where 9 is the highest and 0 is the lowest a location can be.
> 
> Your first goal is to find the low points - the locations that are lower than any of its adjacent locations. Most locations have four adjacent locations (up, down, left, and right); locations on the edge or corner of the map have three or two adjacent locations, respectively. (Diagonal locations do not count as adjacent.)
> 
> In the above example, there are four low points, all highlighted: two are in the first row (a 1 and a 0), one is in the third row (a 5), and one is in the bottom row (also a 5). All other locations on the heightmap have some lower adjacent location, and so are not low points.
> 
> The risk level of a low point is 1 plus its height. In the above example, the risk levels of the low points are 2, 1, 6, and 6. The sum of the risk levels of all low points in the heightmap is therefore 15.
> 
> Find all of the low points on your heightmap. What is the sum of the risk levels of all low points on your heightmap?
> 


 Data parsing was straightforward, simply split the lines and conver the characters to ints. 
```python
def _parse_data(self, input_data: str) -> Any:
    return np.array([[int(char) for char in x] for x in input_data.split("\n") if x])
```

 The only thing that required some thought was the border handling. The default options for peak_local_max don't work for this specific problem, so I simply padded the input with the highest value, 9. Then I invert the array to be able to look for maxima instead of minima. The last part is a simpel sum over the returned coordinates for the different minima. 
```python
def _solve_part1(self, parsed_data: Any) -> Any:
    padded_data = np.pad(parsed_data, ((1, 1), (1, 1)), 'constant', constant_values=9)
    min_coords = peak_local_max(-padded_data)
    return np.sum(padded_data[tuple(min_coords.T)] + 1)
```

### Part 2

> Next, you need to find the largest basins so you know what areas are most important to avoid.
> 
> A basin is all locations that eventually flow downward to a single low point. Therefore, every low point has a basin, although some basins are very small. Locations of height 9 do not count as being in any basin, and all other locations will always be part of exactly one basin.
> 
> The size of a basin is the number of locations within the basin, including the low point. The example above has four basins.
> 
> The top-left basin, size 3:
> ```
> 2199943210
> 3987894921
> 9856789892
> 8767896789
> 9899965678
> ```
> The top-right basin, size 9:
> ```
> 2199943210
> 3987894921
> 9856789892
> 8767896789
> 9899965678
> ```
> The middle basin, size 14:
> ```
> 2199943210
> 3987894921
> 9856789892
> 8767896789
> 9899965678
> ```
> The bottom-right basin, size 9:
> ```
> 2199943210
> 3987894921
> 9856789892
> 8767896789
> 9899965678
> ```
> Find the three largest basins and multiply their sizes together. In the above example, this is 9 * 14 * 9 = 1134.
> 
> What do you get if you multiply together the sizes of the three largest basins?


 As soon as the text started talking about basins, I knew this was a simple masked watershed transform. I directly used the one from scikit-image. Subsequently, I use regionprops to get the area for the individual labels, I sort them based on size and get the top 3, which I multiply together. 
```python
def _solve_part2(self, parsed_data: Any) -> Any:
    labels = watershed(parsed_data, mask=parsed_data != 9)
    props = regionprops(labels)
    return np.prod(sorted([prop.area for prop in props])[-3:])
```

[Return to main page](../)