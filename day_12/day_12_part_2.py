"""
--- Part Two ---
Fortunately, the Elves are trying to order so much fence that they qualify for a bulk discount!

Under the bulk discount, instead of using the perimeter to calculate the price, you need to use the number of sides each region has. Each straight section of fence counts as a side, regardless of how long it is.

Consider this example again:

AAAA
BBCD
BBCC
EEEC
The region containing type A plants has 4 sides, as does each of the regions containing plants of type B, D, and E. However, the more complex region containing the plants of type C has 8 sides!

Using the new method of calculating the per-region price by multiplying the region's area by its number of sides, regions A through E have prices 16, 16, 32, 4, and 12, respectively, for a total price of 80.

The second example above (full of type X and O plants) would have a total price of 436.

Here's a map that includes an E-shaped region full of type E plants:

EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
The E-shaped region has an area of 17 and 12 sides for a price of 204. Including the two regions full of type X plants, this map has a total price of 236.

This map has a total price of 368:

AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
It includes two regions full of type B plants (each with 4 sides) and a single region full of type A plants (with 4 sides on the outside and 8 more sides on the inside, a total of 12 sides). Be especially careful when counting the fence around regions like the one full of type A plants; in particular, each section of fence has an in-side and an out-side, so the fence does not connect across the middle of the region (where the two B regions touch diagonally). (The Elves would have used the Möbius Fencing Company instead, but their contract terms were too one-sided.)

The larger example from before now has the following updated prices:

A region of R plants with price 12 * 10 = 120.
A region of I plants with price 4 * 4 = 16.
A region of C plants with price 14 * 22 = 308.
A region of F plants with price 10 * 12 = 120.
A region of V plants with price 13 * 10 = 130.
A region of J plants with price 11 * 12 = 132.
A region of C plants with price 1 * 4 = 4.
A region of E plants with price 13 * 8 = 104.
A region of I plants with price 14 * 16 = 224.
A region of M plants with price 5 * 6 = 30.
A region of S plants with price 3 * 6 = 18.
Adding these together produces its new total price of 1206.

What is the new total price of fencing all regions on your map?
"""

import numpy as np
from collections import defaultdict

def parse_grid(filename):
    """Parse the grid from the input file into a NumPy array."""
    with open(filename, 'r') as file:
        grid = np.array([list(line.strip()) for line in file.readlines()])
    return grid

def find_regions(grid):
    """Identify all unique regions in the grid using flood-fill."""
    visited = np.zeros_like(grid, dtype=bool)
    regions = defaultdict(list)
    region_id_counter = 0  # Unique ID for each region
    
    def flood_fill(y, x, region_id):
        stack = [(y, x)]
        while stack:
            cy, cx = stack.pop()
            if visited[cy, cx]:
                continue
            visited[cy, cx] = True
            regions[region_id].append((cy, cx))
            for ny, nx in [(cy-1, cx), (cy+1, cx), (cy, cx-1), (cy, cx+1)]:
                if 0 <= ny < grid.shape[0] and 0 <= nx < grid.shape[1]:
                    if not visited[ny, nx] and grid[ny, nx] == grid[y, x]:
                        stack.append((ny, nx))
    
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if not visited[y, x]:
                region_type = grid[y, x]
                region_id = f"{region_type}_{region_id_counter}"  # Unique ID for this region
                region_id_counter += 1
                flood_fill(y, x, region_id)
    
    return regions

def count_sides(region_type, region_coords):
    """Count the number of unique sides in the fence grid."""
    def offset_position(pos, offset):
        """Calculate a new position by applying an offset."""
        return tuple(a + b for a, b in zip(pos, offset))
    
    directions = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1),
        "upleft": (-1, -1),
        "upright": (-1, 1),
        "downleft": (1, -1),
        "downright": (1, 1),
    }
    
    sides = 0
    
    for pos in region_coords:
        # Check outer edges
        if offset_position(pos, directions["left"]) not in region_coords and \
           offset_position(pos, directions["up"]) not in region_coords:
            sides += 1
        if offset_position(pos, directions["right"]) not in region_coords and \
           offset_position(pos, directions["up"]) not in region_coords:
            sides += 1
        if offset_position(pos, directions["right"]) not in region_coords and \
           offset_position(pos, directions["down"]) not in region_coords:
            sides += 1
        if offset_position(pos, directions["left"]) not in region_coords and \
           offset_position(pos, directions["down"]) not in region_coords:
            sides += 1
        
        # Check inner edges
        if offset_position(pos, directions["left"]) in region_coords and \
           offset_position(pos, directions["up"]) in region_coords and \
           offset_position(pos, directions["upleft"]) not in region_coords:
            sides += 1
        if offset_position(pos, directions["right"]) in region_coords and \
           offset_position(pos, directions["up"]) in region_coords and \
           offset_position(pos, directions["upright"]) not in region_coords:
            sides += 1
        if offset_position(pos, directions["left"]) in region_coords and \
           offset_position(pos, directions["down"]) in region_coords and \
           offset_position(pos, directions["downleft"]) not in region_coords:
            sides += 1
        if offset_position(pos, directions["right"]) in region_coords and \
           offset_position(pos, directions["down"]) in region_coords and \
           offset_position(pos, directions["downright"]) not in region_coords:
            sides += 1
    
    return sides

def calculate_total_price(grid):
    """Calculate the total price for fencing all regions."""
    regions = find_regions(grid)
    total_price = 0
    
    for region_type, region_coords in regions.items():
        sides = count_sides(region_type, region_coords)
        area = len(region_coords)
        price = area * sides
        total_price += price
        # print(f"Region '{region_type}' - Area: {area}, Sides: {sides}, Price: {price}")

    return total_price

def main():
    grid = parse_grid("./day_12/day_12_input.txt")
    total_price = calculate_total_price(grid)
    print(f"Total Price: {total_price}")

if __name__ == "__main__":
    main()